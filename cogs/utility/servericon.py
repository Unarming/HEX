import discord
from discord.ext import commands

class ServerIconView(discord.ui.View):
    def __init__(self, ctx, guild):
        super().__init__(timeout=50.0)
        self.ctx = ctx
        self.guild = guild
        self.showing_icon = True

    @discord.ui.button(emoji="<:avatar:1284538151376785449>",label="Show Banner", style=discord.ButtonStyle.gray)
    async def toggle_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return

        if self.showing_icon:
            if not self.guild.banner:
                await interaction.response.send_message(f"**{self.guild}** has no banner set.", ephemeral=True)
                return

            formats = ["png"]
            if self.guild.banner.is_animated():
                formats.append("gif")

            banner_urls = [f"[{fmt.upper()}]({self.guild.banner.replace(format=fmt, size=1024)})" for fmt in formats]
            embed = discord.Embed(colour=discord.Color.default())
            
            # Set the image to GIF if the banner is animated, otherwise use PNG
            image_format = "gif" if self.guild.banner.is_animated() else "png"
            embed.set_image(url=self.guild.banner.replace(format=image_format, size=256))
            
            embed.description = " - ".join(banner_urls)
            embed.title = f"🖼 Banner of **{self.guild}**"

            button.label = "Show Icon"
        else:
            if not self.guild.icon:
                await interaction.response.send_message(f"**{self.guild}** has no icon set.", ephemeral=True)
                return

            formats = ["png"]
            if self.guild.icon.is_animated():
                formats.append("gif")

            icon_urls = [f"[{fmt.upper()}]({self.guild.icon.replace(format=fmt, size=1024)})" for fmt in formats]
            embed = discord.Embed(colour=discord.Color.default())
            
            # Set the image to GIF if the icon is animated, otherwise use PNG
            image_format = "gif" if self.guild.icon.is_animated() else "png"
            embed.set_image(url=self.guild.icon.replace(format=image_format, size=256))
            
            embed.description = " - ".join(icon_urls)
            embed.title = f"🖼 Icon of **{self.guild}**"

            button.label = "Show Banner"

        self.showing_icon = not self.showing_icon
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

class ServerIcon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["servericon","guildicon"])
    @commands.guild_only()
    async def icon(self, ctx):
        """Get the icon of the server"""
        guild = ctx.guild
        if not guild.icon:
            return await ctx.send(f"**{guild}** has no icon set.")

        formats = ["png"]
        if guild.icon.is_animated():
            formats.append("gif")

        icon_urls = [f"[{fmt.upper()}]({guild.icon.replace(format=fmt, size=1024)})" for fmt in formats]
        embed = discord.Embed(colour=discord.Color.default())
        
        # Set the image to GIF if the icon is animated, otherwise use PNG
        image_format = "gif" if guild.icon.is_animated() else "png"
        embed.set_image(url=guild.icon.replace(format=image_format, size=256))
        
        embed.description = " - ".join(icon_urls)
        embed.title = f"🖼 Icon of **{guild}**"

        view = ServerIconView(ctx, guild)
        view.message = await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ServerIcon(bot))