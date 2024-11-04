import discord
from discord.ext import commands

class UnmuteAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unmuteall')
    @commands.has_permissions(administrator=True)
    async def unmute_all(self, ctx):
        unmuted_members = []

        for member in ctx.guild.members:
            if member.timed_out_until:
                await member.edit(timed_out_until=None)
                unmuted_members.append(member)

        if len(unmuted_members) == 0:
            description = "> *No members were in timeout.*"
        else:
            description = f"> *Unmuted {len(unmuted_members)} members.*"

        embed = discord.Embed(
            title="> ***ACTION: <:timeout:1287330885884055634> Unmute All***",
            description=description,
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Command executed by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @unmute_all.error
    async def unmute_all_error(self, ctx, error):
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
    await bot.add_cog(UnmuteAll(bot))
