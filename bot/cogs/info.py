import discord
from discord.ext import commands
from bot import tools
import random

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Testing docstring"""
        embed = tools.create_embed(ctx, 'Pong!', desc=f'`{round(self.bot.latency * 1000, 1)}ms`')
        await ctx.send(embed=embed)

    @commands.command()
    async def version(self, ctx):
        embed = tools.create_embed(ctx, 'Version History')
        embed.add_field(name='Current Version', value='`0.0.1`', inline=False)
        await ctx.send(embed=embed)