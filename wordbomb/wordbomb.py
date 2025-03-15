import discord
from discord.ext import commands
import random
import sqlite3

class WordBomb(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('wordbomb/words.txt', 'r') as f:
            self.words = f.readlines()
        # strip words
        self.words = [word.strip() for word in self.words]
        self.db = sqlite3.connect('wordbomb/wordbomb.db')
        self.c = self.db.cursor()

    async def get_word(self):
        word = random.choice(self.words)
        word_length = len(word)

        # get random substring
        # ideally between 3-5 characters
        # check word length
        # if word length is less than 5
        # then substring length is word length
        if word_length < 5:
            substring_length = word_length
        else:
            substring_length = random.randint(3, 5)
        
        # get random start index
        start = random.randint(0, word_length - substring_length)
        end = start + substring_length
        substring = word[start:end]

        return word, substring

    async def filter_words(self, substring):
        # find all words that contain the substring
        return [word for word in self.words if substring in word]

    async def check_answer(self, guild_id, answer):
        # clean answer
        answer = answer.strip().lower()

        # get last substring
        self.c.execute("SELECT last_substring, last_word FROM guilds WHERE id=?", (guild_id,))
        last_substring, last_word = self.c.fetchone()

        # check if answer is valid
        # needs to both contain the last substring
        # and be in the list of words
        # then return the result and the word
        return last_substring in answer and answer in self.words, last_word

    async def update_score(self, user_id, guild_id):
        # get user's score
        self.c.execute("SELECT score FROM scores WHERE user_id=? and guild_id=?", (user_id, guild_id))
        score = self.c.fetchone()

        # if the user doesn't have a score
        if not score:
            # insert the user into the table
            self.c.execute("INSERT INTO scores (user_id, guild_id, score) VALUES (?, ?, ?)", (user_id, guild_id, 1))
        else:
            # update the user's score
            self.c.execute("UPDATE scores SET score=? WHERE user_id=? and guild_id=?", (score[0] + 1, user_id, guild_id))

        # commit changes
        self.db.commit()
    
    async def check_for_game(self, guild_id, channel_id):
        self.c.execute("SELECT * FROM guilds WHERE id=? and channel_id=?", (guild_id, channel_id))
        return self.c.fetchone()

    @commands.hybrid_command()
    async def start(self, ctx):
        """
        Start a game of Word Bomb in the current channel.
        """
        # get guild id, channel id
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        # if the game is already started in this channel
        if await self.check_for_game(guild_id, channel_id):
            await ctx.send("Game already started in this server!")
            return
        
        # get random word and substring
        word, substring = await self.get_word()

        # insert guild into database
        self.c.execute(
            "INSERT INTO guilds (id, name, channel_id, last_word, last_substring) VALUES (?, ?, ?, ?, ?)",
            (guild_id, ctx.guild.name, channel_id, word, substring)
        )

        # commit changes
        self.db.commit()

        # send message
        embed = discord.Embed(
            title="Word Bomb",
            description=f"Game started! The substring is `{substring}`."
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def get_score(self, ctx, userid: discord.User = None):
        """
        Get the score of a user in the current channel.
        """
        # get guild id, channel id
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        # get user id
        if not userid:
            userid = ctx.author

        # get user's score
        self.c.execute("SELECT score FROM scores WHERE user_id=? and guild_id=?", (userid.id, guild_id))
        score = self.c.fetchone()

        # send message
        if not score:
            await ctx.send("User has no score!")
        else:
            await ctx.send(f"{userid.mention} has a score of {score[0]}!")

    @commands.hybrid_command()
    async def get_hint(self, ctx):
        """
        Send an ephemeral message with the current word.
        """
        # get guild id, channel id
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        # get last word
        self.c.execute("SELECT last_word FROM guilds WHERE id=? and channel_id=?", (guild_id, channel_id))
        last_word = self.c.fetchone()

        # send message
        if not last_word:
            await ctx.send("No game started in this server!")
        else:
            await ctx.send(f"The last word was `{last_word[0]}`.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        # check if the message is from a bot
        if message.author.bot:
            return

        # get guild id, channel id
        guild_id = message.guild.id
        channel_id = message.channel.id

        # check if the game is started in this channel
        if not await self.check_for_game(guild_id, channel_id):
            return

        # check if the message is the correct answer
        valid, last_word = await self.check_answer(guild_id, message.content)
        if valid:
            # get new word and substring
            word, substring = await self.get_word()

            # update database
            self.c.execute(
                "UPDATE guilds SET last_word=?, last_substring=? WHERE id=? and channel_id=?",
                (word, substring, guild_id, channel_id)
            )

            # update score
            await self.update_score(message.author.id, guild_id)

            # commit changes
            self.db.commit()

            # send message
            embed = discord.Embed(
                title="Word Bomb",
                description=f"Correct! The last word was `{last_word}`. The new substring is `{substring}`."
            )
            await message.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(WordBomb(client))
