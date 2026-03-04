from item_query import search_by_item, items_directory
from display import item_search_gui, item_directory_gui
from npc_query import search_by_npc, all_npcs, preferences_by_npc, heart_calc
from npc_routing import check_for_event, route_user
import re


#print("""
#        
#        This tool requires your terminal window to be large enough to display all content properly.
#        In the next step, you will resize the window to ensure the box is fully visible.
#      
#        Press enter to continue.
#      
#      """)
#
#input()
#
#print("""
#      
#    ╔═ UPPER LEFT  ══════════════════════════════════════════════════════════════════════════════════════════════  UPPER RIGHT ═╗
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                           CENTER                                                          ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ║                                                                                                                           ║
#    ╚═ LOWER LEFT  ══════════════════════════════════════════════════════════════════════════════════════════════  LOWER RIGHT ═╝


#        Press enter to continue""")

# input()


#print("""
#This Stardew tool provides information about NPCs who 
#can receive gifts, items that can be gifted, and how to
#route the two together efficiently.
#""")

print("""
Type 1: NPC Information
Type 2: Item Information
Type 3: Gift Route Optimization\n
""")

choice = input("Select option: ").strip()



             # # # # # # # # # # # # # # 
            #       NPC QUERY TOOLS      #
             # # # # # # # # # # # # # #


if choice == "1": 
    print("""
    NPC Information
          
    Type 1: View NPC profile by name
    Type 2: View all giftable NPCs
    Type 3: View all gift preferences by NPC
    Type 4: Calculate gifts needed to gain max NPC hearts\n
    """)

    item_choice = input("Select option: ").strip()    
    
    if item_choice == "1":                                                                              # Still needs GUI-like formatting
        name = input("Enter the NPC name you want to search: ").strip()                                 # Add a comment to best view profile, expand your terminal window.
        name = re.sub(r"[^A-Za-z]", "", name)
        name = name.capitalize() 
        results = search_by_npc(name)
        print(results)

    elif item_choice == "2":                                                                            # Still needs GUI-like formatting
        print(all_npcs())

    elif item_choice == "3":                                                                            # Still needs GUI-like formatting
        name = input("Enter the NPC name you want to search: ").strip()
        name = re.sub(r"[^A-Za-z]", "", name)
        name = name.capitalize() 
        results = preferences_by_npc(name)
        print(results)
    
    elif item_choice == "4":                                                                            # Still needs GUI-like formatting
        hearts = input("Enter how many full hearts you have with the NPC being searched: ").strip()
        hearts = re.sub(r"[^0-9]", "", hearts)
        hearts = int(hearts)
        results_friendship = heart_calc(hearts, 10)
        results_marriage = heart_calc(hearts, 14)
        print(results_friendship)
        print(results_marriage)

            # notes to add
            # stardrop_tea_qty is going to be same as missing hearts
            # ### mention that a bouquet will need to be given at 8 hearts and is not calculated in item qty needed
            # ### mention that a mermaid pendant will need to be given at 10 hearts and is not calculated in item qty needed
            # to get 14 max hearts -> only show this additional calc if the npc we're under is can_marry
            # calculator includes normal daily gifts only
            # it does not include gifts given for events, quests, movie theater, talking to them, or any other actions that increase friendship level
            # it does not include disliked or hated gifts, friendship decay, or any other actions that decrease friendship level
            # calculations based only on full missing hearts. if player has made any progress between hearts, less items will be needed

       

             # # # # # # # # # # # # # # #
            #       ITEM-QUERY TOOLS      #
             # # # # # # # # # # # # # # #      


elif choice == "2":
    print("""
    Item Information
          
    Type 1: Search by item name
    Type 2: Browse item directory by letter\n
    """)

    item_choice = input("Select option: ").strip()

    if item_choice == "1":
        item = input("Enter the item to search: ").strip().lower()
        item = re.sub(r"[^a-z0-9 ]", "", item)
        results = search_by_item(item)

        if results is None:
            print(f"\nCannot find '{item}'. Please try again.\n")

        else:
            item_search_gui(results)

    elif item_choice == "2":                                                                            # UPDATE TO NEW FORMAT
        letter = input("Enter a letter to display matching items or enter 'all' to display all giftable items: ").strip()

        if letter.lower() == "all":
            results = items_directory(None)
            item_directory_gui(results, "all")

        elif len(letter) == 1 and letter.isalpha():
            results = items_directory(letter)
            item_directory_gui(results, letter)

        else:
            print("\nInvalid input. Enter a single letter A–Z or type ALL.\n")

    else:
        print("Directory not recognized.")



             # # # # # # # # # # # # # # #
            #       ROUTE-OPTIMIZER       #
             # # # # # # # # # # # # # # #   


elif choice == "3":

    print("""
        NPC schedules change based on several factors. Answer 4 questions to optimize your gift route correctly.
        If you are just testing this simulation, you can copy and paste the text in the provided example for each question.
        Please note that it is assumed you have at least 2 hearts with all NPCs that have bedrooms so that they are accessible.
    """)

    day_input = input("""
        QUESTION 1: What day is it? Provide the weekday, season, day number, and weather. Your answer must remain in this order.
        For weather, use R for RAIN, G for GREEN RAIN, or N for NO RAIN.
        Your answer must be separated by a comma
        Example: Summer, 22, N

        Enter day info: """)
    
    day_result = check_for_event(day_input)

    npc_input = input("""
        QUESTION 2: Do you have these characters unlocked? 
        Wizard, Kent, Mines Dwarf, Sandy, Krobus, Leo. Your answer must remain in this order.
        Your answer must be in the form of Y for YES, N for NO, and separated with a comma. 
        Example: Y, Y, Y, N, Y, N
                           
        Enter character progress: """)

    hearts_input = input("""
        QUESTION 3: How many full friendship hearts do you have with each of these characters?
        Abigail, Sebastian, Haley, Alex, Elliott, Leah, Leo, Penny, Sam. Your answer must remain in this order.
        Your answer must be in whole numbers and separated with a comma. 
        Example: 5, 9, 3, 5, 10, 7, 0, 3, 5

        Enter hearts: """)
        
    progress_input = input("""
        QUESTION 4: Have you completed these game progress points?
        Bus Service, Beach Bridge Repair, Community Center. Your answer must remain in this order.
        Your answer must be in the form of Y for YES, N for NO, and separated with a comma.
        Example: Y, Y, N

        Enter progress: """)

    npc_route = route_user(day_input, npc_input, hearts_input, progress_input)

    for stop in npc_route:
        print(f"{stop['Arrival Time']} - {stop['NPC Name']}: {stop['Schedule Description']}")

#    selected_schedule = get_player_progress(unlocked_npcs, hearts_dict, game_progress, day_info)
#    route = schedule_routing(selected_schedule)
#
#    for i, step in enumerate(route, start=1):
#        print(f"#{i} - {step['Arrival Time']}: Go to {step['NPC Name']}. Wiki schedule description: {step['Schedule Description']}")

else:
    print("Directory not recognized.")