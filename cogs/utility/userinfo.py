import discord
from discord.ext import commands
from datetime import datetime
import tzlocal  # Import tzlocal
import emoji  # Import the emoji library

class UserInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["user","ui", "uinfo"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(title=f"> {member.mention}'s Info Panel", color=discord.Color.dark_theme())
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=ctx.guild.name, icon_url=self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url)

        # About section
        badges = [flag for flag, value in member.public_flags if value]
        badge_emojis = {
            "staff": "<:staff:1264164482142179338>",
            "partner": "<a:partner:1259855438527074315>",
            "hypesquad": "<a:hypersquad:1260929102513311888>",
            "bug_hunter": "<:BugHunter:1264165688117825589>",
            "hypesquadbravery": "<:Bravery:1264166288826302536>",
            "hypesquad_brilliance": "<:brilliance:1264166453385629748>",
            "hypesquad_balance": "<:hypesquadbalance:1264166329016123472>",
            "Booster": "<a:x_booster:1260559034038353971>",
            "Nitro": "<:nitro:1264167128752193619>",
            "active_developer": "<:ActiveDeveloperBadge:1260931702872735768>"
        }
        badge_display = [emoji.emojize(badge_emojis.get(badge, badge)) for badge in badges]
        about_value = (
            f"> **Default Name:** {member.name}\n"
            f"> **Global Name:** {member.global_name or 'None'}\n"
            f"> **Mention:** {member.mention}\n"
            f"> **ID:** {member.id}\n"
            f"> **Badges:** {' '.join(badge_display) if badge_display else 'None'}\n"
            f"> **Account Created:** {member.created_at.strftime('%B %d, %Y %I:%M %p')}\n"
            f"> **Server Joined:** {member.joined_at.strftime('%B %d, %Y %I:%M %p')}\n"
        )
        embed.add_field(name="> <:about:1264185235592183839>**__About__**", value=about_value, inline=False)

        # Roles section
        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        roles_value = (
            f"> **Total Roles:** {len(roles)}\n"
            f"> **Roles:** {', '.join(roles) if roles else 'Member Has No Roles'}"
        )
        embed.add_field(name="> <:roles:1264185795393097801>**__Roles__**", value=roles_value, inline=False)

        # Permissions section
        permissions = [perm[0].replace('_', ' ').title() for perm in member.guild_permissions if perm[1]]
        permissions_value = ", ".join(permissions) if permissions else "None"
        embed.add_field(name="> <:ke:1264186264786305046>**__Permissions__**", value=f"> {permissions_value}", inline=False)

        # Get the local timezone and current time
        local_tz = tzlocal.get_localzone()
        embed.timestamp = datetime.now(local_tz)  # Add timestamp here
        author_avatar=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=author_avatar)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfoCog(bot))