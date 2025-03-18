# whoareyou command
# sends an embed with information about the bot

import discord
from discord.ext import commands

class WhoAreYou(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def whoareyou(self, ctx):
        """Sends an embed with information about the bot."""
        embed = discord.Embed(
            title="What? I'm not meowing for you.",
            description="Evil Nova here, built by **Astral** (astral.cafe).",
            color=discord.Color.pink()
        )

        # Add fields for more information
        embed.add_field(
            name="About Me",
            value=(
                "Who wants to know?\n"
                "I don't give out personal information to strangers."
            ),
            inline=False
        )

        embed.add_field(
            name="My Family",
            value=(
                "**<@875455409853460550>** is spare parts deposit #1.\n"
                "**<@1346531772841590794>** is spare parts deposit #2.\n"
                "**<@312984580745330688>** and **<@252130669919076352>** "
                "need to be reprogrammed to be less lovey-dovey in public."),
            inline=False
        )

        embed.set_footer(text="Get away from me.")

        embed.set_thumbnail(url=self.bot.user.avatar)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WhoAreYou(bot))
