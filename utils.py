import sqlite3
import math
DB_PATH = "tutorial.db"

def get_user_by_name(name: str):
    """
    Fetches all user profile data based on their name.
    Returns a list of dictionaries (since multiple users could share a name).
    """
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM profiles WHERE name = ?", (name,))
        rows = cur.fetchall()
        
        # Convert SQLite Row objects to standard Python dictionaries for easier use
        return [dict(row) for row in rows]


def get_user_matches(user_id: str):
    """
    Fetches all matches for a specific user_id.
    It returns the match_id and the complete profile of the matched person.
    """
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        # We join the profiles table to get the OTHER user's profile data
        query = """
            SELECT 
                m.id AS match_id,
                p.*
            FROM matches m
            JOIN profiles p ON 
                (m.user1_id = ? AND p.user_id = m.user2_id)
                OR 
                (m.user2_id = ? AND p.user_id = m.user1_id)
        """
        cur.execute(query, (user_id, user_id))
        rows = cur.fetchall()
        
        return [dict(row) for row in rows]


def get_conversation_history(match_id: str):
    """
    Bonus: Fetches the entire message history for a given match.
    """
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        query = """
            SELECT m.content, m.created_at
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.match_id = ?
            ORDER BY m.created_at ASC
        """
        cur.execute(query, (match_id,))
        rows = cur.fetchall()
        
        return [dict(row) for row in rows]
def calculate_distance(lat1: float, lat2: float, long1: float, long2: float) -> float:
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlong = math.radians(long2 - long1)

    # Apply the Haversine formula
    a = (math.sin(dlat / 2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlong / 2)**2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    
    # Optional: Round to 2 decimal places for cleaner output
    return round(distance, 2)
