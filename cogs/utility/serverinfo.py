import discord
from discord.ext import commands
import logging
from datetime import datetime
import tzlocal  # Import tzlocal

# Configure logging
logger = logging.getLogger(__name__)

class ServerInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", aliases=["server", "sinfo","si"])
    async def serverinfo(self, ctx):
        guild = ctx.guild

        logger.info(f"Server info command called by {ctx.author} in {guild.name}")

        embed = discord.Embed(title=f"{guild.name}'s Info Panel", description="", color=discord.Colour.dark_embed())
        
        # Helper function to truncate field values
        def truncate(value, max_length=1024):
            return value if len(value) <= max_length else value[:max_length-3] + '...'
        
        # About section
        about_section = (
            f"> **Server Name:** {guild.name}\n"
            f"> **Server ID:** {guild.id}\n"
            f"> **Owner:** {guild.owner.mention if guild.owner else 'N/A'}\n"
            f"> **Member Count:** {guild.member_count}\n"
            f"> **Created On:** {guild.created_at.strftime('%B %d, %Y %I:%M %p')}\n"
        )
        embed.add_field(name='> **__<:server:1264218309893554259>About Server__**', value=truncate(about_section), inline=False)
        
        # Channels section
        total_channels = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        stage_channels = len(guild.stage_channels)
        categories = len(guild.categories)
        
        channels_section = (
            f"> **Total Channels:** {total_channels}\n"
            f"> **Text Channels:** {text_channels}\n"
            f"> **Voice Channels:** {voice_channels}\n"
            f"> **Stage Channels:** {stage_channels}\n"
            f"> **Categories:** {categories}\n"
        )
        embed.add_field(name='> **__<:channel:1264219126642118788>Channels__**', value=truncate(channels_section), inline=False)
        
        # Roles section
        total_roles = len(guild.roles)
        normal_roles = len([role for role in guild.roles if not role.permissions.administrator and not role.permissions.manage_guild])
        integrated_roles = len([role for role in guild.roles if role.permissions.administrator and role.permissions.manage_guild])
        
        roles_section = (
            f"> **Total Roles:** {total_roles}\n"
            f"> **Normal Roles:** {normal_roles}\n"
            f"> **Integrated Roles:** {integrated_roles}\n"
        )
        embed.add_field(name='> **__<:roles:1264185795393097801>Roles__**', value=truncate(roles_section), inline=False)
        
        # Boost section
        boost_section = (
            f"> **Boost Level:** {guild.premium_tier}\n"
            f"> **Boost Count:** {guild.premium_subscription_count}\n"
        )
        embed.add_field(name='> **__<a:x_booster:1260559034038353971>Boosts__**', value=truncate(boost_section), inline=False)
        
        # Emoji and Sticker section
        emoji_section = (
            f"> **Total Emojis:** {len(guild.emojis)}\n"
            f"> **Total Stickers:** {len(guild.stickers)}\n"
            f"> **Animated Emojis:** {len([emoji for emoji in guild.emojis if emoji.animated])}\n"
            f"> **Normal Emojis:** {len([emoji for emoji in guild.emojis if not emoji.animated])}\n"
            
        )
        embed.add_field(name='> **__<:sticker:1264220952267325481>Emojis & Stickers__**', value=truncate(emoji_section), inline=False)
        
        # New section to display all emojis
        all_emojis = ' '.join([str(emoji) for emoji in guild.emojis])
        
        # Adjust the truncate function to avoid cutting off in the middle of an emoji
        def truncate_emojis(value, max_length=1024):
            if len(value) <= max_length:
                return value
            truncated_value = value[:max_length]
            # Ensure we don't cut off in the middle of an emoji
            if truncated_value[-1] == ' ':
                return truncated_value.strip()
            return truncated_value.rsplit(' ', 1)[0]

        # Split the emojis into multiple fields if necessary
        if len(all_emojis) > 1024:
            emoji_chunks = []
            current_chunk = ""
            for emoji in all_emojis.split(' '):
                if len(current_chunk) + len(emoji) + 1 > 1024:
                    emoji_chunks.append(current_chunk)
                    current_chunk = emoji
                else:
                    current_chunk += ' ' + emoji if current_chunk else emoji
            if current_chunk:
                emoji_chunks.append(current_chunk)
            
            for i, chunk in enumerate(emoji_chunks):
                embed.add_field(name=f'> **__<:emoji:1264220952267325481>All Emojis (Part {i+1})__**', value=f"> {chunk}", inline=False)
        else:
            embed.add_field(name='> **__<:emoji:1264220952267325481>All Emojis__**', value=f"> {all_emojis}", inline=False)
        
        # Get the local timezone and current time
        local_tz = tzlocal.get_localzone()
        embed.timestamp = datetime.now(local_tz)  # Add timestamp here
        
        # Set the bot's avatar and name
        bot_avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url
        embed.set_author(name=self.bot.user.name, icon_url=bot_avatar_url)
        
        # Set the user's avatar
        author_avatar=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        
        embed.set_thumbnail(url=author_avatar)
        
        # Add requested by in the footer
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=author_avatar)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfoCog(bot))
    logger.info("ServerInfoCog loaded")