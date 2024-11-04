import discord
from discord.ext import commands
import yaml
import os

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "autorole.yml"
        self.load_roles()

    def load_roles(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.roles = yaml.safe_load(f) or {}
        else:
            self.roles = {}

    def save_roles(self):
        with open(self.config_file, "w") as f:
            yaml.safe_dump(self.roles, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id in self.roles:
            if member.bot and "bot_role" in self.roles[guild_id]:
                role = member.guild.get_role(self.roles[guild_id]["bot_role"])
                if role:
                    await member.add_roles(role)
            elif not member.bot and "human_role" in self.roles[guild_id]:
                role = member.guild.get_role(self.roles[guild_id]["human_role"])
                if role:
                    await member.add_roles(role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def autorole(self, ctx, role_type: str, role: discord.Role):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.roles:
            self.roles[guild_id] = {}

        if role_type.lower() == "human":
            if "human_role" in self.roles[guild_id]:
                existing_role = ctx.guild.get_role(self.roles[guild_id]["human_role"])
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Already Set***",
                    description=f"> - *Human role is already set to {existing_role.mention}*",
                    color=discord.Color.dark_theme()
                )
            else:
                self.roles[guild_id]["human_role"] = role.id
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Set***",
                    description=f"> - *Human role set to {role.mention}*",
                    color=discord.Color.dark_theme()
                )
        elif role_type.lower() == "bot":
            if "bot_role" in self.roles[guild_id]:
                existing_role = ctx.guild.get_role(self.roles[guild_id]["bot_role"])
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Already Set***",
                    description=f"> - *Bot role is already set to {existing_role.mention}*",
                    color=discord.Color.dark_theme()
                )
            else:
                self.roles[guild_id]["bot_role"] = role.id
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Set***",
                    description=f"> - *Bot role set to {role.mention}*",
                    color=discord.Color.dark_theme()
                )
        else:
            embed = discord.Embed(
                title="Error",
                description="Invalid role type. Use 'human' or 'bot'.",
                color=discord.Color.red()
            )

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        self.save_roles()
        await ctx.send(embed=embed)

    @autorole.error
    async def autorole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description=(
                    "> - *Missing required argument.*\n"
                    "> - *__Command Usage:__* ```!autorole <human|bot> <@role>```\n"
                    "> - *__Example command:__* ```!autorole human @MemberRole```"
                ),
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removeautorole(self, ctx, role_type: str):
        guild_id = str(ctx.guild.id)
        if guild_id in self.roles:
            if role_type.lower() == "human" and "human_role" in self.roles[guild_id]:
                del self.roles[guild_id]["human_role"]
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Removed***",
                    description="> - *Human role removed*",
                    color=discord.Color.dark_theme()
                )
            elif role_type.lower() == "bot" and "bot_role" in self.roles[guild_id]:
                del self.roles[guild_id]["bot_role"]
                embed = discord.Embed(
                    title="> <:role:1287779049233711257> ***AutoRole Removed***",
                    description="> - *Bot role removed*",
                    color=discord.Color.dark_theme()
                )
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Invalid role type or no role set. Use 'human' or 'bot'.",
                    color=discord.Color.red()
                )
        else:
            embed = discord.Embed(
                title="Error",
                description="No autorole settings found for this server.",
                color=discord.Color.red()
            )

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        self.save_roles()
        await ctx.send(embed=embed)

    @removeautorole.error
    async def removeautorole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="> ***Error***",
                description=(
                    "> - *Missing required argument.*\n"
                    "> - *__Command Usage:__* ```!removeautorole <human|bot>```\n"
                    "> - *__Example command:__* ```!removeautorole human```"
                ),
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def viewautorole(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.roles:
            human_role_id = self.roles[guild_id].get("human_role")
            bot_role_id = self.roles[guild_id].get("bot_role")
            human_role = ctx.guild.get_role(human_role_id) if human_role_id else None
            bot_role = ctx.guild.get_role(bot_role_id) if bot_role_id else None

            embed = discord.Embed(
                title="> <:role:1287779049233711257> ***AutoRole Settings***",
                color=discord.Color.dark_theme()
            )
            embed.add_field(name="> *Human Role*", value=f"> - *{human_role.mention if human_role else 'Not set'}*", inline=False)
            embed.add_field(name="> *Bot Role*", value=f"> - *{bot_role.mention if bot_role else 'Not set'}*", inline=False)
        else:
            embed = discord.Embed(
                title="> <:role:1287779049233711257> ***AutoRole Settings***",
                description="> - *No autorole settings found for this server.*",
                color=discord.Color.red()
            )

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @viewautorole.error
    async def viewautorole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
