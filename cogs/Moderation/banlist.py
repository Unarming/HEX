import discord
from discord.ext import commands
import yaml

# Load the config file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class BanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = config['owner_id']

    @commands.command(name='banlist', pass_context=True)
    async def banlist(self, ctx):
        """List all banned users."""
        if not ctx.author.guild_permissions.ban_members and ctx.author.id != self.owner_id:
            embed = discord.Embed(
                title="Permission Denied",
                description="You do not have the required permissions to use this command.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)
            return

        bans = [f"{ban.user.name}#{ban.user.discriminator} (ID: {ban.user.id})" async for ban in ctx.guild.bans()]
        if not bans:
            embed = discord.Embed(
                title="Banned Users",
                description="No users are banned.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)
            return

        pages = [bans[i:i + 6] for i in range(0, len(bans), 6)]
        view = BanListView(pages, ctx.author)
        await ctx.send(embed=view.create_embed(), view=view)

    @banlist.error
    async def banlist_error(self, ctx, error):
        """Error handler for banlist command."""
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="Error",
                description="An error occurred while trying to execute the command.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="An unexpected error occurred.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)

class BanListView(discord.ui.View):
    def __init__(self, pages, author):
        super().__init__(timeout=180)
        self.pages = pages
        self.current_page = 0
        self.author = author

    def create_embed(self):
        embed = discord.Embed(
            title="Banned Users",
            color=discord.Color.dark_gray()
        )
        description = "\n".join(
            [f"{index + 1}. Username: {ban.split(' (ID: ')[0]}\nUserID: {ban.split(' (ID: ')[1][:-1]}" for index, ban in enumerate(self.pages[self.current_page])]
        )
        embed.description = description
        embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")
        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        if self.current_page == 0:
            button.disabled = True
        self.next_button.disabled = False
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        if self.current_page == len(self.pages) - 1:
            button.disabled = True
        self.previous_button.disabled = False
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

async def setup(bot):
    await bot.add_cog(BanList(bot))