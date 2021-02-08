import discord
from discord.ext import commands
from bot import tools
import asyncio
import re

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(aliases=['tic', 'tac', 'toe', 'ttt'])
    async def tictactoe(self, ctx, player2: discord.User):
        def check(msg):
            return msg.author == player2 and msg.channel == ctx.channel

        msg = await self.bot.wait_for('message', check=check, timeout=60)
        if msg.content.lower() == 'y':
            await self.start_game(ctx, player2)

    async def start_game(self, ctx, player2):
        game = {'board': {
            'a1':'', 
            'b1':'', 
            'c1':'', 
            'a2':'', 
            'b2':'', 
            'c2':'', 
            'a3':'', 
            'b3':'', 
            'c3':''
            }
        }

        game['player1'] = ctx.message.author
        game['player2'] = player2

        board_text = self.create_board_text(game['board'])
        embed = discord.Embed(title='Tic Tac Toe', description=board_text)
        embed.set_footer(text=f'{game["player1"].mention} playing {game["player2"].mention}')
        msg = await ctx.send(embed=embed)
        for arrow in ['↖️','⬆️','↗️','⬅️','⏺','➡️','↙️','⬇️','↘️']:
            await msg.add_reaction(arrow)
        game['msg'] = msg
        self.games[msg.id] = game
    
    def create_board_text(self, board):
        iter_list = [['a1','b1','c1'],['a2','b2','c2'],['a3','b3','c3']]
        text = ''
        for row in iter_list:
            for item in row:
                if board[item] == 'p1':
                    text += '<:ttt_x:808393849965379687>'
                elif board[item] == 'p2':
                    text += '<:ttt_o:808393850250854501>'
                elif board[item] == '':
                    text += '<:ttt_w:808396628766621787>'
            text += '\n'
        return text

    async def update_board(self, game_id, game, location, player):
        game['board'][location] = player
        self.games[game_id] = game
        board_text = self.create_board_text(game['board'])
        embed = discord.Embed(title='Tic Tac Toe', description=board_text)
        embed.set_footer(text=f'{game["player1"].mention} playing {game["player2"].mention}')
        await game['msg'].edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        compare_dict = {
            '↖️':'a1',
            '⬆️':'b1',
            '↗️':'c1',
            '⬅️':'a2',
            '⏺':'b2',
            '➡️':'c2',
            '↙️':'a3',
            '⬇️':'b3',
            '↘️':'c3'
        }
        active_game = self.games.get(reaction.message.id)
        
        if active_game and (user.id != 802211256383438861):
            location = compare_dict[reaction.emoji]
            if user.id == active_game["player1"].id:
                await self.update_board(reaction.message.id, active_game, location, "p1")
            if user.id == active_game["player2"].id:
                await self.update_board(reaction.message.id, active_game, location, "p2")
            await reaction.remove(user)
        

    # @commands.command()
    # async def sendboard(self, ctx):
    #     board = 'xxx\nxwo\nowx'
    #     board = re.sub('x', '<:ttt_x:808393849965379687>', board)
    #     board = re.sub('o', '<:ttt_o:808393850250854501>', board)
    #     board = re.sub('w', '<:ttt_w:808396628766621787>', board)
    #     embed = tools.create_embed(ctx, 'Testing TTT Board', desc=board)
    #     msg = await ctx.send(embed=embed)
    #     for arrow in ['↖️','⬆️','↗️','⬅️','⏺','➡️','↙️','⬇️','↘️']:
    #         await msg.add_reaction(arrow)
