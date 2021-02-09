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
        embed = tools.create_embed(ctx, "Tic Tac Toe Request", desc=f'{player2.mention}, you have 45 seconds to respond to {ctx.author.mention}\'s request to play Tic Tac Toe.\nType "y" or "yes" to accept.')
        await ctx.send(embed=embed)
        def check(msg):
            return msg.author == player2 and msg.channel == ctx.channel

        msg = await self.bot.wait_for('message', check=check, timeout=45)
        if msg.content.lower() in ['y','yes']:
            await self.start_game(ctx, player2)

    async def start_game(self, ctx, p2):
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

        game['p1'] = ctx.message.author
        game['p2'] = p2
        game['turn'] = 'p1'

        board_text = self.create_board_text(game['board'])
        embed = discord.Embed(title='Tic Tac Toe', description=board_text)
        footer = f'{game["p1"].name} playing {game["p2"].name}\n{game[game["turn"]].name}\'s turn'
        embed.set_footer(text=footer)
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

    async def update_game(self, game_id, game, location, player):
        game['board'][location] = player
        if player == 'p1':
            game['turn'] = 'p2'
        if player == 'p2':
            game['turn'] = 'p1'
        self.games[game_id] = game
        board_text = self.create_board_text(game['board'])
        embed = discord.Embed(title='Tic Tac Toe', description=board_text)
        footer = f'{game["p1"].name} playing {game["p2"].name}\n{game[game["turn"]].name}\'s turn'
        embed.set_footer(text=footer)
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
            if user.id == active_game[active_game['turn']].id:
                await self.update_game(reaction.message.id, active_game, location, active_game['turn'])
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
