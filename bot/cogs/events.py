import discord
from discord.ext import commands
from bot import tools
import asyncio
import time
import json

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}.')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'c?help | ccs.k12.in.us/chs'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = tools.create_error_embed(ctx, f"This command has been rate-limited. Please try again in {time.strftime('%Mm %Ss', time.gmtime(round(error.retry_after, 1)))}.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = tools.create_error_embed(ctx, f"You do not have the required permission to run this command ({','.join(error.missing_perms)}).")
            await ctx.send(embed=embed)
        elif isinstance(error, asyncio.TimeoutError):
            embed = tools.create_error_embed(ctx, "You didn't respond in time!")
            await ctx.send(embed=embed)
        else:
            raise error