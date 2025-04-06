# birthday command
# sends the birthday song

import discord
from discord.ext import commands

class WhoAreYou(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Responds to Noda's happy birthday message with a birthday song."""
        noda_id = 875455409853460550

        if message.author.id == noda_id and "Happy birthday" in message.content:
            response = "[... Happy birthday, I guess.](https://open.spotify.com/track/20EIvCTkNuaFU0vB6NG8eo)"
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(WhoAreYou(bot))
