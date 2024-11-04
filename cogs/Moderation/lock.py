import discord
from discord.ext import commands

class LockChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx):
        """Locks the current channel from everyone."""
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.send_messages is False:
            embed = discord.Embed(
                title="> <:lock:1287702040742465608> ***Channel Already Locked***",
                description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} is already locked for everyone.*",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
            return

        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:lock:1287702040742465608> ***Channel Locked***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} has been locked for everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        view = UnlockButtonView(ctx.author, channel)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    @lock_channel.error
    async def lock_channel_error(self, ctx, error):
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

class UnlockButton(discord.ui.Button):
    def __init__(self, author, channel):
        super().__init__(style=discord.ButtonStyle.secondary, label="Unlock", emoji="<:unlock:1287701970890657823>")
        self.author = author
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to unlock this channel.", ephemeral=True)
            return

        overwrite = self.channel.overwrites_for(self.channel.guild.default_role)
        overwrite.send_messages = True
        await self.channel.set_permissions(self.channel.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:unlock:1287701970890657823> ***Channel Unlocked***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {self.channel.mention} has been unlocked for everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

        # Disable the button after use
        self.view.disable_all_items()
        await self.view.message.edit(view=self.view)

class UnlockButtonView(discord.ui.View):
    def __init__(self, author, channel):
        super().__init__(timeout=40)  # Set timeout to 40 seconds
        self.author = author
        self.channel = channel
        self.message = None
        self.add_item(UnlockButton(author, channel))

    async def on_timeout(self):
        # Disable the button after timeout
        self.disable_all_items()
        if self.message:
            await self.message.edit(view=self)

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True

async def setup(bot):
    await bot.add_cog(LockChannel(bot))
