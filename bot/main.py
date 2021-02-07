import discord
from discord.ext import commands
import os

from bot.cogs.suggestions import Suggestions
from bot.cogs.events import Events
from bot.cogs.school import School
from bot.cogs.fun import Fun
# from bot.cogs.help import Help
from bot.cogs.info import Info

# https://discord.com/api/oauth2/authorize?client_id=796805491186597968&permissions=2147483639&scope=bot

def start():
    bot = commands.Bot(command_prefix='c?')
    bot.add_cog(Events(bot))
    bot.add_cog(Suggestions(bot))
    bot.add_cog(School(bot))
    bot.add_cog(Fun(bot))
    # bot.add_cog(Help(bot))
    bot.add_cog(Info(bot))
    bot.run(os.environ['TOKEN']) # bot token

if __name__ == "__main__":
    start()