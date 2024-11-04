import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unmute", aliases=["um"])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """
        Unmute a member.
        """
        try:
            # Remove timeout
            await member.timeout(None, reason=reason)
            
            # Create server embed
            embed = discord.Embed(
                title="> ***ACTION: UNMUTE***",
                description=f"> <:member:1287330843286831194> Member: {member.mention}\n> <:reason:1287280377731223593> Reason: {reason}",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Requested by {ctx.author.name}")  # Footer with user avatar and username
            embed.set_thumbnail(url=member.display_avatar.url)  # Thumbnail of the unmuted member
            
            # Send a DM to the user being unmuted
            try:
                dm_embed = discord.Embed(
                    title="You have been unmuted",
                    description=f"You have been unmuted in {ctx.guild.name}.",
                    color=discord.Color.green()
                )
                dm_embed.add_field(name="Reason", value=reason, inline=False)
                dm_embed.set_footer(text=f"Unmuted by {ctx.author}", icon_url=ctx.author.display_avatar.url)
                await member.send(embed=dm_embed)
                dm_status = f"> <:tick:1287282967517073511> *DM successfully sent to {member.mention}.*"
            except discord.Forbidden:
                dm_status = f"> <:cross:1287283014178570282> *Could not send DM to {member.mention}.*"

            embed.add_field(name="> <:dm:1287281448209879061> ***DM Status***", value=dm_status, inline=False)

            # Send the embed
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @unmute.error
    async def unmute_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking the unmute command.
        """
        embed = discord.Embed(
            title="> ***Error***",
            color=discord.Color.red()
        )

        if isinstance(error, commands.MissingPermissions):
            embed.description = "> - *You do not have the ``Timeout permission`` permissions to use this command.*"
        elif isinstance(error, commands.MemberNotFound):
            embed.description = "> - *The specified member was not found.*"
        elif isinstance(error, commands.BadArgument):
            embed.description = "> - *Invalid argument provided.*"
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = "> - *Please mention a member to unmute*\n> - *__Command usage:__* ``` &unmute <member> [reason] ```\n> - *__Example command:__* ``` &unmute @shankar welcome back ```"
        elif isinstance(error, discord.Forbidden):
            embed.description = "> - *I do not have permission to unmute this member. They might have a higher role than me.*"
        else:
            embed.description = "> - *An unexpected error occurred.*"
            raise error

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Unmute(bot))
