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

@bot.hybrid_command()
@commands.is_owner()
async def send_embed(ctx, guild_id: int, channel_id: int, *, content: str):
    """
    Send an embed to a channel
    Content should be in JSON format, sent inside a code block.
    """
    try:
        # Strip code block formatting if present
        if content.startswith("```") and content.endswith("```"):
            content = content[3:-3].strip()

        # Load content as JSON
        content_dict = json.loads(content)
        embed = discord.Embed.from_dict(content_dict)

        # Get guild and channel
        guild = bot.get_guild(guild_id)
        if guild is None:
            await ctx.send(f"❌ Guild with ID `{guild_id}` not found.")
            return

        channel = guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            await ctx.send(f"❌ Channel with ID `{channel_id}` not found or invalid.")
            return

        # Send embed
        await channel.send(embed=embed)
        await ctx.send(f'✅ Embed sent to {guild.name} → #{channel.name}')
    
    except json.JSONDecodeError:
        await ctx.send("❌ Invalid JSON format. Ensure the content is valid JSON.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


        content_dict = json.loads(content)
        embed = discord.Embed.from_dict(content_dict)


@bot.event
async def on_ready():
    assert bot.user is not None # to silence lsp
    print(f'Logged in as {bot.user.name}')
    await load_cogs()

    print('Bot is ready')

bot.run(TOKEN)
