import discord
from discord.ext import commands
from bot import tools
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hi"])
    async def hello(self, ctx):
        f"""Greet the bot!"""
        embed = tools.create_embed(ctx, 'Hello!', desc=f'How are you, {ctx.author.mention}?')
        await ctx.send(embed=embed)
    
    @commands.command(name='8ball')
    async def eightball(self, ctx, *, request):
        f"""Consult the Magic 8 Ball. It is never wrong!"""
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
        if ("lying" in request.lower()) or ("lie" in request.lower()):
            print("test")
            desc = ":green_circle: :yellow_circle: :red_circle: How dare you! The magical 8 ball never lies! Shame on you! :red_circle: :yellow_circle: :green_circle:"
        else:
            desc = response_category[random.randint(0, len(response_category)-1)]
        embed = tools.create_embed(ctx, 'Magic 8 Ball', desc=desc)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rng(self, ctx, minnum:int, maxnum: int):
        await ctx.send(random.randint(minnum, maxnum))