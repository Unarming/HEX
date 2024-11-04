import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, target: str, amount: int = None, *, text: str = None):
        if target.isdigit():
            amount = int(target)
            await self.purge_all(ctx, amount)
        elif target.startswith('<@') and target.endswith('>'):
            member_id = int(target[2:-1])
            await self.purge_member(ctx, member_id, amount)
        elif target.lower() == 'word' and text:
            await self.purge_text(ctx, amount, text)
        elif target.lower() == 'human':
            await self.purge_human(ctx, amount)
        elif target.lower() == 'bot':
            await self.purge_bot(ctx, amount)
        else:
            embed = discord.Embed(
                title="Error",
                description="Invalid target specified. Use `@member`, `word`, `human`, `bot`, or a number.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=5)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to manage messages.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required arguments.*\n> - *__Command Usage:__* ```!purge <target> <amount> [text]```\n> - *__Example commands:__*\n> ```!purge 100```\n> ```!purge @member 100```\n> ```!purge word 100 hello```\n> ```!purge human 100```\n> ```!purge bot 100```",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=5)

    async def purge_member(self, ctx, member_id, amount):
        def check(m):
            return m.author.id == member_id
        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f'Deleted {len(deleted)} messages from the member.', delete_after=5)

    async def purge_text(self, ctx, amount, text):
        def check(m):
            return text in m.content
        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f'Deleted {len(deleted)} messages containing the text "{text}".', delete_after=5)

    async def purge_human(self, ctx, amount):
        def check(m):
            return not m.author.bot
        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f'Deleted {len(deleted)} human messages.', delete_after=5)

    async def purge_bot(self, ctx, amount):
        def check(m):
            return m.author.bot
        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f'Deleted {len(deleted)} bot messages.', delete_after=5)

    async def purge_all(self, ctx, amount):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f'Deleted {len(deleted)} messages.', delete_after=5)

async def setup(bot):
    await bot.add_cog(Purge(bot))
