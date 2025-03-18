import discord
from discord.ext import commands
import dotenv
import os

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
@commands.hybrid_command()
@commands.is_owner()
async def sync(ctx):
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
    await ctx.send('Synced!')

@bot.event
async def on_ready():
    assert bot.user is not None # to silence lsp
    print(f'Logged in as {bot.user.name}')
    await load_cogs()

    print('Bot is ready')

bot.run(TOKEN)
