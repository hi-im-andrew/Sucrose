# genshin.py

import discord, requests
import genshinstats as gs
import pandas as pd
from pathlib import Path
from discord.ext import commands, menus

# color codes for elements and rarity
colors = {'Anemo': 0x9ef9cd, 'Geo': 0xf4d862, 'Electro': 0xc36dff, 'Dendro': 0xb1ea26, 'Hydro': 0x079fff, 'Pyro': 0xff8739, 'Cryo': 0xccfffe,\
            5: 0xff8000, 4: 0xa335ee, 3: 0x0070dd, 2: 0x1eff00, 1: 0xffffff}

class Menu(menus.ListPageSource):
    async def format_page(self, menu, entry):
        return entry

class Genshin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def characters(self, ctx):
        raw = requests.get('https://api.genshin.dev/characters')
        data = raw.json()
        desc = ', '.join([i.capitalize() for i in data])
        await ctx.send(embed=discord.Embed(title='Character List', description=desc))

    @commands.command()
    async def artifacts(self, ctx):
        raw = requests.get('https://api.genshin.dev/artifacts')
        data = raw.json()
        desc = ', '.join([i.capitalize() for i in data])
        await ctx.send(embed=discord.Embed(title='Artifact Sets', description=desc))

    @commands.command()
    async def weapons(self, ctx):
        raw = requests.get('https://api.genshin.dev/weapons')
        data = raw.json()
        desc = ', '.join([i.capitalize() for i in data])
        await ctx.send(embed=discord.Embed(title='Weapon List', description=desc))

    @commands.command()
    async def character(self, ctx, name):
        name = name.lower()
        names = requests.get(f'https://api.genshin.dev/characters')
        names = names.json()
        for char in names:
            if name in char:
                name = char
                break
        
        raw = requests.get(f'https://api.genshin.dev/characters/{name}')
        data = raw.json()
        
        page1 = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["rarity"])]), color=colors[data["vision"]])
        page1.set_footer(text='Page 1/4 • Character Info • Powered by genshin.dev | Images from genshin.gg')
        page1.add_field(name='Element', value=data["vision"])
        page1.add_field(name='Weapon', value=data["weapon"])
        page1.add_field(name='Bio', value=data["description"], inline=False)
        
        page2 = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["rarity"])]), color=colors[data["vision"]])
        page2.set_footer(text='Page 2/4 • Skill Talents • Powered by genshin.dev | Images from genshin.gg')
        for talent in data["skillTalents"]:
            page2.add_field(name=f'{talent["unlock"]}: {talent["name"]}', value=talent["description"], inline=False)
        
        page3 = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["rarity"])]), color=colors[data["vision"]])
        page3.set_footer(text='Page 3/4 • Passive Talents • Powered by genshin.dev | Images from genshin.gg')
        for passive in data["passiveTalents"]:
            page3.add_field(name=f'{passive["name"]}: {passive["unlock"]}', value=passive["description"], inline=False)
        
        page4 = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["rarity"])]), color=colors[data["vision"]])
        page4.set_footer(text='Page 4/4 • Constellations • Powered by genshin.dev | Images from genshin.gg')
        for const in data["constellations"]:
            page4.add_field(name=f'{const["unlock"]}: {const["name"]}', value=const["description"], inline=False)
        
        embeds = [page1, page2, page3, page4]

        for p in embeds:
            if 'traveler' in name:
                p.set_thumbnail(url=f'https://static.wikia.nocookie.net/gensin-impact/images/7/71/Character_Traveler_Thumb.png')
            else:
                p.set_thumbnail(url=f'https://rerollcdn.com/GENSHIN/Characters/{name.capitalize()}.png')
        
        menu = menus.MenuPages(Menu(embeds, per_page=1))
        await menu.start(ctx)

    @commands.command()
    async def artifact(self, ctx, name):
        name = name.lower()
        names = requests.get(f'https://api.genshin.dev/artifacts')
        names = names.json()
        for item in names:
            if name in item:
                name = item
                break
        
        raw = requests.get(f'https://api.genshin.dev/artifacts/{name}')
        data = raw.json()
        
        embed = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["max_rarity"])]), color=colors[data["max_rarity"]])
        embed.set_footer(text='Powered by genshin.dev | Images from genshin.gg')
        embed.add_field(name='2-Piece Bonus', value=data["2-piece_bonus"], inline=False)
        embed.add_field(name='4-Piece Bonus', value=data["4-piece_bonus"], inline=False)
        embed.set_thumbnail(url=f'https://rerollcdn.com/GENSHIN/Gear/{name.replace("-", "_")}.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def weapon(self, ctx, name):
        name = name.lower()
        names = requests.get(f'https://api.genshin.dev/weapons')
        names = names.json()
        for item in names:
            if name in item:
                name = item
                break
        
        raw = requests.get(f'https://api.genshin.dev/weapons/{name}')
        data = raw.json()
        
        embed = discord.Embed(title=f'{data["name"]}', description=''.join([':star:' for i in range(0, data["rarity"])]), color=colors[data["rarity"]])
        embed.set_footer(text='Powered by genshin.dev | Images from genshin.gg')
        embed.add_field(name='Type', value=data["type"])
        embed.add_field(name='Base ATK', value=data["baseAttack"])
        embed.add_field(name='Substat', value=data["subStat"])
        embed.add_field(name=data['passiveName'], value=data["passiveDesc"], inline=False)
        embed.add_field(name='How to Acquire', value=data["location"])
        
        # capitalize weapon name to match genshin.gg naming convention
        ignore = ['of', 'to', 'the']
        temp = name.split('-')
        if temp[0] == 'the':
            ignore.remove('the')
        x = -1
        for word in temp:
            x += 1
            if word in ignore:
                pass
            else:
                temp[x] = word.capitalize()

        embed.set_thumbnail(url=f'https://rerollcdn.com/GENSHIN/Weapon/NEW/{"_".join(temp)}.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def setcookies(self, ctx, ltuid, ltoken):
        if ltuid.isdigit():
            log_user(ctx.author.id, ltuid, ltoken)
            await ctx.send('HoYoLAB UID and site token set!')
        else:
            await ctx.send('Invalid format for UID and/or token :^(')
    
    @commands.command()
    async def setuid(self, ctx, uid):
        if len(uid) == 9 and uid.isdigit():
            log_uid(ctx.author.id, uid)
            await ctx.send('UID set!')
        else:
            await ctx.send('Invalid format for UID :^(')
    
    @commands.command()
    async def abyss(self, ctx):
        #try:
        cookies = get_cookies(ctx.author.id)
        gs.set_cookie(ltuid = cookies[1], ltoken = cookies[2])
        
        uid = get_uid(ctx.author.id)
        spiral_abyss = gs.get_spiral_abyss(uid, previous = True)
        stats = spiral_abyss['stats']
        for field, value in stats.items():
            await ctx.send(f'{field}: {value}')
        #except:
        #    await ctx.send('User not found. Please use =setuid to set your Genshin UID, and =setcookies to set your HoYoLAB account UID and site token.')

def log_user(userid, ltuid, ltoken):
    cookies = pd.read_csv(Path('cookies.csv'))
    if userid not in cookies['id'].values:
        entry = {'id' : userid, 'uid' : ltuid, 'token' : ltoken}
        temp = cookies.append(entry, ignore_index = True)
        temp.to_csv('cookies.csv', index = False)
    else:
        cookies = cookies.set_index('id')
        cookies.loc[userid] = pd.Series({'uid' : ltuid, 'token' : ltoken})
        cookies = cookies.reset_index()
        cookies.to_csv('cookies.csv', index = False)

def get_cookies(userid):
    cookies = pd.read_csv(Path('cookies.csv'))
    cookies = cookies.set_index('id')
    return (cookies.loc[userid]['ltuid'], cookies.loc[userid]['ltoken'])

def log_uid(userid, uid):
    uids = pd.read_csv(Path('uid.csv'))
    if userid not in uids['id'].values:
        entry = {'id' : userid, 'uid' : uid}
        temp = uids.append(entry, ignore_index = True)
        temp.to_csv('uid.csv', index = False)
    else:
        uids = uids.set_index('id')
        uids.loc[userid] = pd.Series({'uid' : uid})
        uids = uids.reset_index()
        uids.to_csv('uids.csv', index = False)

def get_uid(userid):
    uids = pd.read_csv(Path('uid.csv'))
    uids = uids.set_index('id')
    print(uids.loc[userid]['uid'])
    return uids.loc[userid]['uid']

#    @commands.command()
#    async def characterlist(self, ctx):
#        data = gs.get_user_stats(uid)
#        characters = gs.get_characters(uid)
#        embed = discord.Embed(title='', color=0xffffff)
#        for char in characters:
#            embed.add_field(name=f'{char["rarity"]}* {char["name"]:10}', value=f'lvl {char["level"]:2} C{char["constellation"]}')
#        await ctx.send(embed=embed)
#    
#    @commands.command()
#    async def wishhistory(self, ctx, size = 10):
#        wish = gs.get_wish_history(size = size)
#        try:
#            while True:
#                output = next(wish)
#                await ctx.send(f'{output["rarity"]}:star: {output["name"]} from {output["banner"]}, {output["time"]}')
#        except StopIteration:
#            return


#gs.set_cookie(ltuid=6661934, ltoken='0Iz67SiBDaOfKggBgWKcDsRrWjR5ZcHgBt2zWEVP')
#uid = 600771521
#gs.set_authkey('https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?im_out=true&sign_type=2&auth_appid=im_ccs&authkey_ver=1&win_direction=portrait&lang=en&device_type=pc&ext=%7b"loc"%3a%7b"x"%3a-3115.978515625%2c"y"%3a254.21266174316407%2c"z"%3a-4453.935546875%7d%2c"platform"%3a"WinST"%7d&game_version=OSRELWin2.0.0_R3900482_S3918537_D4044049&authkey=u0e468IJ3wXFerHa7Lfyj9gBSQnjHQh9pR570TawrSf7y%2bWSqXST5IOpeQv5zIsFqWseL9vnQts9o%2bgJ2q0yoB9hDhst6VtpvYnOQ9jat%2fSBiPo6SLdeOmgD%2bJs3m%2bdkgI9hylrHI5MvTQ%2bKFkePrJUEuhZtAuNdxqEFoEUFm%2f4HFgvmYzMCYLis%2bgLQ3JKbM1iTKIom%2b%2fcNc5oJzBGdYHkXJbXEhajYSWg%2bR%2bXXSodXx3tFDCambhfSc89Zf2J53kxFfINm4Jz4AcfiHJVwKobOZqvlz%2f94YDwJnvw5VxU4nPxVB7glfp%2bKGi49Wi1%2fmUOXLymTlqMvhQ0pXlBspCSOuH4ejSE5CoxBXjRK1wCOjU%2fGyoOG4NOvRGqkjZ7EF7g6ovSgpYJGDM2cGoLwKFQOfkiBzyvKbA5%2brGmQWZhc%2byjNb4BIZDTnBchQ3p9%2b%2bd45%2fFwZnM%2bspSOPSIBcpL2v2TkzI%2f1Nt3Y9Pdd4K3aFXJ5E4O8J5pRmG%2fF5p1f9UH6EfXOV3oBL8gDsZaYM9D3Dzjlg17SqBeTwjWtToAxhKLe0OPBnmIcBZ%2bnB6arZXspn05J1OECfeRLgGDKJRzT5QJdxvaE01xlSs7%2bOfiGbuyX9Kku5rxzb2OeouBz%2bnGesSRylC9AboKxJAXXTCIDvYTtVpp%2bYfCv6hibPBGJruP1gISlpJluHVa7dyhmFzH3FPJSPOmmowGhxR5pQQuUxzRd8r1M%2f7AvyVBUoBPh1BbaBjSqUU2gnGxoZY74BexgqrFGr%2f6C%2bnWEbOksJRlvunIE%2fTyF0NZummzLXWAfPq97MWzu0dPj3K0YP48jK462chg8hiaV9US9h%2b0wwPJ%2be7cBWHkL6%2fGPt2K9moJ1r%2bEaSAA2Wb4vBxjTz%2bGV1suXY%2fLG8wJYgJUQdBhdLSxhV%2fGaihw0AxkBkfC2NS5GDk97vzxjGL8BlUUfIIxgU5XsLyDXusfA4wzlJ9Y9%2f5b2MDfRXeYrQATryPjjxp%2b99bylifzBoy09tCinyRgH47tJXPFcRSLwjc35mx8v4KNUh2wSwrMKfBP88zmTIdUL58%2fkFb85suydlxItIS7hm8Geg5RKlDiNYvVDtGD%2feS6qbeoHwMqdY9VCcdCxnu6AvRujyBvZ3mivdMf1Ad8IdeUuC%2bmYaXoytIsfOlmg9Y4s4qHaDVSfMD6KGYua4cKgPILKYQelXGdOEc1qYlT7GEoM6ag3oG%2bpZ6B6MsXgPJyG%2fRsodX2uAbt%2fcpybKbLe1XpBwkKr5wplYU9SAThkjKJb%2fVMKohMyEn3ZLI7xhiV%2f15haNQC%2fHVrsqJ%2fW4xVp4gKBCxvtTQB9YplX5PiOliML34P08rDlMab33Bpo1pA%3d%3d&game_biz=hk4e_global')

#class GenshinStats(commands.Cog):
#
#    def __init__(self, bot):
#        self.bot = bot