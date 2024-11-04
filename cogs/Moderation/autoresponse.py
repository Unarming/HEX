import discord
from discord.ext import commands
import yaml
import os

class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = self.load_responses()  # Load responses from YAML file

    def load_responses(self):
        if os.path.exists('response.yml'):
            with open('response.yml', 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def save_responses(self):
        with open('response.yml', 'w') as file:
            yaml.safe_dump(self.responses, file)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
 
    async def autoresponse(self, ctx):
        embed = discord.Embed(title="Auto Response Setup", description="Click the button below to set up an auto-response .\n You can alos set Embeded autoresponse")
        view = AutoResponseView(self, ctx.author)
        await ctx.send(embed=embed, view=view)

    @autoresponse.error
    async def autoresponse_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} does not have `Manage Messages` permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)

    @commands.command(aliases=['lar'])
    @commands.has_permissions(manage_messages=True)
    async def listautoresponses(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.responses or not self.responses[guild_id]:
            await ctx.send("No auto-responses have been set.")
            return

        embed = discord.Embed(title="Auto Responses", description="List of auto-responses set for this guild.")
        for trigger, response in self.responses[guild_id].items():
            embed.add_field(
                name=f"Trigger: {trigger}",
                value=f"Response: {response['message']}\nEmbed: {response['embed']}\nSet by: {response['author']}",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @listautoresponses.error
    async def listautoresponses_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} does not have `Manage Messages` permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.responses:
            return

        for trigger, response in self.responses[guild_id].items():
            if trigger in message.content:
                if response['embed']:
                    embed = discord.Embed(description=response['message'])
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(response['message'])
                break

class AutoResponseView(discord.ui.View):
    def __init__(self, cog, author):
        super().__init__(timeout=180)
        self.cog = cog
        self.author = author

    @discord.ui.button(label="Set Auto Response", style=discord.ButtonStyle.secondary)
    async def set_response(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(AutoResponseModal(self.cog))
        except Exception as e:
            await interaction.response.send_message(f"Failed to open the modal: {str(e)}", ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return False
        return True

class AutoResponseModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="Set Auto Response")
        self.cog = cog
        self.trigger_word = discord.ui.TextInput(label="Trigger Word", placeholder="Enter the trigger word")
        self.response_message = discord.ui.TextInput(label="Response Message", placeholder="Enter the response message", style=discord.TextStyle.paragraph, max_length=4000)
        self.embed_switch = discord.ui.TextInput(label="Embed (yes/no)", placeholder="Enter 'yes' for embed, 'no' otherwise")
        self.add_item(self.trigger_word)
        self.add_item(self.response_message)
        self.add_item(self.embed_switch)

    async def on_submit(self, interaction: discord.Interaction):
        trigger = self.trigger_word.value
        guild_id = str(interaction.guild.id)
        if guild_id not in self.cog.responses:
            self.cog.responses[guild_id] = {}

        if trigger in self.cog.responses[guild_id]:
            await interaction.response.send_message(f"The trigger word '{trigger}' already has an auto-response set.", ephemeral=True)
            return

        message = self.response_message.value
        embed = self.embed_switch.value.lower() == 'yes'
        self.cog.responses[guild_id][trigger] = {'message': message, 'embed': embed, 'author': str(interaction.user)}
        self.cog.save_responses()  # Save responses to YAML file
        await interaction.response.send_message(f"Auto-response set for trigger '{trigger}'", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutoResponse(bot))
