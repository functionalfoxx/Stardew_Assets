import sqlite3
import math

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

START_HOUR = 6
START_LOCATION_ID = 18
MOVEMENT_SPEED = 35                 # 35 TILES PER 10 MINUTES
TIME_INCREMENTS = 10                # IN MINUTES


cursor.execute("""
    SELECT 
        location_id
        location_name
        building
        map_connection
        teleport
        location_column
        location_row
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

    total_minutes = (hour - START_HOUR) * 60 + minute 

    if total_minutes < 0:
        total_minutes += 24 * 60

    return total_minutes

def minutes_to_time(minutes):
    hour = START_HOUR + (minutes // 60)
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"

cursor.execute("""
    SELECT
        schedule_id
        npc_id
        location_id
        time
        schedule_description
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

current_time = time_to_minutes(f"{START_HOUR}:00")                               

route = []

unvisited_npcs = npc_schedules.copy()
visited_npcs = []

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
    travel_time = math.ceil(distance_tiles / MOVEMENT_SPEED) * TIME_INCREMENTS
    arrival_time = current_time + travel_time

    if arrival_time > next_npc["Time As Minutes"]:
        unvisited_npcs.remove(next_npc)
        continue

    route.append({
        "NPC ID": next_npc["NPC ID"],
        "Location Name": next_npc["Location Name"],
        "Arrival Time": minutes_to_time(arrival_time),
        "Distance From Previous": next_npc["Distance From Current"]
    })

    current_time = arrival_time
    current_column = next_npc["Location Column"]
    current_row = next_npc["Location Row"]

    unvisited_npcs.remove(next_npc)
    visited_npcs.append(next_npc)

def check_for_event(season, day):

    cursor.execute("""
    SELECT
        event_name,
        schedule_available
    FROM events
    WHERE season = ? AND day = ?
    """, (season.upper(), day))

    row = cursor.fetchone()

    if row and row["schedule_available"] == 0:
        return row["event_name"]
    
    return None

def get_player_progress(unlocked_input, hearts_input, progress_input, day_input):

    cursor.execute("""
        SELECT npc_names
        FROM npcs
    """)

    rows = cursor.fetchall()

    all_npcs = [row["npc_name"] for row in rows]

    unlocked_npcs = []
    unlocked_npcs = all_npcs.copy()
    
    for npc, status in unlocked_input.items():
        if status.upper() == "N":
            if npc in unlocked_npcs:
                unlocked_npcs.remove(npc)
    
    return

    # match progress to npc_schedules table
    # go through each npc_id one npc at a time and find the highest priority (multiple rows will match that priority for that npc almost every time)
    # player progress needs to fully match all the non-null lines per priority. if not 100%, move to next priority (next priority number is a lower # than the one just checked)
        # condition 1: if table hearts_affects = 1 then heart_condition needs to be looked at
                # if condition = <6 Abigail and Sebastian then hearts input must be <=5 with Abigail AND <=5 with Sebastian
                # if condition = <6 Haley and Alex then hearts input must be <=5 with Haley AND <=5 with Alex
                # if condition = >= 14 Alex then hearts input must be >= 14 with Alex
                # if condition = >= 6 Elliott then hearts input must be >= 6 with Elliott
                # if condition = <6 Leah then hearts input must be <= 5 with Leah
                # if condition = >=6 Alex then hearts input must be >= 6 with Alex
                # if condition = >=6 Leo then hearts input must be >= 6 with Leo
                # if condition = <6 Penny and Sam then hearts input must be <= 5 with Penny AND <= 5 with Sam
                # if condition = <6 Sebastian then hearts input must be <= 5 with Sebastian
                # if condition = >=6 Sebastian then hearts input must be >= 6 with Sebastian
                    # if player matches whatever line is in question, then the hearts_affects line is a match, if not, move on to next priority
        # condition(s) 2: need_comunity_center, need_bus_service, need_beach_bridge all have 0/1 values. match to progress_input
        # condition 3: weather to match letter in day_info {"Date": day_values[2]}
                # if condition = R then check if alternative_rain_possibility is 0/1 in table
                    # if it is a 0, then continue to other conditions
                    # if it is a 1, there is a second schedule possible for the day. there are only 4 times this is a 1
        # condition(s) 5: weekday, season, day to match
        

    

    

"""
        Hearts
        Abigail, Sebastian, Haley, Alex, Elliott, Leah, Leo, Penny, Sam
        Example: 5, 9, 3, 5, 10, 7, 0, 3, 5

        hearts_dict = {
            "Abigail": hearts_values[0],
            "Sebastian": hearts_values[1],
            "Haley": hearts_values[2],
            "Alex": hearts_values[3],
            "Elliott": hearts_values[4],
            "Leah": hearts_values[5],
            "Leo": hearts_values[6],
            "Penny": hearts_values[7],
            "Sam": hearts_values[8]
        }
        
        ======================================================================

        Progress
        Bus Service, Beach Bridge Repair, Community Center
        Example: Y, Y, N

        game_progress = {
            "Bus Service Restored": progress_values[0],
            "Beach Bridge Repaired": progress_values[1],
            "Community Center Completed": progress_values[2]
        }

        =======================================================================

        Day
        Weekday, season, day number, and weather
        For weather, use R for RAIN, G for GREEN RAIN, or N for NO RAIN.
        Example: Wednesday, Summer, 22, N

        day_info = {
            "Weekday": day_values[0],
            "Season": day_values[1],
            "Date": day_values[2],
            "Weather": day_values[3]
        }
        
"""

    
        




"""

RETURNS LIST OF ALL NPCS IN ORDER OF ROUTE OPTIMIZATION STARTING AT 7:00 THROUGH 0:00 IN 24 HOUR FORMAT
EACH LINE SHOWS NPC NAME, LAST TIME LOCATION_DESCRIPTION AND NEXT LOCATION_DESCRIPTION
CHECK IF LANDS ON AN EVENT DAY THAT REMOVES CHARACTER SCHEDULE

"""