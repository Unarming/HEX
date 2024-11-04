import discord
from discord.ext import commands
import asyncio  # Import asyncio for adding delay

class Confirm(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=50.0)
        self.author = author
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.secondary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return
        self.value = False
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nuke", aliases=["n"])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        """
        Nuke a channel by deleting it and creating a new one with the same properties.
        """
        channel = channel or ctx.channel

        # Create a confirmation view
        view = Confirm(ctx.author)
        embed = discord.Embed(
            title="Confirmation",
            description="Are you sure you want to nuke this channel?",
            color=discord.Color.dark_magenta()
        )
        view.message = await ctx.send(embed=embed, view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Nuke command timed out.", delete_after=10.0)
            return
        elif not view.value:
            await ctx.send("Nuke command cancelled.", delete_after=10.0)
            return

        # Save channel properties
        channel_name = channel.name
        channel_topic = channel.topic
        channel_position = channel.position
        channel_category = channel.category
        channel_permissions = channel.overwrites

        # Clone the channel with the same permissions
        new_channel = await channel.clone(reason=f"Channel nuked by {ctx.author}")

        # Delete the original channel
        await channel.delete()

        # Set the position and category of the new channel
        await new_channel.edit(position=channel_position, category=channel_category)

        # Apply the same permissions to the new channel
        for role, overwrite in channel_permissions.items():
            await new_channel.set_permissions(role, overwrite=overwrite)

        # Send a message in the new channel
        embed = discord.Embed(
            title="> ***ACTION: NUKE***",
            description=f"> - *This channel ({channel.mention}) has been nuked by {ctx.author.mention} 💥*",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Nuked by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        # Send the embed message before deleting the channel
        await new_channel.send(embed=embed, delete_after=10.0)

    @nuke.error
    async def nuke_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        """
        embed = discord.Embed(
            title="> ***Error***",
            color=discord.Color.red()
        )

        if isinstance(error, commands.MissingPermissions):
            embed.description = "> - *You do not have the required permissions to use this command.*"
        else:
            embed.description = "> - *An unexpected error occurred.*"
            raise error

        await ctx.send(embed=embed, delete_after=5.0)

async def setup(bot):
    await bot.add_cog(Nuke(bot))
