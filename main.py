from item_query import search_by_item
from display import item_search_gui
import re

# # # # # # # # # # # # # # # # # #
#       ITEM QUERY FUNCTION       #
# # # # # # # # # # # # # # # # # #

print("Enter the item to search")
item = input().lower()
item = re.sub(r"[^a-z0-9 ]", "", item)

results = search_by_item(item)
item_search_gui(results)