import discord
from discord.ext import commands

class HideChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hide')
    @commands.has_permissions(manage_channels=True)
    async def hide_channel(self, ctx):
        """Hides the current channel from everyone."""
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.view_channel is False:
            embed = discord.Embed(
                title="> <:lock:1287702040742465608> ***Channel Already Hidden***",
                description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} is already hidden from everyone.*",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
            return

        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:lock:1287702040742465608> ***Channel Hidden***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} has been hidden from everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        view = UnhideButtonView(ctx.author, channel)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    @hide_channel.error
    async def hide_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="> <:x:1287702040742465608> ***Permission Denied***",
                description="> <a:x_dot:1260287109219225663> *You do not have permission to manage channels.*",
                color=discord.Color.dark_theme()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="> <:x:1287702040742465608> ***Error***",
                description=f"> <a:x_dot:1260287109219225663> *An unexpected error occurred: {error}*",
                color=discord.Color.dark_theme()
            )
            await ctx.send(embed=embed)

class UnhideButton(discord.ui.Button):
    def __init__(self, author, channel):
        super().__init__(style=discord.ButtonStyle.secondary, label="Unhide", emoji="<:unlock:1287701970890657823>")
        self.author = author
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to unhide this channel.", ephemeral=True)
            return

        overwrite = self.channel.overwrites_for(self.channel.guild.default_role)
        overwrite.view_channel = True
        await self.channel.set_permissions(self.channel.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:unlock:1287701970890657823> ***Channel Unhidden***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {self.channel.mention} has been unhidden for everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

        # Disable the button after use
        self.view.disable_all_items()
        await self.view.message.edit(view=self.view)

class UnhideButtonView(discord.ui.View):
    def __init__(self, author, channel):
        super().__init__(timeout=40)  # Set timeout to 40 seconds
        self.author = author
        self.channel = channel
        self.message = None
        self.add_item(UnhideButton(author, channel))

    async def on_timeout(self):
        # Disable the button after timeout
        self.disable_all_items()
        if self.message:
            await self.message.edit(view=self)

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True

async def setup(bot):
    await bot.add_cog(HideChannel(bot))