# emotemanager.py

from http import client
from multiprocessing.connection import Client
import discord, requests, re, io, aiohttp
from interactions import Guild, User
from discord.ext import commands
from PIL import Image, ImageSequence

class EmoteManager(commands.cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def add7tv(self, ctx, name, id: str):
        if ctx.author.guild_permissions.manage_emojis:
            if not re.match(r'^\w{2,32}$', name):
                await ctx.send(embed=discord.Embed(title='Error', description='Emote name must be at 2-32 characters long and can only contain alphanumeric characters and underscores', color=0xff1100))
                return

            if id.isalnum() and str.length(id) == 24:
                pass
            elif re.match(r'^(https:\/\/)?7tv.app\/emotes\/[a-z0-9]{24}$', id):
                id = id.strip('/')[-1]
            else:
                await ctx.send(embed=discord.Embed(title='Error', description='Emote ID must be a valid 7TV emote ID or link', color=0xff1100))
                return

            def _isGif(image):
                try:
                    file = Image.open(image)
                    index = 0
                    for frame in ImageSequence.Iterator(file):
                        index += 1
                    if index > 1:
                        file.info.pop('background', None)
                        file.save(f'{name}.gif', 'gif', save_all=True)
                        return file
                    else:
                        return False
                except:
                    return False
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://cdn.7tv.app/emote/{id}/4x') as response:
                    try:
                        emoji = io.BytesIO(await response.read())
                        if _isGif(emoji):
                            
                        
                        await ctx.guild.create_custom_emoji(name=name, image=emoji, reason=f'Added by {ctx.author.User.name}')
                    except:
                        
            
        else:
            await ctx.send(embed=discord.Embed(title='Error', description='You must have the "Manage Emojis" permission!', color=0xff1100))
    
    @commands.command()
    async def removeemote(ctx, emoji: discord.Emoji):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            await ctx.send(embed=discord.Embed(title='Success', description='Removed {emoji}!', color=0xff1100))
            await emoji.delete()