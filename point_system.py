#point_system.py

import discord, random
from discord.ext import commands
from pathlib import Path
import numpy as np
import pandas as pd

def get_balance(userid):
    points = pd.read_csv(Path('points.csv'))
    points = points.set_index('uid')
    return points.loc[userid]['bal']

def create_entry(userid, balance):
    """
    Creates an entry in points.csv.
    """
    points = pd.read_csv(Path('points.csv'))
    entry = {'uid': userid, 'bal': balance}
    penis = points.append(entry, ignore_index=True)
    penis.to_csv('points.csv', index=False)

def update_entry(userid, balance):
    """
    Updates a user's balance by a set amount. If entry for user does not exist, create a new entry.
    """
    points = pd.read_csv(Path('points.csv'))
    if userid not in points['uid'].values:
        create_entry(userid, balance)
    else:
        points = points.set_index('uid')
        before = get_balance(userid)
        after = int(before) + int(balance)
        points.loc[userid] = pd.Series({'bal': after})
        points = points.reset_index()
        points.to_csv('points.csv', index=False)

def set_entry(userid, balance):
    """
    Set a user's balance to specified amount. If entry for user does not exist, create a new entry.
    """
    points = pd.read_csv(Path('points.csv'))
    if userid not in points['uid'].values:
        create_entry(userid, balance)
    else:
        points = points.set_index('uid')
        points.loc[userid] = pd.Series({'bal': balance})
        points = points.reset_index()
        points.to_csv('points.csv', index=False)

class Currency(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(rate=1, per=72000, type=commands.BucketType.user)
    async def daily(self, ctx):
        update_entry(ctx.author.id, 500)
        await ctx.send(embed=discord.Embed(title='C H R <:OMEGALUL:392184053975220244> M I E S', color=0x69f420,
                                        description=f'<:GoodPepeDank:794513428014039060>500 chromosomes added to {ctx.author.name}\'s balance!'))

    @commands.command()
    async def balance(self, ctx):
        try:
            bal = get_balance(ctx.author.id)
        except:
            bal = 0
        await ctx.send(embed=discord.Embed(title=f'{ctx.author.name}\'s balance', color=0x69f420,
                                        description=f'<:GoodPepeDank:794513428014039060>{bal} chromosomes'))

    @commands.command()
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def gamble(self, ctx, amount):
        if amount == 'all':
            amount = get_balance(ctx.author.id)
        try:
            amount = int(amount)
        except:
            await ctx.send(embed=discord.Embed(title='Error', color=0xff1100, description=f':x: Invalid amount!'))
            return
        if amount > get_balance(ctx.author.id):
            await ctx.send(embed=discord.Embed(title='Error', color=0xff1100, description=f':x: Amount must be less than or equal to your current balance!'))
            return
        elif amount <= 0:
            await ctx.send(embed=discord.Embed(title='Error', color=0xff1100, description=f':x: Amount must be greater than zero!'))
            return
        
        if random.random() < 0.5:
            update_entry(ctx.author.id, amount)
            await ctx.send(embed=discord.Embed(title='You win!', color=0x69f420,
                                            description=f'{amount} chromosomes added to {ctx.author.name}\'s balance!\n\
                                                Current balance: <:GoodPepeDank:794513428014039060>{get_balance(ctx.author.id)}'))
        else:
            update_entry(ctx.author.id, -amount)
            await ctx.send(embed=discord.Embed(title='You lose!', color=0xff1100,
                                            description=f'You lost {amount} chromosomes!\n\
                                                Current balance: <:GoodPepeDank:794513428014039060>{get_balance(ctx.author.id)}'))

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int):
        if ctx.author == member:
            await ctx.send(embed=discord.Embed(title='Error', description=f':x: You can\'t give yourself chromosomes!', color=0xff1100))
            return
        if amount > get_balance(ctx.author.id):
            await ctx.send(embed=discord.Embed(title='Error', description=f':x: Amount must be less than or equal to your current balance!', color=0xff1100))
            return
        elif amount <= 0:
            await ctx.send(embed=discord.Embed(title='Error', description=f':x: Amount must be greater than zero!', color=0xff1100))
            return
        
        await ctx.send(f'{member.mention}, {ctx.author.mention} would like to give you <:GoodPepeDank:794513428014039060>{amount} chromosomes. Type Y to accept or N to decline.')

        def _check(reply):
            return reply.author == member and reply.channel == ctx.channel and reply.content.lower() in ["y", "n"]

        reply = await bot.wait_for('message', check=_check)
        if reply.content.lower() == "y":
            update_entry(ctx.author.id, -amount)
            update_entry(member.id, amount)
            await ctx.send(embed=discord.Embed(title=f'Exchange accepted!', color=0x69f420,
                                            description=f'Current balance: <:GoodPepeDank:794513428014039060>{get_balance(ctx.author.id)}'))
        else:
            await ctx.send(embed=discord.Embed(description=f'Exchange declined.', color=0xff1100))

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def flip(self, ctx, choice: str):
        heads = {'h', 'head', 'heads'}
        tails = {'t', 'tail', 'tails'}
        if choice.lower() not in heads.union(tails):
            await ctx.send(embed=discord.Embed(title='Error', description=f':x: You must specify heads or tails!', color=0xff1100))
            return
        
        outcome = random.randint(0,1)
        if choice in heads and outcome == 0:
            update_entry(ctx.author.id, 1)
            await ctx.send(embed=discord.Embed(title='Heads!', color=0x69f420,
                                            description=f'<:Pog:689280885027242169> You won 1 chromosome!\n\
                                                Current balance: <:GoodPepeDank:794513428014039060>{get_balance(ctx.author.id)}'))
        elif choice in tails and outcome == 1:
            update_entry(ctx.author.id, 1)
            await ctx.send(embed=discord.Embed(title='Tails!', color=0x69f420,
                                            description=f'<:Pog:689280885027242169> You won 1 chromosome!\n\
                                                Current balance: <:GoodPepeDank:794513428014039060>{get_balance(ctx.author.id)}'))
        elif choice in heads and outcome == 1:
            await ctx.send(embed=discord.Embed(title='Tails!', description='<:Sadge:740811323558068238> Better luck next time!', color=0xff1100))
        elif choice in tails and outcome == 0:
            await ctx.send(embed=discord.Embed(title='Heads!', description='<:Sadge:740811323558068238> Better luck next time!', color=0xff1100))



if __name__ == '__main__':
    print('Creating/updating user entry')
    print()
    uid = input('User ID: ')
    bal = input('Balance: ')
    update_entry(uid, bal)