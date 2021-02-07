import discord
from discord.ext import commands
from bot import tools

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            author1 = await ctx.guild.fetch_member(688530998920871969)
            author2 = await ctx.guild.fetch_member(654874992672112650)
            embed = tools.create_embed(ctx, 'Bot Commands', desc=f"Written by {author1.mention} and {author2.mention}.")
            embed.add_field(name='Fun Commands', value=f'`{ctx.prefix}help fun`', inline=False)
            embed.add_field(name='Informational Commands', value=f'`{ctx.prefix}help info`', inline=False)
            embed.add_field(name='School Commands', value=f'`{ctx.prefix}help school`', inline=False)
            await ctx.send(embed=embed)

    @help.command(name='fun')
    async def _fun(self, ctx):
        embed = tools.create_embed(ctx, 'Fun Commands')
        embed.add_field(name=f'{ctx.prefix}_hello', value='Allows you to greet the bot.', inline=False)
        embed.add_field(name=f'{ctx.prefix}8ball <question>', value='Ask a question, get an answer.', inline=False)
        embed.add_field(name=f'{ctx.prefix}rng <minimum> <maximum>', value='Generate a random number between two numbers.', inline=False)
        await ctx.send(embed=embed)

    @help.command(name='info')
    async def _info(self, ctx):
        embed = tools.create_embed(ctx, 'Informational Commands')
        embed.add_field(name=f'{ctx.prefix}ping', value="Tells you the latency of the bot (basically my WiFi speed lol).", inline=False)
        await ctx.send(embed=embed)

    @help.command(name='school')
    async def _school(self, ctx):
        embed = tools.create_embed(ctx, 'School Commands')
        embed.add_field(name=f'{ctx.prefix}register <blue day lunch> <gold day lunch> <cohort>', value="Example: `chs_register B D greyhound`\nAllows you to register details with the bot to get personalized responses.\nAll three values are required.\nOther commands will currently not work without registration.", inline=False)
        embed.add_field(name=f'{ctx.prefix}schoolday [all]', value="Tells you information about today (Blue/Gold, In Person/Virtual, Late Start, weekends, breaks, etc.).\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        embed.add_field(name=f'{ctx.prefix}schoolweek [all]', value="Tells you information about the next seven days.\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        embed.add_field(name=f'{ctx.prefix}schooldate <date> [all]', value="Tells you information about a specified date.\nThe `date` argument is required, and must be in the form `mm/dd/yyyy`.\nThe `all` argument is optional, and it will display information for both cohorts.", inline=False)
        await ctx.send(embed=embed)