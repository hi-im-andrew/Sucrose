# bot.py

import discord, os
from discord.ext import commands, menus
from dotenv import load_dotenv

from danbooru import DanbooruCog
from genshin import Genshin
from point_system import Currency

load_dotenv()
bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}, with ID {bot.user.id}\n')
    print(f'{bot.user} is connected to:')
    print([g.name for g in bot.guilds])
    await bot.change_presence(activity=discord.Game(name='mommy milkers!'))

bot.add_cog(DanbooruCog(bot))
bot.add_cog(Genshin(bot))
bot.add_cog(Currency(bot))

bot.run(os.getenv('DISCORD_TOKEN'))