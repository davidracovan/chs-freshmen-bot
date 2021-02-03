import asyncio
import discord
import json
import random
from datetime import datetime
from discord.ext import commands
import classschedule
import os
from keep_alive import keep_alive

# https://discord.com/api/oauth2/authorize?client_id=796805491186597968&permissions=2147483639&scope=bot

# with open('config.json', 'r') as f:
#     token_dict = json.load(f)
#     BOT_TOKEN = token_dict['token']

PREFIX = 'c?'

bot = commands.Bot(command_prefix=PREFIX, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'{PREFIX}help'))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            author1 = await ctx.guild.fetch_member(688530998920871969)
            author2 = await ctx.guild.fetch_member(654874992672112650)
            embed = create_embed(ctx, 'Bot Commands', description=f"Written by {author1.mention} and {author2.mention}.")
            embed.add_field(name='Fun Commands', value=f'`{PREFIX}help fun`', inline=False)
            embed.add_field(name='Informational Commands', value=f'`{PREFIX}help info`', inline=False)
            embed.add_field(name='School Commands', value=f'`{PREFIX}help school`', inline=False)
            await ctx.send(embed=embed)
            log_command(ctx)

    @help.command(name='fun')
    async def _fun(self, ctx):
        embed = create_embed(ctx, 'Fun Commands')
        embed.add_field(name=f'{PREFIX}_hello', value='Allows you to greet the bot.', inline=False)
        embed.add_field(name=f'{PREFIX}8ball <question>', value='Ask a question, get an answer.', inline=False)
        embed.add_field(name=f'{PREFIX}rng <minimum> <maximum>', value='Generate a random number between two numbers.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='info')
    async def _info(self, ctx):
        embed = create_embed(ctx, 'Informational Commands')
        embed.add_field(name=f'{PREFIX}ping', value="Tells you the latency of the bot (basically my WiFi speed lol).", inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='school')
    async def _school(self, ctx):
        embed = create_embed(ctx, 'School Commands')
        embed.add_field(name=f'{PREFIX}register <blue day lunch> <gold day lunch> <cohort>', value="Example: `chs_register B D greyhound`\nAllows you to register details with the bot to get personalized responses.\nAll three values are required.\nOther commands will currently not work without registration.", inline=False)
        embed.add_field(name=f'{PREFIX}schoolday [all]', value="Tells you information about today (Blue/Gold, In Person/Virtual, Late Start, weekends, breaks, etc.).\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        embed.add_field(name=f'{PREFIX}schoolweek [all]', value="Tells you information about the next seven days.\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        embed.add_field(name=f'{PREFIX}schooldate <date> [all]', value="Tells you information about a specified date.\nThe `date` argument is required, and must be in the form `mm/dd/yyyy`.\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)


bot.add_cog(Help(bot))

class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _register(self, user: str, blue_lunch, gold_lunch, cohort):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        if user not in school_dict:
            with open('school.json', 'w') as f:
                school_dict[user] = {
                    'blue_lunch': blue_lunch.upper(),
                    'gold_lunch': gold_lunch.upper(),
                    'cohort': cohort.lower()
                }
                json.dump(school_dict, f)

    def _register_class(self, user_id, class_type: str, class_name):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        if str(user_id) not in school_dict:
            with open('school.json', 'w') as f:
                if not school_dict[str(user_id)]['classes']:
                    school_dict[str(user_id)]['classes'] = {}
                school_dict[str(user_id)]['classes'][class_type] = class_name
                json.dump(school_dict, f)

    def _registration_checks(self, ctx):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        return str(ctx.author.id) in school_dict
    
    def _class_registration_checks(self, ctx, class_type):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        return str(ctx.author.id) in school_dict

    def _get_users_dict(self):
        with open('school.json', 'r') as f: 
            school_dict = json.load(f)
        return school_dict

    def _get_user_info(self, user: str):
        with open('school.json', 'r') as f: 
            school_dict = json.load(f)
        return school_dict[user]
    
    def _set_users_dict(self, school_dict):
        with open('school.json', 'w') as f:
            json.dump(school_dict, f)
    
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
    
    @commands.command()
    async def register(self, ctx, blue_lunch, gold_lunch, cohort):
        self._register(ctx.author.id, blue_lunch, gold_lunch, cohort)
        desc = f'You have been registered.'
        embed = create_embed(ctx, 'User Registration', description=desc)
        embed.add_field(name='Blue Day Lunch', value=blue_lunch, inline=False)
        embed.add_field(name='Gold Day Lunch', value=gold_lunch, inline=False)
        embed.add_field(name='Cohort', value=cohort, inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.command(name='registerclass')
    async def register_class(self, ctx, class_type, class_name):
        self._register_class(ctx.author.id, class_type.lower(), class_name)
        desc = f'{ctx.author.mention}, you have been registered.'
        embed = create_embed(ctx, 'Class Registration', description=desc)
        embed.add_field(name=class_type, value=class_name, inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.group()
    async def schoolday(self, ctx, arg=None):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_day = classschedule.get_current_day(user_info)
            desc = f'Today is {datetime.now().strftime("%A, %B %d, %Y")}.\nYour Cohort ({user_info["cohort"].title()}): {school_day}'
            embed = create_embed(ctx, 'School Day', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @schoolday.command(name='all')
    async def day_all(self, ctx):
        school_day = classschedule.get_current_day()
        desc = f'Today is {datetime.now().strftime("%A, %B %d, %Y")}.\nCarmel Cohort: {school_day[0]}.\nGreyhound Cohort: {school_day[1]}.\n'
        embed = create_embed(ctx, 'School Day', desc)
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.group()
    async def schoolweek(self, ctx):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_week = classschedule.get_week(user_info)
            desc = '\n'.join(school_week)
            embed = create_embed(ctx, 'School Week', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @schoolweek.command(name='all')
    async def schoolweek_all(self, ctx):
        school_weeks = classschedule.get_week()
        embed = create_embed(ctx, 'School Week')
        value1='\n'.join(school_weeks[0])
        embed.add_field(name='Carmel Cohort', value=value1)
        value2='\n'.join(school_weeks[1])
        embed.add_field(name='Greyhound Cohort', value=value2)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.group()
    async def schooldate(self, ctx, date):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_day = classschedule.get_day(date, user_info)
            desc = f'Your Cohort ({user_info["cohort"].title()}): {school_day}'
            embed = create_embed(ctx, 'School Day', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @schooldate.command(name='all')
    async def schooldate_all(self, ctx, date):
        school_day = classschedule.get_day(date)
        desc = f'Carmel Cohort: {school_day[0]}\nGreyhound Cohort: {school_day[1]}\n'
        embed = create_embed(ctx, 'School Day', desc)
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
            [
                ':green_circle: As I see it, yes. :green_circle:',
                ':green_circle: It is certain. :green_circle:',
                ':green_circle: It is decidedly so. :green_circle:',
                ':green_circle: Most likely. :green_circle:',
                ':green_circle: Outlook good. :green_circle:',
                ':green_circle: Signs point to yes. :green_circle:',
                ':green_circle: Without a doubt. :green_circle:',
                ':green_circle: Yes. :green_circle:',
                ':green_circle: Yes, definitely. :green_circle:',
                ':green_circle: You may rely on it. :green_circle:'
            ],
            [
                ':red_circle: Very doubtful. :red_circle:',
                ':red_circle: My reply is no. :red_circle:',
                ':red_circle: My sources say no. :red_circle:',
                ':red_circle: Outlook not so good. :red_circle:',
                ':red_circle: Don’t count on it. :red_circle:',
            ],
            [
                ':yellow_circle: Ask again later. :yellow_circle:',
                ':yellow_circle: Better not tell you now. :yellow_circle:',
                ':yellow_circle: Cannot predict now. :yellow_circle:',
                ':yellow_circle: Concentrate and ask again. :yellow_circle:',
                ':yellow_circle: Reply hazy, try again. :yellow_circle:',
            ],
        ]
        response_category = responses[random.randint(0,2)]
        desc = response_category[random.randint(0, len(response_category)-1)]
        embed = create_embed(ctx, 'Magic 8 Ball', description=desc)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.command()
    async def rng(self, ctx, minnum:int, maxnum: int):
        await ctx.send(random.randint(minnum, maxnum))
        log_command(ctx)

bot.add_cog(Fun(bot))

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

def create_embed(ctx, title, description=None, url=None):
    embed = discord.Embed(title=title, description=description, url=url)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f'Server: {ctx.guild} | Command: {ctx.message.content}', icon_url=ctx.guild.icon_url)
    return embed

def log_command(ctx):
    print(f'{ctx.author} ran {ctx.message.content}.')

keep_alive()
bot.run(os.environ['TOKEN']) # bot token