import discord
from discord.ext import commands

class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nick', help='Change your own or another user\'s nickname')
    async def nick(self, ctx, member: discord.Member = None, *, nickname: str):
        if member is None:
            # Change the author's nickname
            # Removed the try-except block for changing author's nickname
            pass
        else:
            # Change the mentioned member's nickname
            if ctx.author.guild_permissions.manage_nicknames:
                try:
                    await member.edit(nick=nickname)
                    embed = discord.Embed(
                        title="> <:write:1287339964236828692> ***Nickname Changed***",
                        description=f'> <a:x_dot:1260287109219225663> *Nickname for {member.mention} has been changed to {nickname}*',
                        color=discord.Color.dark_theme()
                    )
                    await ctx.send(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="Error",
                        description='I do not have permission to change this user\'s nickname.',
                        color=discord.Color.dark_red()
                    )
                    await ctx.send(embed=embed)
                except Exception as e:
                    await ctx.send(f"An error occurred: {e}")
            else:
                embed = discord.Embed(
                    title="Error",
                    description='You do not have permission to change other users\' nicknames.',
                    color=discord.Color.dark_red()
                )
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Nickname(bot))

