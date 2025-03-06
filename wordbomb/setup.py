import sqlite3

db = sqlite3.connect('wordbomb.db')
c = db.cursor()

# guild table
c.execute("""
CREATE TABLE guilds (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    channel_id INTEGER NOT NULL,
    last_word TEXT NOT NULL,
    last_substring TEXT NOT NULL
)
""")

# user table
c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

# score table
c.execute("""
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (guild_id) REFERENCES guilds(id)
)
""")

db.commit()
db.close()