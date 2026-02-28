import sqlite3
import re

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def search_by_npc (name):

    cursor.execute("""
        SELECT
            npc_name, 
            address,
            birthday_season,
            birthday_day,
            can_marry,
            npc_wiki_url,
            trivia_fact
        FROM npcs
        WHERE npc_name =?
    """, (name,))

    profile = cursor.fetchone()

    cursor.execute("""
        SELECT
            npcs.npc_name,
            items.item_name,
            npc_preferences.preference AS npc_pref,
            universal_preferences.preference AS universal_pref
        FROM npcs
        CROSS JOIN items
        LEFT JOIN npc_preferences
            ON npcs.npc_id = npc_preferences.npc_id
            AND npc_preferences.item_id = items.item_id
        LEFT JOIN universal_preferences
            ON items.item_id = universal_preferences.item_id
        WHERE npcs.npc_name = ?
    """, (name,))

    preferences = cursor.fetchall()

    loved_items = []
    personal_overrides = []

    for row in preferences:
        npc_pref = row['npc_pref']
        item_name = row['item_name']

        if npc_pref == "loved":
            loved_items.append(item_name)
        elif npc_pref in ("liked", "disliked", "hated"):
            personal_overrides.append(item_name)

    for row in preferences:
        universal_pref = row['universal_pref']
        item_name = row['item_name']

        if universal_pref == "loved" and item_name not in personal_overrides and item_name not in loved_items:
            loved_items.append(item_name)

    combined = dict(profile)
    combined['loved_items'] = loved_items

    return combined





"""

||| NPC QUERY SCREEN |||

FROM NPC PROFILE
    TYPE 1: SEE NPC SCHEDULE FOR THE DAY

    TYPE 2 : SEE HOW MANY MORE ITEMS ARE NEEDED FOR MAX FRIENDSHIP HEARTS
        "HOW MANY HEARTS DO YOU CURRENTLY HAVE WITH [NPC NAME]?"
        "YOU NEED X MORE LOVED ITEMS, X MORE LIKED ITEMS, OR X MORE NEUTRAL ITEMS TO MAX FRIENDSHIP HEARTS"
        "YOU NEED X MORE LOVED ITEMS, X MORE LIKED ITEMS, OR X MORE NEUTRAL ITEMS TO MAX MARRIAGE HEARTS" 
            (ONLY IF CAN MARRY NPC)
        "[FLAVOR TEXT REFLECTING CURRENT FRIENDSHIP STATUS FOR 1-3 HEARTS, 4-6 HEARTS, 7-9 HEARTS, 10+ HEARTS]"

        TYPE B : GO BACK TO THE PREVIOUS SCREEN
        TYPE M : RETURN TO THE MAIN SCREEN

    TYPE 3 : SEE ALL OF [NPC NAME]'S GIFT PREFERENCES
        TYPE 1 : SEE LOVED GIFTS               ||| LIST ALL MATCHING GIFTS IN ABC ORDER |||
        TYPE 2 : SEE LIKED GIFTS               ||| SAME FORMAT FOR EACH PREFERENCE TYPE |||
        TYPE 3 : SEE NEUTRAL GIFTS             ||| GUI-ISH DISPLAY ACROSS PROJECT |||
        TYPE 4 : SEE DISLIKED GIFTS
        TYPE 5 : SEE HATED GIFTS

        TYPE B : GO BACK TO THE PREVIOUS SCREEN
        TYPE M : RETURN TO THE MAIN SCREEN

---------------------------------------------------

TYPE 2 : SEE ALL STARDEW GIFTABLE NPCS
    [LISTS ALL NPCS IN ABC ORDER"]

    TYPE B : GO BACK TO THE PREVIOUS SCREEN
    TYPE M : RETURN TO THE MAIN SCREEN

   """