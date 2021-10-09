# danbooru.py

import discord, os, random
from discord.ext import commands
from dotenv import load_dotenv
from pybooru import Danbooru

client = Danbooru(site_name='danbooru', username=os.getenv('DANBOORU_USER'), api_key=os.getenv('DANBOORU_APIKEY'))

class DanbooruCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_nsfw()
    async def danbooru(self, ctx, *args):
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
                        print(f'{ctx.author.name}: Banned tag found! Finding new post. {ctx.message.created_at}')
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
