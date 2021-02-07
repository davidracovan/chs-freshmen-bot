import discord
from discord.ext import commands
from bot import tools
import asyncio

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 900, type=commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        embed = tools.create_embed(ctx, "Suggestion Reason", "What is the reason for your suggestion?")
        await ctx.send(embed=embed)
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if msg.content.lower() in ["none", "stop"]:
                reason = None
            else:
                reason = msg.content
        except asyncio.TimeoutError:
            embed = tools.create_error_embed(ctx, "Sorry, you didn't respond in time!")
            await ctx.send(embed=embed)
            return

        embed = tools.create_embed(ctx, "Suggestion Notes", "What else you would like to add? Type \"None\" if you don't have anything else.")
        await ctx.send(embed=embed)
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if msg.content.lower() in ["none", "stop"]:
                notes = None
            else:
                notes = msg.content
        except asyncio.TimeoutError:
            embed = tools.create_error_embed(ctx, "You didn't respond in time!")
            await ctx.send(embed=embed)
            return

        suggestions_channel = self.bot.get_channel(710959620667211817)
        embed = tools.create_embed(ctx, "Suggestion", desc=suggestion, footer_enabled=False)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)
        msg = await suggestions_channel.send(embed=embed)
        await msg.add_reaction('<:upvote:711333713316937819>')
        await msg.add_reaction('<:downvote:711333713354686484>')

        embed = tools.create_embed(ctx, "Suggestion", desc="Your suggestion has been submitted successfully!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removesuggestion(self, ctx, arg: int):
        suggestions_channel = self.bot.get_channel(710959620667211817)
        msg = await suggestions_channel.fetch_message(arg)
        await msg.delete()
        desc = f"Suggestion with ID {arg} has been removed."
        embed = tools.create_embed(ctx, "Suggestion Removal", desc=desc)
        await ctx.send(embed=embed)