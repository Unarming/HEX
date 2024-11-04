import discord
from discord.ext import commands
import yaml

# Load configuration
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

OWNER_ID = config['owner_id']

class NoPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='noprefix', aliases=['nop'])
    async def noprefix(self, ctx, action: str = None, user: discord.User = None):
        if ctx.author.id != OWNER_ID:
            await ctx.send("You must be the bot owner to use this command.")
            return

        if not action:
            embed = discord.Embed(
                color=discord.Color.blue(),
                description="```[] = Optional Argument\n<> = Required Argument\nDo NOT type these when using commands!)```\n\n**Aliases:**\n`[nop]`\n**Usage:**\n`add/remove`"
            )
            await ctx.send(embed=embed)
            return

        action = action.lower()
        with open('noprefix.yml', 'r') as file:
            noprefix_data = yaml.safe_load(file) or {}

        if action in ['add', 'a', '+']:
            if not user:
                await ctx.reply("Provide me a valid user")
                return

            if str(user.id) in noprefix_data:
                await ctx.reply("<:cros:1260277444275863596> | This user is already in my no prefix system.")
            else:
                noprefix_data[str(user.id)] = True
                with open('noprefix.yml', 'w') as file:
                    yaml.safe_dump(noprefix_data, file)
                embed = discord.Embed(
                    color=discord.Color.green(),
                    description=f"<:tick:1260279674429505677> | Successfully **Added** {user} to my no prefix."
                )
                embed.set_footer(text=f"Added By {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                await ctx.reply(embed=embed)

        elif action in ['remove', 'r', '-']:
            if not user:
                await ctx.reply("Provide me a valid user")
                return

            if str(user.id) not in noprefix_data:
                await ctx.reply("<:cros:1260277444275863596> | This user is not present in my no prefix system.")
            else:
                del noprefix_data[str(user.id)]
                with open('noprefix.yml', 'w') as file:
                    yaml.safe_dump(noprefix_data, file)
                embed = discord.Embed(
                    color=discord.Color.red(),
                    description=f"<:tick:1260279674429505677> | Successfully **Removed** {user} from my no prefix."
                )
                embed.set_footer(text=f"Removed By {ctx.author.name}", icon_url=ctx.author.display_avatar.url )
                await ctx.reply(embed=embed)

    @noprefix.error
    async def noprefix_error(self, ctx, error):
        try:
            if isinstance(error, commands.NotOwner):
                await ctx.send("You must be the bot owner to use this command.")
            else:
                raise error
        except Exception as e:
            pass # or simply pass to suppress the output

async def setup(bot):
    await bot.add_cog(NoPrefix(bot))