import discord
from discord.ext import commands
from discord.ui import Button, View
import platform
import yaml

class BotInfo(commands.Cog):
    """Cog for providing bot information."""

    def __init__(self, bot):
        self.bot = bot
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    @commands.command(name='botinfo')
    async def show_bot_info(self, ctx):
        """Displays the bot's information with a button to show system info."""
        owner = await self.bot.fetch_user(self.config['owner_id'])
        total_users = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(
            title="> <:bot:1287717874521346131> ***Bot Information***",
            description="> <a:x_dot:1260287109219225663> *Click the button below to see system information.*",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="> <:bot2:1287719055469449237> *Bot Name*", value=f"> <a:x_dot:1260287109219225663> {self.bot.user.name}", inline=True)
        embed.add_field(name="> <:id:1287719372730929193> *Bot ID*", value=f"> <a:x_dot:1260287109219225663>{self.bot.user.id}", inline=True)
        embed.add_field(name="> <:server:1287719669117227039> *Server Count*", value=f"> <a:x_dot:1260287109219225663> {len(self.bot.guilds)}", inline=True)
        embed.add_field(name="> <:users:1287719878391894037> *Total Users*", value=f"> <a:x_dot:1260287109219225663> {total_users}", inline=True)
        embed.add_field(name="> <:folder:1287720488021393449> *Total Commands*", value=f"> <a:x_dot:1260287109219225663> {len(self.bot.commands)}", inline=True)
        embed.add_field(name="> <:developer:1287720662907092992> *Developer*", value=f"> <a:x_dot:1260287109219225663> {owner.mention}", inline=True)
        embed.add_field(name="> <:python:1287720851919212695> *Python Version*", value=f"> <a:x_dot:1260287109219225663> {platform.python_version()}", inline=True)
        embed.add_field(name="> <:python:1287720851919212695> *discord.py Version*", value=f"> <a:x_dot:1260287109219225663> {discord.__version__}", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)

        button = Button(label="Show System Info", style=discord.ButtonStyle.secondary)
        button.callback = self.show_system_info

        view = View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    async def show_system_info(self, interaction: discord.Interaction):
        """Callback to show system information."""
        system_info = f"> <a:x_dot:1260287109219225663> **System Information**\n" \
                      f"> 🖥️ *Platform:* {platform.system()}\n" \
                      f"> 🔢 *Platform Version:* {platform.version()}\n" \
                      f"> 💻 *Machine:* {platform.machine()}\n" \
                      f"> ⚙️ *Processor:* {platform.processor()}"

        embed = discord.Embed(
            title="> 🖥️ ***System Information***",
            description=system_info,
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="System Information", icon_url=self.bot.user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
