import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
import datetime

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason=None):
        if reason is None:
            reason = "No Reason Provided"
        
        await ctx.guild.unban(member, reason=reason)
        
        # Create embed for unban notification
        embed = discord.Embed(
            title="> ***ACTION: <:unban:1287274889178517524> UNBAN***",
            description=f"> <a:x_dot:1260287109219225663> *{member.mention} has been unbanned.*",
            color=discord.Color.dark_theme()
        )
        embed.add_field(name="> <:reason:1287280377731223593> ***Reason***", value=f"> <a:x_dot:1260287109219225663> *{reason}*", inline=False)
        embed.set_footer(text=f"Unbanned by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        
        # Send DM to the unbanned user with an invite link
        invite = await ctx.channel.create_invite(max_uses=1, unique=True)
        try:
            dm_embed = discord.Embed(
                title="> **__You have been unbanned__**",
                description=f"> **You have been unbanned from {ctx.guild.name}**",
                color=discord.Color.dark_theme()
            )
            dm_embed.add_field(name="> **__Reason__:**", value=reason, inline=False)
            dm_embed.set_footer(text=f"Unbanned by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            dm_embed.timestamp = datetime.datetime.utcnow()
            await member.send(embed=dm_embed)
            await member.send(f"Here is your invite link to rejoin the server: {invite.url}")
            dm_status = f"> <:tick:1287282967517073511> *DM successfully sent to {member.mention}.*"
        except discord.Forbidden:
            dm_status = f"> <:cross:1287283014178570282> *Could not send DM to {member.mention}.*"
        
        embed.add_field(name="> <:dm:1287281448209879061> ***DM Status***", value=dm_status, inline=False)
        
        await ctx.send(embed=embed)
        await ctx.message.delete() 
        
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_embed = discord.Embed(
                title="> ***Error***",
                description=f"> {ctx.author.mention}, you do not have ``Ban member`` permission to use this command.",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)
        elif isinstance(error, MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description=f"> - *{ctx.author.mention}, missing required argument.*\n> - *command Usage:__* ```!unban <member> [reason]```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="> ***Error***",
                description=f"> An unexpected error occurred: {str(error)}",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Unban(bot))
