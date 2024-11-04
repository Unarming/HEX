import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason provided"
        
        # Check if the member to be kicked has a higher role than the author
        if member.top_role >= ctx.author.top_role:
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention}, you cannot kick a member with an equal or higher role.",
                color=discord.Color.brand_red()
            )
            return await ctx.send(embed=error_embed)

        # Check if the member to be kicked has a higher role than the bot
        if member.top_role >= ctx.me.top_role:
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.me.mention} cannot kick a member with an equal or higher role.",
                color=discord.Color.brand_red()
            )
            return await ctx.send(embed=error_embed)

        # Create an embed message
        embed = discord.Embed(
            title="> ***ACTION: KICK***",
            description=f"> <a:x_dot:1260287109219225663> *{member.mention} has been kicked from the server.*",
            color=discord.Color.dark_theme()  # Dark theme color
        )
        embed.add_field(name="> <:reason:1287280377731223593> ***Reason***", value=f"> <a:x_dot:1260287109219225663> {reason}", inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        # Send a DM to the user being kicked
        try:
            dm_embed = discord.Embed(
                title="You have been kicked",
                description=f"You have been kicked from {ctx.guild.name}.",
                color=discord.Color.dark_theme()
            )
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await member.send(embed=dm_embed)
            dm_status = f"> <:tick:1287282967517073511> *DM successfully sent to {member.mention}.*"
        except discord.Forbidden:
            dm_status = f"> <:cross:1287283014178570282> *Could not send DM to {member.mention}.*"

        embed.add_field(name="> <:dm:1287281448209879061> ***DM Status***", value=dm_status, inline=False)
        
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__Command Usage:__* ```!kick <member> [reason]```\n> - *__Example command:__* ```!kick @user reason```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)
        elif isinstance(error, MissingPermissions):
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} does not have ``Kick member`` permission to use this command.",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Kick(bot))