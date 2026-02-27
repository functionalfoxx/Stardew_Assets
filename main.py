from item_query import search_by_item, items_directory
from display import item_search_gui, item_directory_gui
import re

print("""
This Stardew tool provides information about NPCs who 
can receive gifts, items that can be gifted, and how to
route the two together efficiently.
""")

print("""
Type 1: NPC Information
Type 2: Item Information
Type 3: Gift Route Optimization\n
""")

choice = input("Select option: ").strip()

if choice == "1":
    print("\nNPC Information page coming soon.")

elif choice == "2":

    print("""
    Item Information
          
    Type 1: Search by item name
    Type 2: Browse item directory by letter\n
    """)

    item_choice = input("Select option: ").strip()

    if item_choice == "1":
        print("Enter the item to search:")
        item = input().lower()
        item = re.sub(r"[^a-z0-9 ]", "", item)

        results = search_by_item(item)
        item_search_gui(results)

    elif item_choice == "2":
        print("Enter a letter to display matching items:")
        letter = input().upper()
        letter = re.sub(r"[^A-Z]", "", letter)
        letter = letter[0] if letter else ""

        results = items_directory(letter)
        item_directory_gui(results, letter)

    else:
        print("Directory not recognized.")

elif choice == "3":
    print("\nGift Route Optimization page coming soon.")

else:
    print("Directory not recognized.")






"""

 ||| ADD DIRECTORY OPTIONS |||

    TYPE B : GO BACK TO THE PREVIOUS SCREEN
    TYPE M : RETURN TO THE MAIN SCREEN

    
||| FIX ERROR FOR SEARCH BY ITEM |||

    STRING THAT SEARCH ISN'T FOUND NOT APPEARING
    ERROR SHOWING IN CONSOLE

    
"""