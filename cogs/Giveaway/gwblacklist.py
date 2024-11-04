import discord
from discord.ext import commands
import yaml
import os

class GWBlacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklist_file = 'blacklists/gwblacklist.yml'
        self.blacklists = self.load_blacklists()

    def load_blacklists(self):
        if os.path.exists(self.blacklist_file):
            with open(self.blacklist_file, 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def save_blacklists(self):
        if not os.path.exists('blacklists'):
            os.makedirs('blacklists')
        with open(self.blacklist_file, 'w') as file:
            yaml.safe_dump(self.blacklists, file)

    def get_blacklist(self, guild_id):
        return self.blacklists.get(str(guild_id), [])

    def save_blacklist(self, guild_id, blacklist):
        self.blacklists[str(guild_id)] = blacklist
        self.save_blacklists()

    @commands.command(name="addblacklist")
    @commands.has_permissions(administrator=True)
    async def add_blacklist(self, ctx, user: discord.User):
        """Add a user to the giveaway blacklist."""
        guild_id = ctx.guild.id
        blacklist = self.get_blacklist(guild_id)
        if user.id in blacklist:
            embed = discord.Embed(
                title="User Already Blacklisted",
                description=f"{user.mention} is already in the blacklist.",
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)
            return

        blacklist.append(user.id)
        self.save_blacklist(guild_id, blacklist)
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"{user.mention} has been added to the blacklist.",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

    @commands.command(name="removeblacklist")
    @commands.has_permissions(administrator=True)
    async def remove_blacklist(self, ctx, user: discord.User):
        """Remove a user from the giveaway blacklist."""
        guild_id = ctx.guild.id
        blacklist = self.get_blacklist(guild_id)
        if user.id not in blacklist:
            embed = discord.Embed(
                title="User Not Blacklisted",
                description=f"{user.mention} is not in the blacklist.",
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)
            return

        blacklist.remove(user.id)
        self.save_blacklist(guild_id, blacklist)
        embed = discord.Embed(
            title="User Removed from Blacklist",
            description=f"{user.mention} has been removed from the blacklist.",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

    @commands.command(name="viewblacklist")
    @commands.has_permissions(administrator=True)
    async def view_blacklist(self, ctx):
        """View the giveaway blacklist."""
        guild_id = ctx.guild.id
        blacklist = self.get_blacklist(guild_id)
        if not blacklist:
            embed = discord.Embed(
                title="Blacklist",
                description="The blacklist is currently empty.",
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)
            return

        users = [f"<@{user_id}>" for user_id in blacklist]
        embed = discord.Embed(
            title="Blacklist",
            description="\n".join(users),
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GWBlacklist(bot))

