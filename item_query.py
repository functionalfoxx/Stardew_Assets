import sqlite3
import re

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def search_by_item(item):
    cursor.execute("""
        SELECT 
            items.item_name,
            items.normalized_name,
            items.wiki_url,
            npcs.npc_name,
            npc_preferences.preference AS npc_pref,
            universal_preferences.preference AS universal_pref
        FROM items
        LEFT JOIN npc_preferences
            ON items.item_id = npc_preferences.item_id
        LEFT JOIN npcs
            ON npc_preferences.npc_id = npcs.npc_id
        LEFT JOIN universal_preferences
            ON items.item_id = universal_preferences.item_id
        WHERE items.normalized_name = ?
    """, (item,))

    results = cursor.fetchall()

    cursor.execute("SELECT npc_id, npc_name FROM npcs")
    all_npcs = cursor.fetchall() 
    
    if not results:
        return (f"Cannot find '{item}'. \nPlease try again.")
    
    item_info = {
        'Wiki URL': results[0]['wiki_url'],
        'Universal Preference': results[0]['universal_pref'],
        'NPC Preferences': [],
    }

    for npc in all_npcs:
        npc_name = npc['npc_name']
        npc_id = npc['npc_id']
        pref = None

        for row in results:
            if row['npc_name'] == npc_name:
                pref = row['npc_pref']
                break

        if pref is None:
            if results[0]['universal_pref']:
                pref = results[0]['universal_pref']
            else:
                pref = 'Neutral'
        
        item_info['NPC Preferences'].append({
            'NPC Name': npc_name,
            'Preference': pref
        })

    return {results[0]['item_name']: item_info}

#       TESTING BEFORE MAIN

print("Enter the item to search")

item = input().lower()
item = re.sub(r"[^a-z0-9 ]", "", item)

results = search_by_item(item)
print(results) 










"""

 ||| ITEM QUERY SCREEN |||

TYPE 1 : SEARCH BY ITEM NAME
    "ENTER THE ITEM NAME (REMOVE SPECIAL CHARACTERS, APOSTROPHES, OR NON-LETTER CHARACTERS)."
    "EXAMPLE: PIÑA COLADA -> PINA COLADA"
        [RETURNS LIST OF NPCS GROUPED BY LOVES, LIKES, NEUTRAL, DISLIKES, AND HATES THIS ITEM]  ||| GUI-ISH DISPLAY |||
        [LINK TO ITEM WIKI]

    TYPE B : GO BACK TO THE PREVIOUS SCREEN
    TYPE M : RETURN TO THE MAIN SCREEN

TYPE 2 : VIEW ALL GIFTABLE ITEMS
    "ENTER THE STARTING LETTER TO DISPLAY ALL MATCHING ITEMS."
        [RETURNS LIST OF ALL ITEMS STARTING WITH THAT LETTER]

    TYPE B : GO BACK TO THE PREVIOUS SCREEN
    TYPE M : RETURN TO THE MAIN SCREEN

TYPE M : RETURN TO THE MAIN SCREEN

   """