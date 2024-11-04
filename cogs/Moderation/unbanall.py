import discord
from discord.ext import commands

class UnbanAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unbanall')
    @commands.has_permissions(administrator=True)
    async def unban_all(self, ctx):
        banned_users = ctx.guild.bans()  # Don't await here, `bans()` is not a coroutine
        unbanned_users = []

        async for ban_entry in banned_users:  # Use `async for` to iterate over the async generator
            user = ban_entry.user
            await ctx.guild.unban(user)
            unbanned_users.append(user)

        if len(unbanned_users) == 0:
            description = "> <a:x_dot:1260287109219225663> *No users were banned.*"
        else:
            description = f"> <a:x_dot:1260287109219225663> *Unbanned {len(unbanned_users)} users.*"

        embed = discord.Embed(
            title="> ***ACTION: <:ban:1287274889178517524> Unban All***",
            description=description,
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Command executed by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @unban_all.error
    async def unban_all_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You do not have the `administrator` permissions to use this command.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {str(error)}",
                color=discord.Color.red()
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UnbanAll(bot))
