import sqlite3
import math

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

STARTING_HOUR = 6
START_LOCATION_ID = 18
TILES_PER_10_MIN = 35
GAME_TIME_INCREMENTS = 10


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

    total_minutes = (hour - STARTING_HOUR) * 60 + minute 

    if total_minutes < 0:
        total_minutes += 24 * 60

    return total_minutes

def minutes_to_time(minutes):
    hour = STARTING_HOUR + (minutes // 60)
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"

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

current_column = locations[START_LOCATION_ID]["Location Column"]
current_row = locations[START_LOCATION_ID]["Location Row"]

current_time = time_to_minutes(STARTING_HOUR)                                          

route = []

unvisited_npcs = npc_schedules.copy()
visited_npcs = []

next_npc = unvisited_npcs.pop(0)
visited_npcs.append(next_npc)

def get_available_npcs(unvisited_npcs, current_time):
    
    available_npcs = []
    
    for npc in unvisited_npcs:

        if npc["Time As Minutes"] >= current_time:
            available_npcs.append(npc)
    
    return available_npcs

def distance(current_col, current_row, target_col, target_row):
    return abs(current_col - target_col) + abs(current_row - target_row)

available_npcs = get_available_npcs(unvisited_npcs, current_time)

for npc in available_npcs:
    npc["Distance From Current"] = distance(
        current_col = current_column,
        current_row = current_row,
        target_col = npc["Location Column"],
        target_row = npc["Location Row"]
    )

while unvisited_npcs:

    available_npcs = get_available_npcs(unvisited_npcs, current_time)

    if not available_npcs:
        break

    for npc in available_npcs:
        npc["Distance From Current"] = distance(
            current_col = current_column,
            current_row = current_row,
            target_col = npc["Location Column"],
            target_row = npc["Location Row"]
        )

    next_npc = available_npcs[0]

    for npc in available_npcs:
        if npc["Distance From Current"] < next_npc["Distance From Current"]:
            next_npc = npc

    distance_tiles = next_npc["Distance From Current"]
    travel_time = (distance_tiles / TILES_PER_10_MIN) * GAME_TIME_INCREMENTS
    travel_time = math.ceil(travel_time / GAME_TIME_INCREMENTS) * GAME_TIME_INCREMENTS
    arrival_time = current_time + travel_time

    if arrival_time > next_npc["Time As Minutes"]:
        unvisited_npcs.remove(next_npc)
        continue

    route.append({
        "NPC ID": next_npc["NPC ID"],
        "Location Name": next_npc["Location Name"],
        "Arrival Time": arrival_time,
        "Distance From Previous": next_npc["Distance From Current"]
    })

    current_time = arrival_time
    current_column = next_npc["Location Column"]
    current_row = next_npc["Location Row"]

    unvisited_npcs.remove(next_npc)
    visited_npcs.append(next_npc)

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