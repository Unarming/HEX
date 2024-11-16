import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime
import asyncio

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban',aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        # Check if the member to be banned has a higher role than the author
        if member.top_role >= ctx.author.top_role:
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention}, you cannot ban a member with an equal or higher role.",
                color=discord.Color.brand_red()
            )
            return await ctx.send(embed=error_embed)

        # Check if the member to be banned has a higher role than the bot
        if member.top_role >= ctx.me.top_role:
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.me.mention} cannot ban a member with an equal or higher role.",
                color=discord.Color.brand_red()
            )
            return await ctx.send(embed=error_embed)

        # Check if the bot has the required permissions
        if not ctx.guild.me.guild_permissions.ban_members:
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.me.mention} does not have ``Ban member`` permission to ban members.",
                color=discord.Color.brand_red()
            )
            return await ctx.send(embed=error_embed)

       
        embed = discord.Embed(
            title="> ***ACTION: <:ban:1287274889178517524> BAN***",
            description=f"> <a:x_dot:1260287109219225663> *{member.mention} has been banned.*",
            color=discord.Color.dark_theme()
        )
        embed.add_field(name="> <:reason:1287280377731223593> ***Reason***", value=f"> <a:x_dot:1260287109219225663> *{reason}*", inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)  # Thumbnail of the muted member

        # Send a DM to the user being banned
        try:
            dm_embed = discord.Embed(
                title="You have been banned",
                description=f"You have been banned from {ctx.guild.name}.",
                color=discord.Color.dark_theme()
            )
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.set_footer(text=f"Banned by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await member.send(embed=dm_embed)
            dm_status = f"> <:tick:1287282967517073511> *DM successfully sent to {member.mention}.*"
        except discord.Forbidden:
            dm_status = f"> <:cross:1287283014178570282> *Could not send DM to {member.mention}.*"

        embed.add_field(name="> <:dm:1287281448209879061> ***DM Status***", value=dm_status, inline=False)
        embed.set_footer(text=f"Banned by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        
        # Ban the user
        await member.ban(reason=reason)
        
        # Create an Unban button
        unban_button = Button(label="Unban", style=discord.ButtonStyle.secondary)

        async def unban_callback(interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("> **Only the person who used the command can use this button.**", ephemeral=True)
                return

            class UnbanReasonModal(Modal):
                def __init__(self, member):
                    super().__init__(title="Unban Reason")
                    self.member = member
                    self.add_item(TextInput(label="Reason", placeholder="Enter the reason for unbanning", max_length=200, required=False))

                async def on_submit(self, interaction):
                    reason = self.children[0].value or "No reason provided"
                    try:
                        await interaction.guild.unban(self.member, reason=reason)
                        await interaction.response.send_message(f"{self.member} has been unbanned for: {reason}", ephemeral=True)
                        
                        # Send direct message to the unbanned user
                        try:
                            dm_embed = discord.Embed(
                                title="> **__You have been unbanned__**",
                                description=f"> **You have been unbanned from {interaction.guild.name}**",
                                color=discord.Color.green()
                            )
                            dm_embed.add_field(name="> **__Reason__:**", value=reason, inline=False)
                            dm_embed.set_footer(text=f"Unbanned by {interaction.user}", icon_url=interaction.user.avatar.url)
                            dm_embed.timestamp = datetime.utcnow()
                            await self.member.send(embed=dm_embed)

                            # Create an invite link and send it to the unbanned user
                            invite = await interaction.guild.text_channels[0].create_invite(max_age=3600, max_uses=1)
                            await self.member.send(f"Here is your invite link to rejoin the server: {invite.url}")
                        except discord.errors.HTTPException as e:
                            if e.code == 50007:
                                await interaction.response.send_message("Cannot send messages to this user.", ephemeral=True)
                            else:
                                raise e
                    except discord.errors.NotFound:
                        await interaction.response.send_message(f"{self.member} is not banned.", ephemeral=True)

            await interaction.response.send_modal(UnbanReasonModal(member))
            for item in view.children:
                item.disabled = True
            await message.edit(view=view)

        unban_button.callback = unban_callback

        view = View()
        view.add_item(unban_button)

        # Send embed message to the channel with the unban button
        message = await ctx.send(embed=embed, view=view)

        # Wait for 30 seconds
        await asyncio.sleep(30)
        for item in view.children:
            item.disabled = True
        await message.edit(view=view)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__command Usage:__* ```!ban <member> [reason]```\n> - *__Example command:__* ```!ban @shankar fuckoff```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)
        elif isinstance(error, MissingPermissions):
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} does not have  ``Ban member`` permission to use this command.",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Ban(bot))