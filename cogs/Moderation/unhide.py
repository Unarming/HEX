import discord
from discord.ext import commands

class UnhideChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unhide')
    @commands.has_permissions(manage_channels=True)
    async def unhide_channel(self, ctx):
        """Unhides the current channel for everyone."""
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.view_channel is True:
            embed = discord.Embed(
                title="> <:unlock:1287701970890657823> ***Channel Already Unhidden***",
                description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} is already visible to everyone.*",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
            return

        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:unlock:1287701970890657823> ***Channel Unhidden***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} has been unhidden for everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @unhide_channel.error
    async def unhide_channel_error(self, ctx, error):
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

async def setup(bot):
    await bot.add_cog(UnhideChannel(bot))
