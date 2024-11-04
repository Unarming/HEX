import discord
from discord.ext import commands, tasks
import yaml
import asyncio
from datetime import datetime
import tzlocal
import aiohttp

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

TOKEN = config["token"]
DEFAULT_PREFIX = config["prefix"]
BOT_INVITE_LINK = config["bot_invite_link"]
SUPPORT_LINK = config["support_link"]
BOT_OWNER_ID = config["owner_id"]

def get_prefix(bot, message):
    if not message.guild:
        return DEFAULT_PREFIX
    with open('prefixes.yml', 'r') as file:
        prefixes = yaml.safe_load(file) or {}
    return prefixes.get(str(message.guild.id), DEFAULT_PREFIX)

intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')  # Remove the default help command

initial_extension = [
    "cogs.utility.setprefix",
    "cogs.utility.help",
    "cogs.utility.avatar",
    "cogs.utility.userinfo",
    "cogs.utility.timediff",
    "cogs.utility.serverinfo",
    "cogs.utility.servericon",
    "cogs.noprefix",
    "cogs.Moderation.ban",
    "cogs.Moderation.unban",
    "cogs.Moderation.nuke",
    "cogs.Moderation.mute",
    'cogs.Moderation.unmute',
    "cogs.Moderation.kick",
    "cogs.Moderation.nick",
    "cogs.Moderation.purge",
    "cogs.Giveaway.gwblacklist",
    "cogs.Moderation.hide",
    "cogs.Moderation.unhide",
    "cogs.Moderation.lock",
    "cogs.Moderation.unlock",
    "cogs.info.botinfo",
    "cogs.info.owner",
    "cogs.utility.remind",
    "cogs.Moderation.role",
    "cogs.Moderation.autorole",
    "cogs.Moderation.autoresponse",
    "cogs.Moderation.unbanall",
    "cogs.Moderation.banlist",
    "cogs.Moderation.emojilist",
    "cogs.Moderation.unmuteall",
    "cogs.Moderation.muteall"
    
    
    
    
   
]

async def load_extensions():
    for extension in initial_extension:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    log_channel_id = config.get("log_channel_id")
    if log_channel_id:
        log_channel = bot.get_channel(log_channel_id)
        if log_channel is None:
            print("Log channel not found. Please check the log_channel_id in config.yml.")
    else:
        print("log_channel_id not set in config.yml.")
    
    # Fetch bot owner name using their ID
    bot_owner = await bot.fetch_user(BOT_OWNER_ID)
    bot_owner_name = bot_owner.name

    # Start the task to update rich presence
    update_presence.start(bot_owner_name)

@tasks.loop(seconds=60)
async def update_presence(bot_owner_name):
    # Alternate between two statuses
    update_presence.counter += 1
    if update_presence.counter % 2 == 0:
        activity = discord.Activity(type=discord.ActivityType.listening, name=bot_owner_name)
    else:
        activity = discord.Activity(type=discord.ActivityType.listening, name=f"{DEFAULT_PREFIX}help")
    await bot.change_presence(activity=activity)

# Initialize the counter
update_presence.counter = 0

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Load no-prefix users from YAML file
    with open('noprefix.yml', 'r') as file:
        noprefix_data = yaml.safe_load(file) or {}

    # Check if the user is in the no-prefix list
    if str(message.author.id) in noprefix_data:
        # Attempt to process the message directly as a command
        ctx = await bot.get_context(message, cls=commands.Context)
        
        if ctx.command:
            await bot.invoke(ctx)
            return

        # If no command is found, check if adding the default prefix would work
        original_content = message.content
        message.content = f"{DEFAULT_PREFIX}{message.content}"
        ctx = await bot.get_context(message, cls=commands.Context)
        
        if ctx.command:
            await bot.invoke(ctx)
            return
        else:
            # Restore original content if no command is found
            message.content = original_content
    else:
        # If not in the no-prefix list, process as a normal message
        await bot.process_commands(message)

    # Check if the bot was mentioned
    if bot.user in message.mentions and not message.mention_everyone and not message.reference:
        guild_prefix = get_prefix(bot, message)
        local_timezone = tzlocal.get_localzone()

        embed = discord.Embed(
            title=f"> ***{bot.user.name} Prefix***",
            description=f"> - **__Default Prefix__:** `{DEFAULT_PREFIX}`\n> - **__Guild Prefix__:** `{guild_prefix}`\n\n> - **__Bot Invite Link__:** [Click here]({BOT_INVITE_LINK})\n> - **__Support Server__:** [Click here]({SUPPORT_LINK})",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(local_timezone)
        )
        embed.set_footer(
            text="Prefix Information",
            icon_url=bot.user.display_avatar.url if bot.user.display_avatar else bot.user.default_avatar_url
        )
        await message.channel.send(embed=embed)

async def main():
    async with aiohttp.ClientSession() as session:
        bot.session = session
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())