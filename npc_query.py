import sqlite3
import math
import re

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def search_by_npc (name):

    name = re.sub(r"[^A-Za-z]", "", name)
    name = name.capitalize()

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

def heart_calc(hearts, max_hearts):

    hearts = re.sub(r"[^0-9]", "", hearts)
    hearts = int(hearts)

    full_heart_points = 250
    loved = 80
    liked = 45
    neutral = 20

    empty_hearts = max_hearts - hearts
    points_needed = empty_hearts * full_heart_points

    loved_item_qty = math.ceil(points_needed / loved)
    loved_min_weeks = math.ceil(points_needed / (loved * 2))

    liked_item_qty = math.ceil(points_needed / liked)
    liked_min_weeks = math.ceil(points_needed / (liked * 2))

    neutral_item_qty = math.ceil(points_needed / neutral)
    neutral_min_weeks = math.ceil(points_needed / (neutral * 2))

    return {
        "points_needed": points_needed,
        "loved_qty": loved_item_qty,
        "loved_weeks": loved_min_weeks,
        "liked_qty": liked_item_qty,
        "liked_weeks": liked_min_weeks,
        "neutral_qty": neutral_item_qty,
        "neutral_weeks": neutral_min_weeks
    }
    
def all_npcs():
    cursor.execute("""
        SELECT npc_name
        FROM npcs
    """)
    results = cursor.fetchall()
    return [row['npc_name'] for row in results]


def preferences_by_npc(name):

    name = re.sub(r"[^A-Za-z]", "", name)
    name = name.capitalize()
    
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

    preference_info = {
        'Loved' : [],
        'Liked' : [],
        'Neutral' : [],
        'Disliked' : [],
        'Hated' : [],
    }

    for row in preferences:
        npc_pref = row['npc_pref']
        item_name = row['item_name']

        if npc_pref == "loved":
            preference_info['Loved'].append(item_name)
        elif npc_pref == "liked":
            preference_info['Liked'].append(item_name)
        elif npc_pref == "disliked":
            preference_info['Disliked'].append(item_name)
        elif npc_pref == "hated":
            preference_info['Hated'].append(item_name)

    for row in preferences:
        universal_pref = row['universal_pref']
        item_name = row['item_name']

        if universal_pref and all(item_name not in lst for lst in preference_info.values()):
            if universal_pref == "loved":
                preference_info['Loved'].append(item_name)
            elif universal_pref == "liked":
                preference_info['Liked'].append(item_name)
            elif universal_pref == "disliked":
                preference_info['Disliked'].append(item_name)
            elif universal_pref == "hated":
                preference_info['Hated'].append(item_name)

    for row in preferences:
            item_name = row['item_name']
            if all(item_name not in lst for lst in preference_info.values()):
                preference_info['Neutral'].append(item_name)

    return preference_info