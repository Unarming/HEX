import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument

class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role", aliases=["r", "giverole"])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, target: discord.Member, role: discord.Role):
        """Give a role to a member."""
        await target.add_roles(role)
        embed = discord.Embed(
            title="> <:role:1287779049233711257> ***Role Assigned***",
            description=f"> *Successfully assigned {role.mention} to {target.mention}.*",
            color=discord.Color.dark_theme()
        )
        await ctx.send(embed=embed)

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__Command Usage:__* ```!role <member> <role>```\n> - *__Example command:__* ```!role @user Member```\n> - *__Aliases:__* ```r```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="removerole", aliases=["rr", "removerolefrommember"])
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, target: discord.Member, role: discord.Role):
        """Remove a role from a member."""
        await target.remove_roles(role)
        embed = discord.Embed(
            title="> <:role:1287779049233711257> *Role Removed*",
            description=f"> *Successfully removed {role.mention} from {target.mention}.*",
            color=discord.Color.dark_theme()
        )
        await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__Command Usage:__* ```!removerole <member> <role>```\n> - *__Example command:__* ```!removerole @user Member```\n> - *__Aliases:__* ```rr```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="assignrole", aliases=["ar", "giveroletoall"])
    @commands.has_permissions(manage_roles=True)
    async def assignrole(self, ctx, target_role: discord.Role, role: discord.Role):
        """Give a role to all members with a certain role."""
        members_with_role = [member for member in ctx.guild.members if target_role in member.roles]
        for member in members_with_role:
            await member.add_roles(role)
        embed = discord.Embed(
            title="> <:role:1287779049233711257> ***Role Assigned***",
            description=f"> *Successfully assigned {role.mention} to all members with the {target_role.mention} role.*",
            color=discord.Color.dark_theme()
        )
        await ctx.send(embed=embed)

    @assignrole.error
    async def assignrole_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__Command Usage:__* ```!assignrole <target_role> <role>```\n> - *__Example command:__* ```!assignrole @Role Member```\n> - *__Aliases:__* ```ar```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="removeassignrole", aliases=["rar", "removerolefromall"])
    @commands.has_permissions(manage_roles=True)
    async def removeassignrole(self, ctx, target_role: discord.Role, role: discord.Role):
        """Remove a role from all members with a certain role."""
        members_with_role = [member for member in ctx.guild.members if target_role in member.roles]
        for member in members_with_role:
            await member.remove_roles(role)
        embed = discord.Embed(
            title="> <:role:1287779049233711257> ***Role Removed***",
            description=f"> *Successfully removed {role.mention} from all members with the {target_role.mention} role.*",
            color=discord.Color.dark_theme()
        )
        await ctx.send(embed=embed)

    @removeassignrole.error
    async def removeassignrole_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *Missing required argument.*\n> - *__Command Usage:__* ```!removeassignrole <target_role> <role>```\n> - *__Example command:__* ```!removeassignrole @Role Member```\n> - *__Aliases:__* ```rar```",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="> ***Error***",
                description="> - *You don't have ``Manage role`` permission to use this command.*",
                color=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RoleCog(bot))
