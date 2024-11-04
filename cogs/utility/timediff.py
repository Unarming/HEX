import discord
from discord.ext import commands
from datetime import datetime
import pytz

class TimeDiff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('America/New_York')  # Set your desired time zone here

    def snowflake_time(self, snowflake):
        return datetime.utcfromtimestamp(((snowflake >> 22) + 1288834974657) / 1000).replace(tzinfo=pytz.utc).astimezone(self.timezone)

    @commands.command(name='timediff')
    async def timediff(self, ctx, message_id1: int = None, message_id2: int = None):
        """Calculate the time difference between two messages."""
        if message_id1 is None or message_id2 is None:
            if ctx.message.reference:
                replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                if message_id1 is None:
                    message_id1 = replied_message.id
                elif message_id2 is None:
                    message_id2 = replied_message.id
            else:
                await ctx.send("Please provide two message IDs or reply to a message and provide one message ID.")
                return

        try:
            time1 = self.snowflake_time(message_id1)
            time2 = self.snowflake_time(message_id2)
        except ValueError:
            await ctx.send("Invalid message IDs provided.")
            return

        time_diff = abs((time2 - time1).total_seconds())
        hours, remainder = divmod(time_diff, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(
            title="Time Difference",
            description=f"The time difference between the messages is {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.",
            color=discord.Color.dark_theme()
        )
        embed.add_field(name="Message 1", value=f"ID: {message_id1}", inline=False)
        embed.add_field(name="Message 2", value=f"ID: {message_id2}", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @timediff.error
    async def timediff_error(self, ctx, error):
        """Handle errors for the timediff command."""
        embed = discord.Embed(
            title="Error",
            description=str(error),
            color=discord.Color.dark_theme()
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot's own messages
        if message.author == self.bot.user:
            return

        # Check if the message is a DM or a message in a guild
        if isinstance(message.channel, discord.DMChannel):
            channel_type = "DM"
        elif isinstance(message.guild, discord.Guild):
            channel_type = f"Guild: {message.guild.name}"
        else:
            channel_type = "Unknown"

        # Calculate the time difference between now and when the message was created
        now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(self.timezone)
        message_time = message.created_at.replace(tzinfo=pytz.utc).astimezone(self.timezone)
        time_difference = now - message_time

        # Format the time difference to be more readable
        time_diff_str = f"{time_difference.seconds // 3600} hours, {(time_difference.seconds % 3600) // 60} minutes ago"

       

async def setup(bot):
    await bot.add_cog(TimeDiff(bot))
