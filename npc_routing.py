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

def format_npc_schedules():

    formatted_schedule = []

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
        ORDER BY npc_schedules.schedule_id
    """)

    schedule_rows = cursor.fetchall()

    for row in schedule_rows:
        formatted_schedule.append({
            "Schedule ID": row["schedule_id"],
            "NPC ID": row["npc_id"],
            "NPC Name": row["npc_name"],
            "Priority": row["priority"],
            "Friendship Condition Applies?": row["hearts_affects"],
            "Friendship Condition Terms": row["heart_condition"],
            "Need Community Center?": row["need_community_center"],
            "Need Bus Service?": row["need_bus_service"],
            "Need Beach Bridge?": row["need_beach_bridge"],
            "Weather": row["weather"],
            "Second Schedule Possibility If Rain?": row["alternative_rain_possibility"],
            "Weekday": row["weekday"],
            "Season": row["season"],
            "Day": int(row["day"]),
            "Time": row["time"],
            "Location ID": row["location_id"],
            "Schedule Description": row["schedule_description"]
        })

    return formatted_schedule

def find_best_route(day_input, npc_input, hearts_input, progress_input):

    user_npcs_unlocked = unlocked_npcs(npc_input)               
    user_day_info = process_day(day_input)        
    user_friendship_hearts = friendship_hearts(hearts_input)
    user_progress_points = game_progress(progress_input)
    all_schedules = format_npc_schedules()

    all_schedules.sort(key=lambda schedule: schedule["Priority"], reverse=True)

    best_schedules_by_npc = {}

    for npc_name in user_npcs_unlocked:

        npc_schedules_for_npc = [
            schedule for schedule in all_schedules 
            if schedule["NPC Name"] == npc_name
        ]

        filtered_schedules = []

        for schedule_row in npc_schedules_for_npc:

            if schedule_row["Season"] not in (user_day_info[0], None):
                continue
            if schedule_row["Day"] not in (user_day_info[1], None):
                continue
            if schedule_row["Weather"] not in (user_day_info[2], None):
                continue
            if schedule_row["Weekday"] not in (user_day_info[3], None):
                continue
            
            if schedule_row["Friendship Condition Applies?"] == 1:
                heart_condition_terms = schedule_row["Friendship Condition Terms"]
                conditions = [terms.strip() for terms in heart_condition_terms.split(" and ")]
                failed_condition = False

                for condition in conditions:
                    operator = condition[:2]
                    space_index = condition.index(" ")
                    required_value = int(condition[2:space_index])
                    npc_in_condition = condition[space_index+1:]

                    player_value = user_friendship_hearts.get(npc_in_condition, 0)

                    if operator == "<=" and player_value > required_value:
                        failed_condition = True
                        break
                    elif operator == ">=" and player_value < required_value:
                        failed_condition = True
                        break

                if failed_condition:
                    continue

            if schedule_row["Need Bus Service?"] == 1 and user_progress_points["Bus Service Restored"] == 0:
                continue
            if schedule_row["Need Beach Bridge?"] == 1 and user_progress_points["Beach Bridge Repaired"] == 0:
                continue
            if schedule_row["Need Community Center?"] == 1 and user_progress_points["Community Center Completed"] == 0:
                continue

            filtered_schedules.append(schedule_row)

        if filtered_schedules:
            highest_priority = filtered_schedules[0]["Priority"]
            best_schedules_for_npc = [
                schedule_row for schedule_row in filtered_schedules
                if schedule_row["Priority"] == highest_priority
            ]
            best_schedules_by_npc[npc_name] = best_schedules_for_npc

    return best_schedules_by_npc

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