import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from datetime import datetime
import tzlocal
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
    bot_invite_link = config.get('bot_invite_link')
    support_link = config.get('support_link')

class HelpSelect(Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options = [
            discord.SelectOption(emoji="<:utility:1286907058276274208>", label=" - Utility", value="1", description="Get all commands according to 'Utility'"),
            discord.SelectOption(emoji="<:info:1286907281006661695>", label=" - Info", value="2", description="Get all commands according to 'Info'"),
            discord.SelectOption(emoji="<:moderation:1286907675703246912>", label=" - Moderation", value="3", description="Get all commands according to 'Moderation'"),
            discord.SelectOption(emoji="<:fun:1286906229267894293>", label=" - Fun", value="4", description="Get all commands according to 'Fun'"),
            discord.SelectOption(emoji="<:gift:1286976114912395295>", label=" - Giveway", value="5", description="Get all commands according to 'Giveway'"),
            discord.SelectOption(emoji="<:mic:1286909127083429958>", label=" - Voice", value="6", description="Get all commands according to 'Voice'"),
            discord.SelectOption(emoji="<:log:1286910312070778890>", label=" - Logger", value="7", description="Get all commands according to 'Logger'"),
            discord.SelectOption(emoji="<a:cancel:1076294664094744626>", label=" - Cancel", value="Cancel", description="Cancel this interaction.")
        ]
        super().__init__(placeholder="Select a category", options=options)
    
    local_timezone = tzlocal.get_localzone()
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)
            return

        await interaction.response.defer()  # Defer the interaction

        if self.values[0] == "Cancel":
            await interaction.followup.send("Interaction cancelled.", ephemeral=True) 
            if self.view and self.view.message:
                await self.view.message.delete()  # Delete the message after cancellation
            return

        embed = None
        if self.values[0] == "1":
            embed = discord.Embed(
                title="<:utility:1286907058276274208> Utility Commands",
                description="Here are the Utility commands:\n `help, setprefix, avatar, serverinfo, userinfo, timediff,servericon`",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "2":
            embed = discord.Embed(
                title="<:info:1286907281006661695> Info Commands",
                description="Here are the Info commands:\n `botinfo, ownerinfo`",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "3":
            embed = discord.Embed(
                title="<:moderation:1286907675703246912> Moderation Commands",
                description="Here are the moderation commands:\n `ban, unban, mute, unmute, purge, nick, kick, nuke, hide, unhide, lock,unlock, autoresponse, listautoresponses, role, assignrole, autorole, viewautorole, removeautorole`",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "4":
            embed = discord.Embed(
                title="<:fun:1286906229267894293> Fun Commands",
                description="Here are the Fun commands.",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "5":
            embed = discord.Embed(
                title="<:gift:1286976114912395295> Giveway Commands",
                description="Here are the Giveway commands.",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "6":
            embed = discord.Embed(
                title="<:mic:1286909127083429958> Voice Commands",
                description="Here are the Voice commands.",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )
        elif self.values[0] == "7":
            embed = discord.Embed(
                title="<:log:1286910312070778890> Logger Commands",
                description="Here are the Logger commands.",
                color=discord.Color.dark_theme(),
                timestamp=datetime.now(self.local_timezone)  # Add timestamp here
            )

        if embed:
            await interaction.edit_original_response(embed=embed)

class UtilityButton(Button):
    def __init__(self):
        super().__init__(emoji="<:utility:1286907058276274208>", label="Utility", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:utility:1286907058276274208> Utility Commands",
            description="Here are the Utility commands:\n `help, setprefix, avatar, serverinfo, userinfo, timediff,servericon`",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class InfoButton(Button):
    def __init__(self):
        super().__init__(emoji="<:info:1286907281006661695>", label="Info", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:info:1286907281006661695> Info Commands",
            description="Here are the Info commands:\n `botinfo, ownerinfo`",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class ModerationButton(Button):
    def __init__(self):
        super().__init__(emoji="<:moderation:1286907675703246912>", label="Moderation", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:moderation:1286907675703246912> Moderation Commands",
            description="Here are the moderation commands:\n `ban, unban, mute, unmute, purge, nick, kick, nuke, hide, unhide, lock,unlock, autoresponse, listautoresponses, role, assignrole, autorole, viewautorole, removeautorole`",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class FunButton(Button):
    def __init__(self):
        super().__init__(emoji="<:fun:1286906229267894293>", label="Fun", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:fun:1286906229267894293> Fun Commands",
            description="Here are the Fun commands.",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class GivewayButton(Button):
    def __init__(self):
        super().__init__(emoji="<:gift:1286976114912395295>", label="Giveway", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:gift:1286976114912395295> Giveway Commands",
            description="Here are the Giveway commands.",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class VoiceButton(Button):
    def __init__(self):
        super().__init__(emoji="<:mic:1286909127083429958>", label="Voice", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:mic:1286909127083429958> Voice Commands",
            description="Here are the Voice commands.",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class LoggerButton(Button):
    def __init__(self):
        super().__init__(emoji="<:log:1286910312070778890>", label="Logger", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="<:log:1286910312070778890> Logger Commands",
            description="Here are the Logger commands.",
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class ShowAllCommandsButton(Button):
    def __init__(self):
        super().__init__(emoji="<a:emoji_1724051862957:1274990666522427393>", label="Show All Commands", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction
        embed = discord.Embed(
            title="All Commands",
            description=(
                f"**<:utility:1286907058276274208> Utility Commands:**\n `help, setprefix, avatar, serverinfo, userinfo, timediff,servericon`\n\n"
                f"**<:info:1286907281006661695> Info Commands:**\n `botinfo, ownerinfo`\n\n"
                f"**<:moderation:1286907675703246912> Moderation Commands: **\n `ban, unban, mute, unmute, purge, nick, kick, nuke, hide, unhide, lock,unlock, autoresponse, listautoresponses, role, assignrole, autorole, viewautorole, removeautorole`\n\n"
                f"**<:fun:1286906229267894293> Fun Commands:**\n\n"
                f"**<:gift:1286976114912395295> Giveway Commands:**\n\n"
                f"**<:mic:1286909127083429958> Voice Commands:**\n\n"
                f"**<:log:1286910312070778890> Logger Commands:**\n"
            ),
            color=discord.Color.dark_theme(),
            timestamp=datetime.now(tzlocal.get_localzone())
        )
        await interaction.edit_original_response(embed=embed)

class HelpView(View):
    def __init__(self, user_id):
        super().__init__(timeout=60)  # Set timeout to 60 seconds
        self.user_id = user_id
        self.message = None
        self.add_item(HelpSelect(user_id))
        self.add_item(UtilityButton())
        self.add_item(InfoButton())
        self.add_item(ModerationButton())
        self.add_item(FunButton())
        self.add_item(GivewayButton())
        self.add_item(VoiceButton())
        self.add_item(LoggerButton())
        self.add_item(ShowAllCommandsButton())  # Add the new button here

    async def on_timeout(self):
        if self.message:
            await self.message.delete()  # Delete the message after timeout

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["H",'Help'])
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help Menu",
            description="Select a category to get help on specific commands.",
            color=discord.Color.dark_magenta(),  # Change color to dark magenta
            timestamp=datetime.now(tzlocal.get_localzone())  # Add timestamp here
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.add_field(name="> <:module:1286905875583340544> **__Modules__**", value=f"> <:utility:1286907058276274208> **Utility**\n> <:info:1286907281006661695> **Info**\n> <:moderation:1286907675703246912> **Moderation**\n> <:fun:1286906229267894293> **Fun**\n> <:gift:1286976114912395295> **Giveway**\n> <:mic:1286909127083429958> **Voice**\n> <:log:1286910312070778890> **Logger**", inline=False)
        embed.add_field(name="> <:link:1272223658894557259>***__Links__***", value=f"> <:bot:1272222775242784809> ***[Invite Bot]({bot_invite_link})***\n> <:support:1272223139925065801> ***[Support Server]({support_link})***", inline=False)
        embed.set_footer(text="Use the dropdown menu below to select a category.")

        view = HelpView(ctx.author.id)
        message = await ctx.send(embed=embed, view=view)  # Send the help menu directly
        view.message = message  # Store the message object in the view for later editing

async def setup(bot):
    await bot.add_cog(Help(bot))