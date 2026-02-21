import sqlite3
import uuid

# 1. Connect to the database (creates tutorial.db if it doesn't exist)
con = sqlite3.connect("tutorial.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

# 2. Initialize the Schema
print("Creating tables...")
cur.executescript("""
    CREATE TABLE IF NOT EXISTS matches (
        id TEXT PRIMARY KEY,
        user1_id TEXT NOT NULL,
        user2_id TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        looking_for TEXT,
        bio TEXT,
        latitude REAL,
        longitude REAL
    );
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        match_id TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        content TEXT,
        created_at TEXT,
        deleted_at TEXT
    );
""")

# 3. Seed the Profiles
print("Inserting test profiles...")
profiles_data = [
    ("user-1", "Alice", 28, "woman", "relationship", "I love hiking, cooking, and reading sci-fi.", 40.7128, -74.0060),
    ("user-2", "Bob", 30, "man", "relationship", "Big fan of hiking, board games, and cooking new recipes.", 40.7580, -73.9855),
    ("user-3", "Charlie", 26, "man", "casual", "Coffee addict. Let's find the best espresso in town.", 40.7306, -73.9866),
    ("user-4", "Diana", 29, "woman", "relationship", "Movie buff, love exploring art galleries and trying street food.", 40.7282, -73.9943),
    ("user-5", "Eve", 24, "woman", "casual", "Looking for someone to go to live rock concerts with!", 40.7484, -73.9857),
    ("user-6", "Frank", 32, "man", "relationship", "Quiet nights in, cooking pasta, and watching documentaries.", 40.7112, -74.0055)
]

cur.executemany(
    "INSERT OR IGNORE INTO profiles VALUES (?,?,?,?,?,?,?,?)", 
    profiles_data
)

# 4. Seed Matches and Conversations
print("Inserting test matches and conversations...")
matches_data = [
    ("match-1", "user-1", "user-2"), # Alice and Bob
    ("match-2", "user-3", "user-5"), # Charlie and Eve
]
cur.executemany("INSERT OR IGNORE INTO matches VALUES (?,?,?)", matches_data)

conversations_data = [
    ("conv-1", "match-1"),
    ("conv-2", "match-2"),
]
cur.executemany("INSERT OR IGNORE INTO conversations VALUES (?,?)", conversations_data)

# 5. Seed Messages
print("Inserting test messages...")
messages_data = [
    (str(uuid.uuid4()), "conv-1", "Hey Bob, want to grab coffee and play Catan sometime?"),
    (str(uuid.uuid4()), "conv-1", "I'd love that Alice! Do you know any good cafes nearby?"),
    (str(uuid.uuid4()), "conv-2", "Hey Eve! What was the last concert you went to?")
]

# We iterate here to use the SQLite datetime('now') function properly for each row
for msg_id, conv_id, content in messages_data:
    cur.execute(
        "INSERT OR IGNORE INTO messages VALUES (?,?,?,datetime('now'),NULL)",
        (msg_id, conv_id, content)
    )

# 6. Commit and Close
con.commit()
con.close()
print("Success! Database seeded and ready to go.")


