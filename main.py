from item_query import search_by_item, items_directory
from display import item_search_gui, item_directory_gui, npc_directory_gui, npc_preferences_gui, heart_calc_gui, route_user_gui
from npc_query import search_by_npc, all_npcs, preferences_by_npc, heart_calc
from npc_routing import check_for_event, route_user
import re


print("""
     
      
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       This tool requires your terminal window to be large enough to display all content properly       ╡
        ╡            In the next step, you will resize the window to ensure the box is fully visible             ╞
        ╞                                                                                                        ╡
        ╡                                        Press ENTER to continue                                         ╞
        ╞                                                                                                        ╡
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
      

      """)

input()


print("""
      
    ╔═ UPPER LEFT  ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════  UPPER RIGHT ═╗
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                      CENTER                                                                                      ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ║                                                                                                                                                                                  ║
    ╚═ LOWER LEFT  ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════  LOWER RIGHT ═╝


        Press ENTER to continue
      
      
      
      """)

input()


print("""
      

        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       Hello farmer!                                                                                    ╡
        ╡                                                                                                        ╞
        ╞         Forget that lengthy wiki and get ready to get quick and customized information for your        ╡
        ╡         Stardew needs. Search by NPC, item, or get your daily gift route optimized!                    ╞
        ╞                                                                                                        ╡
        ╡       Type 1: NPC Information                                                                          ╞
        ╞       Type 2: Item Information                                                                         ╡
        ╡       Type 3: Gift Route Optimization                                                                  ╞
        ╞                                                                                                        ╡
        ╡                                                                                                        ╞
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦

      
""")


choice = input("        ✦   Select option: ").strip()

             # # # # # # # # # # # # # # 
            #       NPC QUERY TOOLS      #
             # # # # # # # # # # # # # #


if choice == "1": 
    print("""

                    
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       NPC INFORMATION                                                                                  ╡
        ╡                                                                                                        ╞
        ╞       Type 1: View NPC profile by name                                                                 ╡
        ╡       Type 2: View all giftable NPCs                                                                   ╞
        ╞       Type 3: View all gift preferences by NPC                                                         ╡
        ╡       Type 4: Calculate gifts needed to gain max NPC hearts                                            ╞
        ╞                                                                                                        ╡
        ╡                                                                                                        ╞
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦


    """)

    item_choice = input("        ✦   Select option: ").strip()
    print("\n\n")    

    if item_choice == "1":                                                                              # Still needs GUI-like formatting
        name = input("        ✦   Enter the NPC name you want to search: ").strip()
        print("\n\n") 
        results = search_by_npc(name)
        print(results)

    elif item_choice == "2":
        print("\n\n")
        results = all_npcs()
        npc_directory_gui(results)

    elif item_choice == "3":
        name = input("        ✦   Enter the NPC name you want to search: ").strip()
        print("\n\n")
        results = preferences_by_npc(name)
        npc_preferences_gui(name, results)
    
    elif item_choice == "4":
        
        print("""

                        
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       INFORMATION REGARDING HEART GIFTING                                                              ╡
        ╡                                                                                                        ╞
        ╞                Gifting a 'Stardrop Tea' will progress you by 1 full friendship heart                   ╡
        ╡                A 'Bouquet' needs to be given at 8 hearts to progress further                           ╞
        ╞                A 'Mermaid Pendant' needs to be given at 10 hearts to progress further                  ╡
        ╡                                                                                                        ╞
        ╞                This calculator only includes normal daily gifts, so it does not consider:              ╡
        ╡                - Gifts given at events                                                                 ╞
        ╞                - Gifts given on birthdays                                                              ╡
        ╡                - Quests completed                                                                      ╞
        ╞                - Going to the movie theater                                                            ╡
        ╡                - Talking to the NPC                                                                    ╞
        ╞                - Friendship points boosters                                                            ╡
        ╡                                                                                                        ╞
        ╞                It also doesn't consider whether NPC friendship has declined from:                      ╡
        ╡                - Disliked or hated gifts                                                               ╞
        ╞                - Friendship decay for not talking to NPC                                               ╡
        ╡                - Any other actions that decrease friendship level                                      ╞
        ╞                                                                                                        ╡
        ╡                Calculations are based only on full missing hearts                                      ╞
        ╞                If you have any partial progress towards the next friendship heart, less                ╡
        ╡                items will be needed.                                                                   ╞
        ╞                                                                                                        ╡
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦


        """)

        hearts = input("        ✦   Enter how many full hearts you have with the NPC being searched: ").strip()

        print("\n\n")
        results_friendship = heart_calc(hearts, 10)
        results_marriage = heart_calc(hearts, 14)

        heart_calc_gui(results_friendship, results_marriage)        
       

             # # # # # # # # # # # # # # #
            #       ITEM-QUERY TOOLS      #
             # # # # # # # # # # # # # # #      


elif choice == "2":

    print("""

                    
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       ITEM INFORMATION                                                                                 ╡
        ╡                                                                                                        ╞
        ╞       Type 1: Search by item name                                                                      ╡
        ╡       Type 2: Browse item catalogue by letter                                                          ╞
        ╞                                                                                                        ╡
        ╡                                                                                                        ╞
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦


    """)


    item_choice = input("        ✦   Select option: ").strip()

    if item_choice == "1":
        item = input("        ✦   Enter the item to search: ").strip().lower()
        item = re.sub(r"[^a-z0-9 ]", "", item)
        print("\n\n")
        results = search_by_item(item)

        if results is None:
            print(f"\nCannot find '{item}'. Please try again.\n")

        else:
            item_search_gui(results)

    elif item_choice == "2":
        letter = input("        ✦   Enter a letter to display matching items or enter 'all' to display all giftable items: ").strip()
        print("\n\n")

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

                    
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
        ╡                                                                                                        ╞
        ╞       GIFT ROUTE OPTIMIZATION                                                                          ╡
        ╡                                                                                                        ╞
        ╞         NPC schedules change based on several in-game factors. Answer 4 questions to optimize          ╡
        ╡         your gift route correctly.                                                                     ╞
        ╞                                                                                                        ╡
        ╡         It is assumed you have at least 2 friendship hearts with all NPCs that have bedrooms           ╞
        ╞         so that they are accessible.                                                                   ╡
        ╡                                                                                                        ╞
        ╞         If you are just testing this simulation, you may copy and paste the text in the                ╡
        ╡         provided example for each question.                                                            ╞
        ╞                                                                                                        ╡
        ╡                                                                                                        ╞
        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨ ✦
  
    """)


    day_input = input("""        ✦   QUESTION 1
        ╞              
        ╡     What day is it? Provide the weekday, season, day number, and weather 
        ╞     Your answer must remain in this order
        ╡     For weather, use R for RAIN, G for GREEN RAIN, or N for NO RAIN
        ╞     Your answer must be separated by a comma
        ╡
        ╞     Example: Summer, 22, N
        ╡
        ✦   Enter day info: """)

    print ("""        ╞\n        ╡\n        ╞""")
    
    day_result = check_for_event(day_input)

    npc_input = input("""        ✦   QUESTION 2
        ╡
        ╞     Do you have these characters unlocked? 
        ╡     Wizard, Kent, Mines Dwarf, Sandy, Krobus, Leo
        ╞     Your answer must remain in this order
        ╡     Your answer must be in the form of Y for YES, N for NO, and separated with a comma 
        ╞              
        ╡     Example: Y, Y, Y, N, Y, N
        ╞                  
        ✦   Enter character progress: """)

    print ("""        ╡\n        ╞\n        ╡""")

    hearts_input = input("""        ✦   QUESTION 3
        ╞
        ╡     How many full friendship hearts do you have with each of these characters?
        ╞     Abigail, Sebastian, Haley, Alex, Elliott, Leah, Leo, Penny, Sam
        ╡     Your answer must remain in this order
        ╞     Your answer must be in whole numbers and separated with a comma 
        ╡                 
        ╞     Example: 5, 9, 3, 5, 10, 7, 0, 3, 5
        ╡     
        ✦   Enter friendship hearts: """)

    print ("""        ╞\n        ╡\n        ╞""")

    progress_input = input("""        ✦   QUESTION 4
        ╡
        ╞     Have you completed these game progress points?
        ╡     Bus Service, Beach Bridge Repair, Community Center 
        ╞     Your answer must remain in this order
        ╡     Your answer must be in the form of Y for YES, N for NO, and separated with a comma
        ╞                   
        ╡    Example: Y, Y, N
        ╞
        ✦   Enter game progress: """)

    print ("\n")

    route_user_gui(route_user(day_input, npc_input, hearts_input, progress_input))

else:
    print("Directory not recognized.")