import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
import yaml
import os

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "remind.yml"
        self.load_reminders()

    def load_reminders(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.reminders = yaml.safe_load(f) or {}
        else:
            self.reminders = {}

    def save_reminders(self):
        with open(self.config_file, "w") as f:
            yaml.safe_dump(self.reminders, f)

    @commands.command(name='remind')
    async def remind(self, ctx, time: str, *, message: str):
        # Parse time
        time_unit = time[-1]
        time_value = int(time[:-1])
        if time_unit == 's':
            delay = timedelta(seconds=time_value)
        elif time_unit == 'm':
            delay = timedelta(minutes=time_value)
        elif time_unit == 'h':
            delay = timedelta(hours=time_value)
        elif time_unit == 'd':
            delay = timedelta(days=time_value)
        else:
            await ctx.send("Invalid time format. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days.")
            return

        # Determine the type of reminder
        if message.startswith('<@&'):  # Role mention
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("You don't have ``Manage role`` permission to set role reminders.")
                return
            role_id = int(message.split()[0][3:-1])
            role = ctx.guild.get_role(role_id)
            reminder_message = ' '.join(message.split()[1:])
            await self.set_reminder(ctx, delay, role=role, message=reminder_message, time_str=time)
        elif message.startswith('<@!'):  # Member mention
            if not ctx.author.guild_permissions.manage_messages:
                await ctx.send("You don't have ``Manage message`` permission to set reminders for other members.")
                return
            member_id = int(message.split()[0][3:-1])
            member = ctx.guild.get_member(member_id)
            reminder_message = ' '.join(message.split()[1:])
            await self.set_reminder(ctx, delay, member=member, message=reminder_message, time_str=time)
        else:  # User reminder
            await self.set_reminder(ctx, delay, message=message, time_str=time)

    async def set_reminder(self, ctx, delay, role=None, member=None, message=None, time_str=None):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.reminders:
            self.reminders[guild_id] = []

        reminder_data = {
            "time": time_str,
            "message": message,
            "role_id": role.id if role else None,
            "member_id": member.id if member else None,
            "author_id": ctx.author.id,
            "timestamp": (datetime.now() + delay).timestamp()
        }
        self.reminders[guild_id].append(reminder_data)
        self.save_reminders()

        # Send confirmation as an embed
        confirmation_embed = discord.Embed(
            title="> <:remind:1287763715084779635> ***Reminder Set***",
            description=f"> *Reminder set for {time_str}.*",
            color=discord.Color.dark_theme()
        )
        confirmation_embed.add_field(name="> <:message:1287280356881469521> ***Content***", value=f"> <a:x_dot:1260287109219225663> *{message}*", inline=False)
        confirmation_embed.set_footer(text="Use the remind command to set more reminders.")
        await ctx.send(embed=confirmation_embed)
        
        await asyncio.sleep(delay.total_seconds())
        
        # Send the actual reminder as an embed
        reminder_embed = discord.Embed(
            title="> <:remind:1287763715084779635> ***It's Time!***",
            description=f"> <a:x_dot:1260287109219225663> *Don't forget: {message}*",
            color=discord.Color.dark_theme()
        )
        
        if role:
            await ctx.send(content=role.mention, embed=reminder_embed)
        elif member:
            await ctx.send(content=member.mention, embed=reminder_embed)
        else:
            await ctx.send(content=ctx.author.mention, embed=reminder_embed)

        # Remove the reminder from the YAML file
        self.reminders[guild_id].remove(reminder_data)
        if not self.reminders[guild_id]:
            del self.reminders[guild_id]
        self.save_reminders()

    @remind.error
    async def remind_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description=(
                    "> - *Missing required argument.*\n"
                    "> - *__Command Usage:__* ```!remind <time> <message>```\n"
                    "> - *__Example commands:__* \n"
                    "```!remind 10s I have work to do```\n"
                    "```!remind 5m @role You have work to do```\n"
                    "```!remind 1h @member You have work to do```"
                ),
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Remind(bot))