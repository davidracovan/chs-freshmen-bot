import discord
from discord.ext import commands
from bot import tools
import asyncio
import re

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boards = []

    def start_game(self, ctx, player2):
        board = {"board": [["", "", ""], ["", "", ""], ["", "", ""]]}
        board["player1"] = ctx.message.author.id
        board["player2"] = player2.id
        self.boards[ctx.message.id] = board

    def update_board(self, board):
        pass

    @commands.command(aliases=['tic', 'tac', 'toe', 'ttt'])
    async def tictactoe(self, ctx, player2: discord.User):

        def check(msg):
            return msg.author == player2 and msg.channel == ctx.channel and \
            msg.content.lower() in ['y', 'n']

        msg = await self.bot.wait_for('message', check=check, timeout=60)
    
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     active_board = None
    #     if payload.message_id in board["message_id"]:
    #         active_board = board

    @commands.command()
    async def sendboard(self, ctx):
        board = "x x x\nx o o\no o x"
        board = re.sub('x', '<:ttt_x:808393849965379687>', board)
        board = re.sub('o', '<:ttt_x:808393849965379687>', board)
        embed = tools.create_embed(ctx, 'Testing TTT Board', desc=board)
