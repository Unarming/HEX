import discord
from discord.ext import commands
from datetime import timedelta
from discord.ui import Button, View

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timeout", aliases=["mute", "m"])
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason: str = None):
        """
        Timeout a member for a specified duration.
        Duration can be specified in seconds (s), minutes (m), hours (h), or days (d).
        """
        try:
            # Determine the duration in seconds
            time_unit = duration[-1]
            time_value = int(duration[:-1])
            if time_unit == 's':
                duration_seconds = time_value
            elif time_unit == 'm':
                duration_seconds = time_value * 60
            elif time_unit == 'h':
                duration_seconds = time_value * 3600
            elif time_unit == 'd':
                duration_seconds = time_value * 86400
            else:
                await ctx.send("Invalid time unit! Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.")
                return

            # Apply timeout
            await member.timeout(timedelta(seconds=duration_seconds), reason=reason)
            
            # Create server embed without image
            embed = discord.Embed(
                title="> ***ACTION: <:timeout:1287330885884055634> MUTE***",
                description=f"> <:member:1287330843286831194> Member: {member.mention}\n> <:timeout:1287330885884055634> Duration: {duration}\n> <:reason:1287280377731223593> Reason: {reason}",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Requested by {ctx.author.name}")  # Footer with user avatar and username
            embed.set_thumbnail(url=member.display_avatar.url)  # Thumbnail of the muted member
            
            # Send a DM to the user being muted
            try:
                dm_embed = discord.Embed(
                    title="You have been muted",
                    description=f"You have been muted in {ctx.guild.name}.",
                    color=discord.Color.dark_theme()
                )
                dm_embed.add_field(name="Reason", value=reason, inline=False)
                dm_embed.add_field(name="Duration", value=duration, inline=False)
                dm_embed.set_footer(text=f"Muted by {ctx.author}", icon_url=ctx.author.display_avatar.url)
                await member.send(embed=dm_embed)
                dm_status = f"> <:tick:1287282967517073511> *DM successfully sent to {member.mention}.*"
            except discord.Forbidden:
                dm_status = f"> <:cross:1287283014178570282> *Could not send DM to {member.mention}.*"

            embed.add_field(name="> <:dm:1287281448209879061> ***DM Status***", value=dm_status, inline=False)

            # Create unmute button
            button = Button(label="Unmute", style=discord.ButtonStyle.secondary)

            async def unmute_callback(interaction):
                await member.timeout(None)  # Remove timeout
                await interaction.response.send_message(f"{member.mention} has been unmuted.", ephemeral=True)
                button.disabled = True
                await interaction.message.edit(view=view)

            button.callback = unmute_callback

            # Create view and add button
            class UnmuteView(View):
                def __init__(self, author):
                    super().__init__()
                    self.author = author

                async def interaction_check(self, interaction: discord.Interaction) -> bool:
                    if interaction.user != self.author:
                        await interaction.response.send_message("Only the command author can use this button.", ephemeral=True)
                        return False
                    return True

            view = UnmuteView(ctx.author)
            view.add_item(button)

            # Send the embed with the button
            await ctx.send(embed=embed, view=view)

            await view.wait()
            if not button.disabled:
                button.disabled = True
                await ctx.send("The unmute button has been disabled due to timeout")
                await ctx.message.edit(view=view)  # Update the message to disable the button
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @timeout.error
    async def timeout_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking the timeout command.
        """
        embed = discord.Embed(
            title="> ***Error***",
            color=discord.Color.dark_magenta()
        )

        if isinstance(error, commands.MissingPermissions):
            embed.description = "> - *You do not have the ``Timeout permission`` permissions to use this command.*"
        elif isinstance(error, commands.MemberNotFound):
            embed.description = "> - *The specified member was not found.*"
        elif isinstance(error, commands.BadArgument):
            embed.description = "> - *Invalid argument provided.*"
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = "> - *Please mention a member to mute*\n> - *__Command usage:__* ``` &mute <member> [duration] [reason] ```\n> - *__Example command:__* ``` &mute @shankar 10m shutup ```\n> - *__Time Unit:__* `Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.`"
        elif isinstance(error, discord.Forbidden):
            embed.description = "> - *I do not have permission to mute this member. They might have a higher role than me.*"
        else:
            embed.description = "> - *An unexpected error occurred.*"
            raise error

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Timeout(bot))