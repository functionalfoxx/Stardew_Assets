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

def time_to_minutes(HH_mm):
    hour_str, minute_str = HH_mm.split(":")
    hour = int(hour_str)
    minute = int(minute_str)

    total_minutes = (hour - 6) * 60 + minute 

    if total_minutes < 0:
        total_minutes += 24 * 60

    return total_minutes

cursor.execute("""
    SELECT *
    FROM npc_schedules
""")

npc_schedules = []

for row in cursor.fetchall():
    schedule_id = row["schedule_id"]
    npc_id = row["npc_id"]
    location_id = row["location_id"]
    HH_mm = row["time"]
    schedule_description = row["schedule_description"]
    
    time_as_minutes = time_to_minutes(HH_mm)
    
    npc_schedules.append({
        "Schedule ID": schedule_id,
        "NPC ID": npc_id,
        "Location ID": location_id,
        "Time": HH_mm,
        "Time As Minutes": time_as_minutes,
        "Schedule Description": schedule_description
    })

for schedule in npc_schedules:
    loc_id = schedule["Location ID"]
    
    schedule["Location Name"] = locations[loc_id]["Location Name"]
    schedule["Is Building?"] = locations[loc_id]["Is Building?"]
    schedule["Is Map Connection?"] = locations[loc_id]["Is Map Connection?"]
    schedule["Is Teleport?"] = locations[loc_id]["Is Teleport?"]
    schedule["Location Column"] = locations[loc_id]["Location Column"]
    schedule["Location Row"] = locations[loc_id]["Location Row"]

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