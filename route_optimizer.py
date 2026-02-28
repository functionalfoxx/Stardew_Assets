import sqlite3

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM locations
""")
locations = {}

for row in cursor.fetchall():
    location_id = row["location_id"]
    locations[location_id] = {
        "Location Name": row["location_name"],
        "Is Building?": row["building"],
        "Is Map Connection?": row["map_connection"],
        "Is Teleport?": row["teleport"],
        "Location Column": row["location_column"],
        "Location Row": row["location_row"]
    }

"""

QUESTION 1 :    DO YOU HAVE THESE CHARACTERS UNLOCKED?
WIZARD, KENT, MINES DWARF, SANDY, KROBUS, LEO
EXAMPLE: Y, Y, Y, N, Y, N"

QUESTION 2 :    HOW MANY FRIENDSHIP HEARTS DO YOU HAVE WITH EACH OF THESE CHARACTERS?
ABIGAIL, SEBASTIAN, HALEY, ALEX, ELLIOTT, LEAH, LEO, PENNY, SAM
EXAMPLE: 5, 9, 3, 5, 10, 7, 0, 3, 5

QUESTION 3 :    HAVE YOU COMPLETED THESE GAME PROGRESS POINTS?
BUS SERVICE, BEACH BRIDGE REPAIR, COMMUNITY CENTER
EXAMPLE: Y, Y, N"

QUESTION 4 :    WHAT DAY IS IT?
PROVIDE THE WEEKDAY, SEASON, DATE, AND WEATHER
EXAMPLE: WEDNESDAY, SUMMER, 22, R

----------

RETURNS LIST OF ALL NPCS IN ORDER OF ROUTE OPTIMIZATION STARTING AT 7:00 THROUGH 0:00 IN 24 HOUR FORMAT
EACH LINE SHOWS NPC NAME, LAST TIME LOCATION_DESCRIPTION AND NEXT LOCATION_DESCRIPTION
CHECK IF LANDS ON AN EVENT DAY THAT REMOVES CHARACTER SCHEDULE

"""