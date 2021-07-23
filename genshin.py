# genshin.py

import discord, requests
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
        
        embed = discord.Embed(title=f'{data["name"]}', description='Max Rarity: ' + ''.join([':star:' for i in range(0, data["max_rarity"])]), color=colors[data["max_rarity"]])
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
