import discord
from discord.ext import commands

class AvatarView(discord.ui.View):
    def __init__(self, ctx, user):
        super().__init__(timeout=50.0)
        self.ctx = ctx
        self.user = user
        self.showing_avatar = True

    @discord.ui.button(emoji="<:avatar:1284538151376785449>",label="Show Banner", style=discord.ButtonStyle.gray)
    async def toggle_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return

        if self.showing_avatar:
            # Re-fetch the user to get the banner
            user = await self.ctx.bot.fetch_user(self.user.id)

            if not user.banner:
                await interaction.response.send_message(f"**{user}** has no banner set.", ephemeral=True)
                return

            formats = ["png"]
            if user.banner.is_animated():
                formats.append("gif")

            banner_urls = [f"[{fmt.upper()}]({user.banner.replace(format=fmt, size=1024)})" for fmt in formats]
            embed = discord.Embed(colour=user.accent_color or discord.Color.default())
            
            # Set the image to GIF if the banner is animated, otherwise use PNG
            image_format = "gif" if user.banner.is_animated() else "png"
            embed.set_image(url=user.banner.replace(format=image_format, size=256))
            
            embed.description = " - ".join(banner_urls)
            embed.title = f"🖼 Banner of **{user}**"

            button.label = "Show Avatar"
            
        else:
            formats = ["png"]
            if self.user.avatar.is_animated():
                formats.append("gif")

            avatar_urls = [f"[{fmt.upper()}]({self.user.avatar.replace(format=fmt, size=1024)})" for fmt in formats]
            embed = discord.Embed(colour=self.user.top_role.colour)
            
            # Set the image to GIF if the avatar is animated, otherwise use PNG
            image_format = "gif" if self.user.avatar.is_animated() else "png"
            embed.set_image(url=self.user.avatar.replace(format=image_format, size=256))
            
            embed.description = " - ".join(avatar_urls)
            embed.title = f"🖼 Avatar of **{self.user}**"

            button.label = "Show Banner"

        self.showing_avatar = not self.showing_avatar
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get the avatar of you or someone else"""
        user = user or ctx.author
        if not user.avatar:
            return await ctx.send(f"**{user}** has no avatar set.")

        formats = ["png"]
        if user.avatar.is_animated():
            formats.append("gif")

        avatar_urls = [f"[{fmt.upper()}]({user.avatar.replace(format=fmt, size=1024)})" for fmt in formats]
        embed = discord.Embed(colour=user.top_role.colour)
        
        # Set the image to GIF if the avatar is animated, otherwise use PNG
        image_format = "gif" if user.avatar.is_animated() else "png"
        embed.set_image(url=user.avatar.replace(format=image_format, size=256))
        
        embed.description = " - ".join(avatar_urls)
        embed.title = f"🖼 Avatar of **{user}**"

        view = AvatarView(ctx, user)
        view.message = await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
