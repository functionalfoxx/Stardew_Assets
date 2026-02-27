from item_query import search_by_item, items_directory
from display import item_search_gui
import re



 # # # # # # # # # # # # # # # # # # 
#        ITEM QUERY FUNCTION        #
 # # # # # # # # # # # # # # # # # # 

print("Enter the item to search")
item = input().lower()
item = re.sub(r"[^a-z0-9 ]", "", item)

results = search_by_item(item)
item_search_gui(results)



 # # # # # # # # # # # # # # # # # # 
#      ITEM DIRECTORY FUNCTION      #
 # # # # # # # # # # # # # # # # # # 


print("Enter a letter to display matching items")
letter = input().upper()
letter = re.sub(r"[^A-Z]", "", letter)
letter = letter[0] if letter else ""
results = items_directory(letter)
if results:
    print(results)
else:
    print("No results, try again.")
