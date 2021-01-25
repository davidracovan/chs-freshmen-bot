from logging import log
import os
import textwrap
import asyncio
import discord
import json
import random
from discord.ext import commands

# https://discord.com/api/oauth2/authorize?client_id=802211256383438861&permissions=2147483639&scope=bot

with open('config.json', 'r') as f:
    token_dict = json.load(f)
    BOT_TOKEN = token_dict['token']

bot = commands.Bot(command_prefix='chs_', help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='/help | CHS is great!'))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = create_embed(ctx, 'Bot Commands')
            embed.add_field(name='Fun Commands', value='`/help fun`', inline=False)
            embed.add_field(name='Informational Commands', value='`/help info`', inline=False)
            embed.add_field(name='Server Moderation Commands', value='`/help mod`', inline=False)
            embed.add_field(name='Link Commands', value='`/help link`', inline=False)
            await ctx.send(embed=embed)
            log_command(ctx)

    @help.command(name='fun')
    async def _fun(self, ctx):
        embed = create_embed(ctx, 'Fun Commands')
        embed.add_field(name='/hello', value='Allows you to greet the bot and earn some coins.', inline=False)
        embed.add_field(name='/8ball <question>', value='Ask a question, get an answer.', inline=False)
        embed.add_field(name='/rng <minimum> <maximum>', value='Generate a random number between two numbers.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='info')
    async def _info(self, ctx):
        embed = create_embed(ctx, 'Informational Commands')
        embed.add_field(name='/ping', value="Tells you the latency of the bot (basically my WiFi speed lol).", inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='mod')
    async def _mod(self, ctx):
        embed = create_embed(ctx, 'Server Moderation Commands')
        embed.add_field(name='/purge <message count>', value="Purges messages from the current channel.", inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='link')
    async def _link(self, ctx):
        embed = create_embed(ctx, 'Link Commands')
        embed.add_field(name='/safety', value='Links to Safety Dance.', inline=False)
        embed.add_field(name='/tainted', value='Links to Tainted Love.', inline=False)
        embed.add_field(name='/goldenhair', value='Links to Sister Golden Hair.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(Help(bot))

class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _register(self, user, blue_lunch, gold_lunch, cohort):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if str(user) not in users:
            with open('users.json', 'w') as f:
                users[user]['blue_lunch'] = blue_lunch
                users[user]['gold_lunch'] = gold_lunch
                users[user]['cohort'] = cohort
                json.dump(users, f)

    def _registration_checks(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        return str(ctx.author.id) in users
    
    def _get_users_dict(self, ctx):
        with open('users.json', 'r') as f: 
            users = json.load(f)
        return users
    
    def _set_users_dict(self, ctx, users):
        with open('users.json', 'w') as f:
            json.dump(users, f)
    
    @commands.command()
    async def register(self, ctx, blue_lunch, gold_lunch, cohort):
        self._register(ctx.author.id, blue_lunch, gold_lunch, cohort)
        desc = f'{ctx.author.mention}, you have been registered.'
        embed = create_embed(ctx, 'User Registration', description=desc)
        embed.add_field(name='Blue Day Lunch', value=blue_lunch, inline=False)
        embed.add_field(name='Gold Day Lunch', value=gold_lunch, inline=False)
        embed.add_field(name='Cohort', value=cohort, inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(School(bot)) 

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        embed = create_embed(ctx, 'Hello!', description=f'How are you, {ctx.author.mention}?')
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.command(name='8ball')
    async def eightball(self, ctx, arg):
        responses = [
            ":green_circle: As I see it, yes. :green_circle:",
            ":yellow_circle: Ask again later. :yellow_circle:",
            ":yellow_circle: Better not tell you now. :yellow_circle:",
            ":yellow_circle: Cannot predict now. :yellow_circle:",
            ":yellow_circle: Concentrate and ask again. :yellow_circle:",
            ":red_circle: Don’t count on it. :red_circle:",
            ":green_circle: It is certain. :green_circle:",
            ":green_circle: It is decidedly so. :green_circle:",
            ":green_circle: Most likely. :green_circle:",
            ":red_circle: My reply is no. :red_circle:",
            ":red_circle: My sources say no. :red_circle:",
            ":red_circle: Outlook not so good. :red_circle:",
            ":green_circle: Outlook good. :green_circle:",
            ":yellow_circle: Reply hazy, try again. :yellow_circle:",
            ":green_circle: Signs point to yes. :green_circle:",
            ":red_circle: Very doubtful. :red_circle:",
            ":green_circle: Without a doubt. :green_circle:",
            ":green_circle: Yes. :green_circle:",
            ":green_circle: Yes, definitely. :green_circle:",
            ":green_circle: You may rely on it. :green_circle:"
        ]

        desc = responses[random.randint(0,19)]
        embed = create_embed(ctx, 'Magic 8 Ball', description=desc)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.command()
    async def rng(self, ctx, minnum:int, maxnum: int):
        await ctx.send(random.randint(minnum, maxnum))
        log_command(ctx)

bot.add_cog(Fun(bot))

class Links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def safety(self, ctx):
        embed = create_embed(ctx, 'Safety Dance', url='https://www.youtube.com/watch?v=AjPau5QYtYs')
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.command()
    async def tainted(self, ctx):
        embed = create_embed(ctx, 'Tainted Love', url='https://www.youtube.com/watch?v=ZcyCQLewj10')
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.command()
    async def goldenhair(self, ctx):
        embed = create_embed(ctx, 'Sister Golden Hair', url='https://www.youtube.com/watch?v=XIycEe59Auc')
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(Links(bot))

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = create_embed(ctx, 'Pong!', description=f'`{round(bot.latency * 1000, 1)}ms`')
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.command()
    async def version(self, ctx):
        embed = create_embed(ctx, 'Version History')
        embed.add_field(name='Current Version', value='`0.0.1`', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(Info(bot))

@bot.command()
async def davidisbad(ctx):
    embed = create_embed(ctx, 'No u', description=f'{ctx.author.mention} ur bad')
    await ctx.send(embed=embed)
    log_command(ctx)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, num: int):
        if ctx.author.guild_permissions.manage_messages == True:
            msgs = []
            async for x in ctx.channel.history(limit=num):
                msgs.append(x)
            await ctx.channel.delete_messages(msgs)
            embed = create_embed(ctx, 'Message Purge', f'{num} messages deleted.')
            await ctx.send(embed=embed)
            asyncio.sleep(5)
        else:
            embed = create_embed(ctx, 'Message Purge', 'You do not have the required permission to run this command (Manage Messages).')
            await ctx.send(embed=embed)

bot.add_cog(Moderation(bot))

def create_embed(ctx, title, description=None, url=None):
    embed = discord.Embed(title=title, description=description, url=url)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f'Server: {ctx.guild} | Command: {ctx.message.content}', icon_url=ctx.guild.icon_url)
    return embed

def log_command(ctx):
    print(f'{ctx.author} ran {ctx.message.content}.')

bot.run(BOT_TOKEN) # bot token