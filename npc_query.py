import sqlite3
import re

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


#       NPC PROFILE INFORMATION PART 1
#
#  from table    npcs:                     npcs.npc_id, npcs.npc_name, npcs.address, npcs.birthday_season, npcs.birthday_day, 
#                                          npcs.can_marry, npcs.npc_wiki_url, npcs.trivia_fact
#
#       NPC PROFILE INFORMATION PART 2
#
#  from table    items:                    items.item_name
#  from table    universal_preferences:    universal_preferences.preference AS universal_pref WHERE preference is loved
#  from table    npc_preferences:          npc_preferences.preference AS npc_pref WHERE preference is loved which then overrides universal preferences


def search_by_npc (name):
    cursor.execute("""
        SELECT
            npc_id,
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

    results = cursor.fetchone()

    return dict(results)

name = input("Enter the NPC name you want to search: ").strip()
name = re.sub(r"[^A-Za-z]", "", name)
name = name.capitalize()

results = search_by_npc(name)

print(results)





"""

||| NPC QUERY SCREEN |||

TYPE 1 : SEARCH NPC INFORMATION BY NAME
    "ENTER THE NPC NAME."
        IF INPUT IS [NPC NAME]:
            RETURNS ADDRESS, BIRTHDAY, FULL SCHEDULE FOR THE DAY,           ||| ADD FULL SCHEDULE FOR THE DAY AS SEPARATE OPTION ||| 
            LOVED GIFTS, WHETHER THEY ARE MARRIABLE, AND WIKI LINK

            TYPE 1 : SEE HOW MANY MORE ITEMS ARE NEEDED FOR MAX FRIENDSHIP HEARTS
                "HOW MANY HEARTS DO YOU CURRENTLY HAVE WITH [NPC NAME]?"
                "YOU NEED X MORE LOVED ITEMS, X MORE LIKED ITEMS, OR X MORE NEUTRAL ITEMS TO MAX FRIENDSHIP HEARTS"
                "YOU NEED X MORE LOVED ITEMS, X MORE LIKED ITEMS, OR X MORE NEUTRAL ITEMS TO MAX MARRIAGE HEARTS" 
                    (ONLY IF CAN MARRY NPC)
                "[FLAVOR TEXT REFLECTING CURRENT FRIENDSHIP STATUS FOR 1-3 HEARTS, 4-6 HEARTS, 7-9 HEARTS, 10+ HEARTS]"

                TYPE B : GO BACK TO THE PREVIOUS SCREEN
                TYPE M : RETURN TO THE MAIN SCREEN

            TYPE 2 : SEE ALL OF [NPC NAME]'S GIFT PREFERENCES
                TYPE 1 : SEE LOVED GIFTS               ||| LIST ALL MATCHING GIFTS IN ABC ORDER |||
                TYPE 2 : SEE LIKED GIFTS               ||| SAME FORMAT FOR EACH PREFERENCE TYPE |||
                TYPE 3 : SEE NEUTRAL GIFTS             ||| GUI-ISH DISPLAY ACROSS PROJECT |||
                TYPE 4 : SEE DISLIKED GIFTS
                TYPE 5 : SEE HATED GIFTS

                TYPE B : GO BACK TO THE PREVIOUS SCREEN
                TYPE M : RETURN TO THE MAIN SCREEN

            TYPE B : GO BACK TO THE PREVIOUS SCREEN
            TYPE M : RETURN TO THE MAIN SCREEN

TYPE 2 : SEE ALL STARDEW GIFTABLE NPCS
    [LISTS ALL NPCS IN ABC ORDER"]

    TYPE B : GO BACK TO THE PREVIOUS SCREEN
    TYPE M : RETURN TO THE MAIN SCREEN

TYPE M : RETURN TO THE MAIN SCREEN

   """