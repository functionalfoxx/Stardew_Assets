import sqlite3
import math

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

START_HOUR = 8
START_LOCATION_ID = 25              # LOCATION ID 25 = Map connection between player farm and Cindersap Forest
MOVEMENT_SPEED = 23                 # TILES PER TIME_INCREMENTS / Actual speed is about 36 tiles per 10 in game minutes if player runs perfectly without any error in a straight line
TIME_INCREMENTS = 10                # IN GAME MINUTES


cursor.execute("""
    SELECT 
        location_id,
        location_name,
        building,
        open,
        close,
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
        "Building Open Time": row["open"],
        "Building Closed Time": row["close"],
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
    schedule["Building Open Time"] = locations[loc_id]["Building Open Time"]
    schedule["Building Closed Time"] = locations[loc_id]["Building Closed Time"]
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

def process_day(day_input):

    day_values = []

    split_day_input = day_input.split(",")

    for day in split_day_input:
        day_info = day.strip().capitalize()
        day_values.append(day_info)
    
    day_values[1] = int(day_values[1])
    day_number = day_values[1]

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_index = (day_number - 1) % 7
    weekday_name = weekdays[weekday_index]

    date_info = day_values + [weekday_name]

    return date_info

def check_for_event(day_input):

    processed_day = process_day(day_input)

    season = processed_day[0]
    day = processed_day [1]

    cursor.execute("""
        SELECT 
            event_name,
            season,
            day,
            schedule_available
        FROM 
            events
        WHERE
            season = ? 
            AND day = ?
            AND schedule_available = 0
    """, (season, day))

    event_row = cursor.fetchone()

    if event_row:
        print(f"""
            Schedule unavailable. {event_row["event_name"]} is taking place and affects NPC schedules.
        """)
        exit()

def unlocked_npcs (npc_input):

    npc_names = ["Wizard", "Kent", "Dwarf", "Sandy", "Krobus", "Leo"]

    unlocked_npcs = []
    
    split_npc_input = npc_input.split(",")

    for npc in range(len(split_npc_input)):
        answer = split_npc_input[npc].strip().upper()
        
        if answer == "Y":
            unlocked_npcs.append(npc_names[npc])

    cursor.execute("""
        SELECT npc_name
        FROM npcs
        WHERE is_unlocked_by_default == 1
    """)

    rows = cursor.fetchall()

    default_npcs = [row["npc_name"] for row in rows]

    all_unlocked_npcs = default_npcs + unlocked_npcs

    return all_unlocked_npcs


def friendship_hearts(hearts_input):

    hearts_values = []

    split_hearts_input = hearts_input.split(",")

    for hearts in split_hearts_input:
        hearts = hearts.strip()
        hearts_values.append(int(hearts))

    hearts_by_npc = {
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

    return hearts_by_npc

def game_progress(progress_input):

    progress_values = []
    
    split_progress_input = progress_input.split(",")

    for answer in split_progress_input:
        answer = answer.strip().upper()
        if answer == "Y":
            progress_values.append(1)
        elif answer == "N":
            progress_values.append(0)

    user_progress = {
        "Bus Service Restored": progress_values[0],
        "Beach Bridge Repaired": progress_values[1],
        "Community Center Completed": progress_values[2]
    }

    return user_progress






def get_player_progress(npc_input, hearts_input, progress_input, day_info):

    cursor.execute("""
        SELECT 
            npc_schedules.schedule_id,
            npc_schedules.npc_id,
            npc_schedules.priority,
            npc_schedules.hearts_affects,
            npc_schedules.heart_condition,
            npc_schedules.need_community_center,
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

    selected_schedule = {}

    for npc_name in npc_schedules_by_npc:
        schedules = npc_schedules_by_npc[npc_name]

        selected_schedule[npc_name] = []

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

            if_progress_flags = True
            if schedule["need_community_center"] == 1 and progress_input.get("Community Center Completed", 0) == 0:
                if_progress_flags = False
            if schedule["need_bus_service"] == 1 and progress_input.get("Bus Service Restored", 0) == 0:
                if_progress_flags = False
            if schedule["need_beach_bridge"] == 1 and progress_input.get("Beach Bridge Repaired", 0) == 0:
                if_progress_flags = False

            day_matches = True
            if schedule["weekday"] is not None:
                if schedule["weekday"].capitalize() != day_info["Weekday"].strip().capitalize():
                    day_matches = False

            if schedule["season"] is not None:
                if schedule["season"].capitalize() != day_info["Season"].strip().capitalize():
                    day_matches = False

            if schedule["day"] is not None:
                if str(schedule["day"]) != day_info["Date"]:
                    day_matches = False

            weather_ok = False
            day_weather = day_info["Weather"].strip().capitalize()
            schedule_weather = str(schedule["weather"]).strip().capitalize()

            if schedule_weather == day_weather:
                weather_ok = True
            elif schedule_weather == "R" and day_weather == "R" and schedule.get("alternative_rain_possibility", 0) == 1:
                weather_ok = True

            if if_hearts and if_progress_flags and day_matches and weather_ok:
                selected_schedule[npc_name].append(schedule)

    return selected_schedule

def schedule_routing(selected_schedule, start_location_id=START_LOCATION_ID, start_hour=START_HOUR):

    npc_schedules_for_day = []

    for npc_name, schedules in selected_schedule.items():
        if not schedules:
            continue

        schedule = schedules[0]  

        loc_id = schedule["location_id"]

        npc_schedules_for_day.append({
            "NPC Name": npc_name,
            "Location ID": loc_id,
            "Location Name": locations[loc_id]["Location Name"],
            "Location Column": locations[loc_id]["Location Column"],
            "Location Row": locations[loc_id]["Location Row"],
            "Time": schedule["time"],
            "Time As Minutes": time_to_minutes(schedule["time"]),
            "Schedule Description": schedule["schedule_description"]
        })

    if not npc_schedules_for_day:
        return []

    current_col = locations[start_location_id]["Location Column"]
    current_row = locations[start_location_id]["Location Row"]
    current_time = time_to_minutes(f"{start_hour}:00")

    route = []
    unvisited = npc_schedules_for_day.copy()

    while unvisited:

        available = unvisited.copy()

        if not available:
            break

        for npc in available:
            npc["Distance"] = abs(current_col - npc["Location Column"]) + \
                              abs(current_row - npc["Location Row"])

        next_npc = min(available, key=lambda x: x["Distance"])

        distance_tiles = next_npc["Distance"]
        travel_time = math.ceil(distance_tiles / MOVEMENT_SPEED) * TIME_INCREMENTS
        arrival_time = current_time + travel_time

        route.append({
            "NPC Name": next_npc["NPC Name"],
            "Location Name": next_npc["Location Name"],
            "Arrival Time": minutes_to_time(arrival_time),
            "Distance From Previous": distance_tiles,
            "Schedule Description": next_npc["Schedule Description"]
        })

        current_time = arrival_time
        current_col = next_npc["Location Column"]
        current_row = next_npc["Location Row"]

        unvisited.remove(next_npc)

    return route