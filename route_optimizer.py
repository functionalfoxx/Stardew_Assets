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
        location_id,
        location_name,
        building,
        map_connection,
        teleport,
        location_column,
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
        schedule_id,
        npc_id,
        location_id,
        time,
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
    day = int(day)

    cursor.execute("""
        SELECT event_name, schedule_available
        FROM events
        WHERE UPPER(season) = ? AND day = ?
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

    cursor.execute("""
        SELECT 
            npc_schedules.schedule_id,
            npc_schedules.npc_id,
            npc_schedules.priority,
            npc_schedules.hearts_affects,
            npc_schedules.heart_condition,
            npc_schedules.need_comunity_center,
            npc_schedules.need_bus_service,
            npc_schedules.need_beach_bridge,
            npc_schedules.weather,
            npc_schedules.alternative_rain_possibility,
            npc_schedules.weekday,
            npc_schedules.season,
            npc_schedules.day,
            npc_schedules.time,
            npc_schedules.location_id,
            npc_schedules.schedule_description,
            npcs.npc_name
        FROM npc_schedules
        LEFT JOIN npcs ON npc_schedules.npc_id = npcs.npc_id
    """)

    schedule_rows = cursor.fetchall()

    npc_schedules_by_npc = {}

    for npc_name in unlocked_npcs:
        npc_schedules_by_npc[npc_name] = []

    for row in schedule_rows:
        npc_name = row["npc_name"]
        if npc_name in npc_schedules_by_npc:
            npc_schedules_by_npc[npc_name].append(row)

    for npc_name in npc_schedules_by_npc:
        schedules = npc_schedules_by_npc[npc_name]

        sorted_schedules = []

        while len(schedules) > 0:

            highest = schedules[0]
            for row in schedules:
                if row["priority"] > highest["priority"]:
                    highest = row

            sorted_schedules.append(highest)
            
            schedules.remove(highest)
        
        npc_schedules_by_npc[npc_name] = sorted_schedules

    for npc_name in npc_schedules_by_npc:
    schedules = npc_schedules_by_npc[npc_name]

        for schedule in schedules:
            if_hearts = True
    
            if schedule["hearts_affects"] == 1 and schedule["heart_condition"]:
                condition = schedule["heart_condition"]

                npc_conditions = []

                if "and" in condition:
                    for cond in condition.split("and"):
                        npc_conditions.append(cond.strip())
                else:
                    npc_conditions = [condition.strip()]

                for npc_cond in npc_conditions:

                    operator = npc_cond[:2]
                    number_and_npc = npc_cond[2:].strip()
                    number_str, target_npc_name = number_and_npc.split(" ", 1)
                    number = int(number_str)
                    target_npc_name = target_npc_name.strip()

                    npc_hearts = hearts_input.get(target_npc_name, 0)

                    if operator == ">=" and npc_hearts < number:
                        if_hearts = False
                        break
                    elif operator == "<=" and npc_hearts > number:
                        if_hearts = False
                        break            
    
    return

    # player progress needs to fully match all the non-null lines per priority. if not 100%, move to next priority (next priority number is a lower # than the one just checked)

        # condition(s) 2: need_comunity_center, need_bus_service, need_beach_bridge all have 0/1 values. match to progress_input
        # condition 3: weather to match letter in day_info {"Date": day_values[2]}
                # if condition = R then check if alternative_rain_possibility is 0/1 in table
                    # if it is a 0, then continue to other conditions
                    # if it is a 1, there is a second schedule possible for the day. there are only 4 times this is a 1
        # condition(s) 5: weekday, season, day to match
        

    

    

"""
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