# bot.py

import discord, random, os, json, requests
from discord.ext import commands
from dotenv import load_dotenv
from pybooru import Danbooru
import point_system as ps

load_dotenv()

client = Danbooru(site_name='danbooru', username='arizonagreentea', api_key=os.getenv('DANBOORU_APIKEY'))
bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'with ID: {bot.user.id}')
    print()
    print(f'{bot.user} is connected to:')
    print([g.name for g in bot.guilds])
    await bot.change_presence(activity=discord.Game(name='mommy milkers!'))

@bot.command()
async def soojin(ctx):
    embed = discord.Embed(title='Soojin says...', color=0xff5757)
    if ctx.author.id == 336679153644601344:
        embed.add_field(name='shut up kathy', value='<:OMEGALUL:392184053975220244>')
        embed.set_thumbnail(url='https://i.pinimg.com/originals/03/2f/5e/032f5e2c6efeff839ef9670238807ed0.gif')
    else:
        embed.add_field(name=f'henlo {ctx.author.name}!', value='uwu')
        embed.set_thumbnail(url='https://66.media.tumblr.com/7dece74f10c03bd6054601882a4379e9/tumblr_p9pu1v0a7F1vc5dxto2_400.gif')
        embed.color=0x05ff12
    
    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx):
    print(bot.owner_id)
    if ctx.author.id == 126105851504099328:
        await ctx.send(':x: **Stopping bot! Goodbye.**')
        print('Stopping bot!')
        await bot.logout()
    else:
        await ctx.send(':no_entry: **You are not the bot owner!**')

@bot.command()
async def dylan(ctx):
    await ctx.send('dylan is a peepeepoopoo head <:OMEGALUL:392184053975220244>')

@bot.command()
async def ed(ctx):
    if ctx.author.id == 355965807840329729:
        await ctx.send('lmao stfu nerd')
    else:
        await ctx.send('ed gei lmfao <:OMEGALUL:392184053975220244>')

@bot.command()
async def about(ctx):
    await ctx.send('**Developed by yours truly <3**\nhttps://github.com/hi-im-andrew/Sucrose')

# Danbooru

@bot.command()
@commands.is_nsfw()
async def danbooru(ctx, *args):
    banned_tags = {'loli', 'shota', 'furry', 'bestiality', 'toddlercon', 'guro', 'gore', 'scat'}
    
    for tag in banned_tags:
        if tag in args:
            embed = discord.Embed()
            embed.set_image(url='https://c8.alamy.com/comp/B1Y982/businessman-in-jail-B1Y982.jpg')
            await ctx.send(embed=embed)
            return
    
    try:
        count = 0
        def _check():
            nonlocal count
            if count == 10:
                raise AssertionError
            
            raw = client.post_list(limit='1', tags=' '.join(args), random=True)
            for tag in banned_tags:
                if tag in raw[0]['tag_string_general']:
                    print('Banned tag found! Finding new post.')
                    count += 1
                    return _check()
            return raw[0]
        post = _check()
    
    except AssertionError:
        await ctx.send(embed=discord.Embed(title='Error', description='Too many posts with banned tags. Cancelling search.', color=0xff1100))
        return
    except:
        await ctx.send(embed=discord.Embed(title='Error', description='No posts on Danbooru with matching/allowed tags', color=0xff1100))
        return

    #Post details
        #['id', 'created_at', 'uploader_id', 'score', 'source', 'md5', 'last_comment_bumped_at', 'rating',
        # 'image_width', 'image_height', 'tag_string', 'is_note_locked', 'fav_count', 'file_ext', 'last_noted_at',
        # 'is_rating_locked', 'parent_id', 'has_children', 'approver_id', 'tag_count_general', 'tag_count_artist',
        # 'tag_count_character', 'tag_count_copyright', 'file_size', 'is_status_locked', 'pool_string', 'up_score',
        # 'down_score', 'is_pending', 'is_flagged', 'is_deleted', 'tag_count', 'updated_at', 'is_banned', 'pixiv_id',
        # 'last_commented_at', 'has_active_children', 'bit_flags', 'tag_count_meta', 'has_large', 'has_visible_children',
        # 'is_favorited', 'tag_string_general', 'tag_string_character', 'tag_string_copyright', 'tag_string_artist',
        # 'tag_string_meta', 'file_url', 'large_file_url', 'preview_file_url']
    
    if post['rating'] == 's':
        rating = 'Safe'
    elif post['rating'] == 'q':
        rating = 'Questionable'
    elif post['rating'] == 'e':
        rating = 'Explicit'
    
    pid = post['id']

    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.add_field(name='Score', value=post['score'])
    embed.add_field(name='Rating', value=rating)
    embed.add_field(name='Artist', value=post['tag_string_artist'])
    embed.add_field(name='Dimensions', value=str(post['image_height']) + 'x' + str(post['image_width']))
    embed.add_field(name='Post ID', value=pid)
    embed.add_field(name='Link', value=f'[In case image isn\'t displayed](https://danbooru.donmai.us/posts/{pid})')
    embed.set_footer(text=post['tag_string_character'] + ' ' + post['tag_string_general'] + '\nPowered by Pybooru')
    embed.set_image(url=post['file_url'])

    await ctx.send(embed=embed)

# Currency system

@bot.command()
@commands.cooldown(rate=1, per=72000, type=commands.BucketType.user)
async def daily(ctx):
    ps.update_entry(ctx.author.id, 500)
    await ctx.send(embed=discord.Embed(title='C H R <:OMEGALUL:392184053975220244> M I E S', color=0x69f420,
                                       description=f'<:GoodPepeDank:794513428014039060>200 chromosomes added to {ctx.author.name}\'s balance!'))

@bot.command()
async def balance(ctx):
    try:
        bal = ps.get_balance(ctx.author.id)
    except:
        bal = 0
    await ctx.send(embed=discord.Embed(title=f'{ctx.author.name}\'s balance', color=0x69f420,
                                       description=f'<:GoodPepeDank:794513428014039060>{bal} chromosomes'))

@bot.command()
@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
async def gamble(ctx, amount):
    if amount == 'all':
        amount = ps.get_balance(ctx.author.id)
    try:
        amount = int(amount)
    except:
        await ctx.send(embed=discord.Embed(title='Error', color=0xff1100,
                                           description=f':x: Invalid amount!'))
        return
    if amount > ps.get_balance(ctx.author.id):
        await ctx.send(embed=discord.Embed(title='Error', color=0xff1100,
                                           description=f':x: Amount must be less than or equal to your current balance!'))
        return
    elif amount <= 0:
        await ctx.send(embed=discord.Embed(title='Error', color=0xff1100,
                                           description=f':x: Amount must be greater than zero!'))
        return
    
    if random.random() < 0.5:
        ps.update_entry(ctx.author.id, amount)
        await ctx.send(embed=discord.Embed(title='Heads!', color=0x69f420,
                                           description=f'{amount} chromosomes added to {ctx.author.name}\'s balance!\n\
                                               Current balance: <:GoodPepeDank:794513428014039060>{ps.get_balance(ctx.author.id)}'))
    else:
        ps.update_entry(ctx.author.id, -amount)
        await ctx.send(embed=discord.Embed(title='Tails!', color=0xff1100,
                                           description=f'You lost {amount} chromosomes!\n\
                                            Current balance: <:GoodPepeDank:794513428014039060>{ps.get_balance(ctx.author.id)}'))

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    if ctx.author == member:
        await ctx.send(embed=discord.Embed(title='Error', description=f':x: You can\'t give yourself chromosomes!', color=0xff1100))
        return
    if amount > ps.get_balance(ctx.author.id):
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
        ps.update_entry(ctx.author.id, -amount)
        ps.update_entry(member.id, amount)
        await ctx.send(embed=discord.Embed(title=f'Exchange accepted!', color=0x69f420,
                                           description=f'Current balance: <:GoodPepeDank:794513428014039060>{ps.get_balance(ctx.author.id)}'))
    else:
        await ctx.send(embed=discord.Embed(description=f'Exchange declined.', color=0xff1100))

@bot.command()
@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
async def flip(ctx, choice: str):
    heads = {'h', 'head', 'heads'}
    tails = {'t', 'tail', 'tails'}
    if choice.lower() not in heads.union(tails):
        await ctx.send(embed=discord.Embed(title='Error', description=f':x: You must specify heads or tails!', color=0xff1100))
        return
    
    outcome = random.randint(0,1)
    if choice in heads and outcome == 0:
        ps.update_entry(ctx.author.id, 1)
        await ctx.send(embed=discord.Embed(title='Heads!', color=0x69f420,
                                           description=f'<:Pog:689280885027242169> You won 1 chromosome!\n\
                                            Current balance: <:GoodPepeDank:794513428014039060>{ps.get_balance(ctx.author.id)}'))
    elif choice in tails and outcome == 1:
        ps.update_entry(ctx.author.id, 1)
        await ctx.send(embed=discord.Embed(title='Tails!', color=0x69f420,
                                           description=f'<:Pog:689280885027242169> You won 1 chromosome!\n\
                                            Current balance: <:GoodPepeDank:794513428014039060>{ps.get_balance(ctx.author.id)}'))
    elif choice in heads and outcome == 1:
        await ctx.send(embed=discord.Embed(title='Tails!', description='<:Sadge:740811323558068238> Better luck next time!', color=0xff1100))
    elif choice in tails and outcome == 0:
        await ctx.send(embed=discord.Embed(title='Heads!', description='<:Sadge:740811323558068238> Better luck next time!', color=0xff1100))

# Genshin Impact 

@bot.command()
async def character(ctx, name):
    elements = {'Anemo': 0x9ef9cd, 'Geo': 0xf4d862, 'Electro': 0xc36dff, 'Dendro': 0xb1ea26, 'Hydro': 0x079fff, 'Pyro': 0xff8739, 'Cryo': 0xccfffe}
    
    raw = requests.get(f'https://api.genshin.dev/characters/{name}')
    data = raw.json()
    
    embed = discord.Embed(name=f'{data["name"]}, {data["title"]}', description=''.join([':star:' for i in range(0, int(data["rarity"]) + 1)]), color=elements[data["vision"]])
    embed.set_footer(text='Powered by genshin.dev')
    embed.add_field(name='Vision', value=data["vision"])
    embed.add_field(name='Weapon', value=data["weapon"])
    embed.add_field(name='Gender', value=data["gender"])
    embed.add_field(name='Nation', value=data["nation"])
    embed.add_field(name='Affiliation', value=data["affiliation"])
    embed.add_field(name='Constellation', value=data["constellation"])
    bday = data["birthday"].split('-')
    embed.add_field(name='Birthday', value=f'{bday[1]}/{bday[2]}')
    embed.add_field(name='Bio', value=data["description"], inline=False)
    await ctx.send(embed=embed)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(title='Error', description=str(error), color=0xff1100))
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(embed=discord.Embed(title='Error', description='Channel must be marked as NSFW!', color=0xff1100))

bot.run(os.getenv('DISCORD_TOKEN'))