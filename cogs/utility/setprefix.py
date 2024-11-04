import discord
from discord.ext import commands
import yaml
import os

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes = self.load_prefixes()

    def load_prefixes(self):
        if os.path.exists('prefixes.yml'):
            with open('prefixes.yml', 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def save_prefixes(self):
        with open('prefixes.yml', 'w') as file:
            yaml.safe_dump(self.prefixes, file)

    @commands.command(name='setprefix')
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix: str):
        self.prefixes[str(ctx.guild.id)] = prefix
        self.save_prefixes()
        await ctx.send(f"Prefix set to `{prefix}`")

    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!setprefix <new_prefix>`")
        else:
            await ctx.send("An unexpected error occurred. Please try again later.")
            print(f"Error in setprefix command: {error}")

async def setup(bot):
    await bot.add_cog(SetPrefix(bot))
