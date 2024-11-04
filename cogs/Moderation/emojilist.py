import discord
from discord.ext import commands
import yaml

# Load the config file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class EmojiList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = config['owner_id']

    @commands.command(name='emojilist', pass_context=True)
    async def emojilist(self, ctx):
        """List all custom emojis in the server."""
        if not ctx.author.guild_permissions.manage_emojis and ctx.author.id != self.owner_id:
            embed = discord.Embed(
                title="Permission Denied",
                description="You do not have the required permissions to use this command.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)
            return

        emojis = [
            f"{str(emoji)} - ```<:{emoji.name}:{emoji.id}>```" if not emoji.animated else f"{str(emoji)} - ```<a:{emoji.name}:{emoji.id}>```"
            for emoji in ctx.guild.emojis
        ]
        if not emojis:
            embed = discord.Embed(
                title="Custom Emojis",
                description="No custom emojis found.",
                color=discord.Color.dark_gray()
            )
            await ctx.send(embed=embed)
            return

        pages = [emojis[i:i + 6] for i in range(0, len(emojis), 6)]
        view = EmojiListView(pages, ctx.author)
        await ctx.send(embed=view.create_embed(), view=view)

    @emojilist.error
    async def emojilist_error(self, ctx, error):
        """Error handler for emojilist command."""
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

class EmojiListView(discord.ui.View):
    def __init__(self, pages, author):
        super().__init__(timeout=180)
        self.pages = pages
        self.current_page = 0
        self.author = author

    def create_embed(self):
        embed = discord.Embed(
            title="Custom Emojis",
            color=discord.Color.dark_gray()
        )
        description = "\n".join(
            [f"{index + 1}. {emoji}" for index, emoji in enumerate(self.pages[self.current_page])]
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
    await bot.add_cog(EmojiList(bot))
