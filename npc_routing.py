import sqlite3
import math

DB_PATH = r"C:\Portfolio_Projects\stardew_assets\sqlite\stardew.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

DAY_START = 6
ROUTE_START_HOUR = 8
START_LOCATION_ID = 25              # LOCATION ID 25 = Map connection between player farm and Cindersap Forest
MOVEMENT_SPEED = 23                 # TILES PER TIME_INCREMENTS / Actual speed is about 36 tiles per 10 in game minutes if player runs perfectly without any error in a straight line
TIME_INCREMENTS = 10                # IN GAME MINUTES

def time_to_minutes(HH_mm):
    hour, minute = map(int, HH_mm.split(":"))
    total_minutes = (hour - DAY_START) * 60 + minute
    if total_minutes < 0:
        total_minutes += 24 * 60
    return total_minutes

def minutes_to_time(minutes):
    minutes %= 24 * 60
    hour = (minutes // 60 + DAY_START) % 24
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"

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
            "Day": row["day"],
            "Time": time_to_minutes(row["time"]),
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

def load_locations ():

    cursor.execute("""
        SELECT 
            location_id,
            building,
            open,
            close,
            location_column,
            location_row
        FROM
            locations
    """)

    locations = {}

    for row in cursor.fetchall():
        location_id = row["location_id"]
        locations[location_id] = {
            "Is Building?": row["building"],
            "Building Open Time": row["open"],
            "Building Closed Time": row["close"],
            "Location Column": row["location_column"],
            "Location Row": row["location_row"]
        }

    return locations

def route_user(day_input, npc_input, hearts_input, progress_input):

    all_schedules_today = find_best_route (day_input, npc_input, hearts_input, progress_input)
    locations = load_locations()
    current_col = locations[START_LOCATION_ID]["Location Column"]
    current_row = locations[START_LOCATION_ID]["Location Row"]
    current_time = 0

    visited = []
    unvisited = all_schedules_today.copy()
    route = []

    while unvisited:

        candidates = [] 

        for npc_name, schedules in unvisited.items():

            last_schedule = max([schedule for schedule in schedules if schedule["Time"] <= current_time], 
                            key=lambda x: x["Time"], 
                            default = None)
            if not last_schedule:
                continue
            
            loc = locations[last_schedule["Location ID"]]
            travel_distance = abs(current_col - loc["Location Column"]) + abs(current_row - loc["Location Row"])
            travel_time = math.ceil(travel_distance / MOVEMENT_SPEED) * TIME_INCREMENTS
            arrival_time = current_time + travel_time

            next_schedule = min([schedule["Time"] for schedule in schedules if schedule["Time"] > last_schedule["Time"]], default=24*60)

            if arrival_time < next_schedule:
                candidates.append((npc_name, last_schedule, travel_time, arrival_time, loc))        

        if not candidates:
            current_time += TIME_INCREMENTS
            continue

        chosen = min(candidates, key=lambda x: x[2]) # by travel_time, not sure if arrival_time better
        npc_name, schedule, travel_time, arrival_time, loc = chosen

        arrival_time_adjust = minutes_to_time(arrival_time)
        
        route.append({
                    "Arrival Time": arrival_time_adjust,
                    "NPC Name": npc_name,
                    "Schedule Description": schedule["Schedule Description"]})

        current_col = loc ["Location Column"]
        current_row = loc ["Location Row"]
        current_time = arrival_time

        visited.append(npc_name)
        del unvisited[npc_name]

    return route



# WHILE STILL UNVISITED
# CHECK FOR NPCS IN CLOSEST DISTANCE FOR CURRENT TIME 
# CHECK IF THAT CLOSEST NPC IS IN A BUILDING
    # IF IN BUILDING, CHECK IF BUILDING IS OPEN
        # IF OPEN, 
            # ADD 10 MINUTES TO ARRIVAL TIME, ROUTE TO THAT NPC
        # IF NOT OPEN
            # SKIP THAT NPC THE SAME WAY WE WOULD IF THEY WERENT CLOSE
    # IF NO BUILDING, ROUTE TO THAT NPC
        # REMOVED FROM UNVISITED, ADD TO VISITED, CONVERT ARRIVAL TIME TO HH:MM AND ADD TIME, 
            # NPC NAME, AND MATCHING NPC SCHEDULE DESCRIPTION TO THAT TIME TO ROUTE