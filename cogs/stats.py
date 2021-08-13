import discord
from discord.ext import commands, tasks
import platform
import psutil
import time
import datetime
import os
from fuzzywuzzy import process


#
#this here is home to the various stats commands about users, roles or the bot
#


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #some basic info about a role
    @commands.command()
    async def roleinfo(self, ctx, *,input_role):
        unwanted = ['<','@','>', '&']
        for i in unwanted:
            input_role = input_role.replace(i,'')
        all_roles = []

        for role in ctx.guild.roles:
            all_roles.append(role.name)
        try:
            role = discord.utils.get(ctx.guild.roles, id=int(input_role))
        except:
            match = process.extractOne(input_role, all_roles, score_cutoff=30)[0]
            role = discord.utils.get(ctx.guild.roles, name=match)

        #the above block searches all roles for the closest match, as seen in the admin cog

        embed = discord.Embed(title=f"Roleinfo of {role.name} ({role.id})", color = role.colour)
        embed.add_field(name="Role Name:", value=role.mention, inline=True)
        embed.add_field(name="Users with role:", value=len(role.members), inline=True)
        embed.add_field(name="Created at:", value=discord.utils.format_dt(role.created_at, style='F'))
        embed.add_field(name="Mentionable:", value=role.mentionable, inline=True)
        embed.add_field(name="Displayed Seperately:", value=role.hoist, inline=True)
        embed.add_field(name="Color:", value=role.color, inline=True)
        await ctx.send(embed=embed)

    #lists every member in the role if there arent more than 60 members, to prevent spam
    @commands.command(aliases=['listroles']) 
    async def listrole(self, ctx, *,input_role):
        unwanted = ['<','@','>', '&']
        for i in unwanted:
            input_role = input_role.replace(i,'')
        all_roles = []

        for role in ctx.guild.roles:
            all_roles.append(role.name)
        try:
            role = discord.utils.get(ctx.guild.roles, id=int(input_role))
        except:
            match = process.extractOne(input_role, all_roles, score_cutoff=30)[0]
            role = discord.utils.get(ctx.guild.roles, name=match)

        members = role.members
        memberlist = []

        if len(members) > 60:
            await ctx.send(f"Users with the {role} role ({len(role.members)}):\nToo many users to list!")
            return
        if len(members) == 0:
            await ctx.send(f"No user currently has the {role} role!")
            return
        else:
            for member in members:
                memberlist.append(f"{member.name}#{member.discriminator}")
            all_members = ', '.join(memberlist)
            await ctx.send(f"Users with the {role} role ({len(role.members)}):\n{all_members}")



    #serverinfo, gives out basic info about the server
    @commands.command(aliases=['serverinfo'])
    async def server(self, ctx):
        if not ctx.guild:
            await ctx.send("This command is only available on servers.")
            return

        server = ctx.guild
        embed = discord.Embed(title=f"{server.name}({server.id})", color=discord.Color.green())
        embed.add_field(name="Created on:", value=discord.utils.format_dt(server.created_at, style='F'), inline=True) #timezone aware datetime object, F is long formatting
        embed.add_field(name="Owner:", value=server.owner.mention, inline=True)
        embed.add_field(name="Channels:", value=len(server.channels), inline=True)
        embed.add_field(name="Members:", value=f"{len(server.members)} (Bots: {sum(member.bot for member in server.members)})")
        embed.add_field(name="Emojis:", value=len(server.emojis))
        embed.add_field(name="Roles:", value=len(server.roles))
        embed.set_thumbnail(url=server.icon.url)
        await ctx.send(embed=embed)


    #userinfo
    @commands.command(aliases=['user'])
    async def userinfo(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author

        try:
            activity = member.activity.name
        except:
            activity = "None"

        if not ctx.guild:
            await ctx.send("This command can only be used in the SSBU TG Discord Server.")
            return

        sorted_members = sorted(ctx.guild.members, key=lambda x:x.joined_at)
        index = sorted_members.index(member)


        embed = discord.Embed(title=f"Userinfo of {member.name}#{member.discriminator} ({member.id})", color=member.top_role.color)
        embed.add_field(name="Name:", value=member.mention, inline=True)
        embed.add_field(name="Top Role:", value=member.top_role.mention, inline=True)
        embed.add_field(name="Number of Roles:", value=f"{(len(member.roles)-1)}", inline=True) #gives the number of roles to prevent listing like 35 roles, -1 for the @everyone role
        embed.add_field(name="Joined Server on:", value=discord.utils.format_dt(member.joined_at, style='F'), inline=True) #timezone aware datetime object, F is long formatting
        embed.add_field(name="Join Rank:", value=f"{(index+1)}/{len(ctx.guild.members)}", inline=True)
        embed.add_field(name="Joined Discord on:",  value=discord.utils.format_dt(member.created_at, style='F'), inline=True)
        embed.add_field(name="Online Status:", value=member.status, inline=True)
        embed.add_field(name="Activity Status:", value=activity, inline=True)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)


    #some bot stats
    @commands.command(aliases=['stats'])
    async def botstats(self, ctx):
        pyversion = platform.python_version() #python version
        dpyversion = discord.__version__ #discord.py version
        servercount = len(self.bot.guilds) #total servers
        membercount = len(set(self.bot.get_all_members())) #total members
        proc = psutil.Process(os.getpid()) #gets process id
        uptimeSeconds = time.time() - proc.create_time() #gets uptime in seconds
        delta = datetime.timedelta(seconds=uptimeSeconds) #converts that to a timedelta object
        tabuu3 = self.bot.get_user(785303736582012969) #the bot
        embed = discord.Embed(title="Tabuu 3.0 Stats", color=0x007377, url="https://github.com/sonnenbankpimp/Tabuu-3.0-Bot") #link to the github, its still private but maybe not in the future, who knows
        embed.add_field(name="Name:", value=f"{tabuu3.mention}", inline=True)
        embed.add_field(name="Servers:", value=servercount, inline=True)
        embed.add_field(name="Total Users:", value=membercount, inline=True)
        embed.add_field(name="Bot Version:", value=self.bot.version_number, inline=True)
        embed.add_field(name="Python Version:", value=pyversion, inline=True)
        embed.add_field(name="discord.py Version:", value=dpyversion, inline=True)
        embed.add_field(name="CPU Usage:", value=f"{psutil.cpu_percent(interval=1)}%", inline=True) #only gets the % value
        embed.add_field(name="RAM Usage:", value=f"{psutil.virtual_memory()[2]}%", inline=True) #only gets the % value, thats what the [2] is for
        embed.add_field(name="Uptime:", value=str(delta).split(".")[0], inline=True) #the split thing is to get rid of the microseconds, who cares about uptime in microseconds
        embed.set_footer(text="Creator: Phxenix#1104, hosted on: Raspberry Pi 3B+")
        embed.set_thumbnail(url=tabuu3.avatar.url)
        await ctx.send(embed=embed)




    #error handling for the above
    @listrole.error
    async def listrole_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send("You need to name a valid role!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Nice try, but you don't have the permissions to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I didn't find a good match for the role you provided. Please be more specific, or mention the role, or use the Role ID.")
        else:
            raise error

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send("You need to name a valid role!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Nice try, but you don't have the permissions to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I didn't find a good match for the role you provided. Please be more specific, or mention the role, or use the Role ID.")
        else:
            raise error
        

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member, or just leave it blank.")
        else:
            raise error


def setup(bot):
    bot.add_cog(Stats(bot))
    print("Stats cog loaded")