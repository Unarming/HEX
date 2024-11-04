import discord
from discord.ext import commands
import yaml

class OwnerInfo(commands.Cog):
    """Cog for providing information about the bot owner."""

    def __init__(self, bot):
        self.bot = bot
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    @commands.command(name='ownerinfo')
    async def show_owner_info(self, ctx):
        """Displays information about the bot owner."""
        owner = await self.bot.fetch_user(self.config['owner_id'])
        
        embed = discord.Embed(
            title="> <:owner:1287723926293839894> ***Owner Information***",
            description=f"> <a:x_dot:1260287109219225663> *Hello, I'm {owner.mention}. I hope you like the bot! Also, make sure to join the support server.*",
            color=discord.Color.dark_red()
        )
        embed.set_thumbnail(url=owner.display_avatar.url)
        embed.add_field(name="> <:owner:1287723926293839894> *Owner Name*", value=f"> <a:x_dot:1260287109219225663> {owner.mention}", inline=True)
        embed.add_field(name="> <:id:1287719372730929193> *Owner ID*", value=f"> <a:x_dot:1260287109219225663> {owner.id}", inline=True)
        embed.add_field(name="> <:calander:1287724281026838620> *Account Created*", value=f"> <a:x_dot:1260287109219225663> {owner.created_at.strftime('%Y-%m-%d %H:%M:%S')}", inline=True)
        embed.add_field(name="> <:link:1287724627241603163> *Bot Invite Link*", value=f"> <a:x_dot:1260287109219225663> [Click here to invite the bot]({self.config['bot_invite_link']})", inline=False)
        embed.add_field(name="> <:link:1287724627241603163> *Support Server*", value=f"> <a:x_dot:1260287109219225663> [Join Support Server]({self.config['support_link']})", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OwnerInfo(bot))
