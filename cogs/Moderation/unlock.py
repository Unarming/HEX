import discord
from discord.ext import commands

class UnlockChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        """Unlocks the current channel for everyone."""
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.send_messages is True:
            embed = discord.Embed(
                title="> <:unlock:1287701970890657823> ***Channel Already Unlocked***",
                description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} is already unlocked for everyone.*",
                color=discord.Color.dark_theme()
            )
            embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
            return

        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="> <:unlock:1287701970890657823> ***Channel Unlocked***",
            description=f"> <a:x_dot:1260287109219225663> *The channel {channel.mention} has been unlocked for everyone.*",
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Action by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @unlock_channel.error
    async def unlock_channel_error(self, ctx, error):
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
    await bot.add_cog(UnlockChannel(bot))
