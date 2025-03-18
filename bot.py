import discord
from discord.ext import commands
import dotenv
import os
import json

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN') or ''

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)

async def load_cogs():
    await bot.load_extension('wordbomb.wordbomb')

# hybrid command for syncing
@bot.hybrid_command()
@commands.is_owner()
async def sync(ctx):
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
    await ctx.send('Synced!')


# lets owner send an embed to a channel
@bot.hybrid_command()
@commands.is_owner()
async def send_embed(ctx, guild_id: int, channel_id: int, content: str):
    """
    Send an embed to a channel
    Content will be in JSON format, with the following keys:
    - title (str)
    - description (str)
    - color (int)
    """
    
    try:
        # load content as json
        content_dict = json.loads(content)
        embed = discord.Embed.from_dict(content_dict)

        # get guild and channel
        guild = bot.get_guild(guild_id)
        assert(guild is not None)
        channel = guild.get_channel(channel_id)
        assert(isinstance(channel, discord.TextChannel))

        # send embed
        await channel.send(embed=embed)
        await ctx.send(f'Embed sent to {guild.name} → #{channel.name}')
    except Exception as e:
        await ctx.send(f'Error: {e}')
    


@bot.event
async def on_ready():
    assert bot.user is not None # to silence lsp
    print(f'Logged in as {bot.user.name}')
    await load_cogs()

    print('Bot is ready')

bot.run(TOKEN)
