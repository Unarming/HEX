import discord
from discord.ext import commands
from datetime import timedelta
from discord.utils import utcnow

class MuteAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='muteall')
    @commands.has_permissions(administrator=True)
    async def mute_all(self, ctx, duration: str, *, reason: str = None):
        """
        Timeout all members for a specified duration.
        Duration can be specified in seconds (s), minutes (m), hours (h), or days (d).
        """
        try:
            # Determine the duration in seconds
            time_unit = duration[-1]
            time_value = int(duration[:-1])
            if time_unit == 's':
                duration_seconds = time_value
            elif time_unit == 'm':
                duration_seconds = time_value * 60
            elif time_unit == 'h':
                duration_seconds = time_value * 3600
            elif time_unit == 'd':
                duration_seconds = time_value * 86400
            else:
                await ctx.send("Invalid time unit! Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.")
                return

            timeout_until = utcnow() + timedelta(seconds=duration_seconds)
            muted_members = []
            not_muted_members = []

            for member in ctx.guild.members:
                if not member.bot and not member.guild_permissions.administrator:
                    try:
                        await member.edit(timed_out_until=timeout_until, reason=reason)
                        muted_members.append(member)
                    except discord.Forbidden:
                        not_muted_members.append(member)
                    except Exception as e:
                        not_muted_members.append(member)
                        print(f"Failed to mute {member}: {e}")

            if len(muted_members) == 0:
                description = "> <a:x_dot:1260287109219225663> *No members were muted.*"
            else:
                description = f"> <a:x_dot:1260287109219225663> *Muted {len(muted_members)} members for {duration}.*"

            if len(not_muted_members) > 0:
                not_muted_list = ', '.join([member.mention for member in not_muted_members])
                description += f"\n> <a:x_dot:1260287109219225663> *Could not mute the following members: {not_muted_list}*"

            embed = discord.Embed(
                title="> ***ACTION: <:mute:1287274889178517524> Mute All***",
                description=description,
                color=discord.Color.dark_theme()
            )
            embed.set_footer(text=f"Command executed by {ctx.author}", icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @mute_all.error
    async def mute_all_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You do not have the `administrator` permissions to use this command.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {str(error)}",
                color=discord.Color.red()
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MuteAll(bot))
