def item_search_gui(results):
    item_name, item_info = list(results.items())[0]
    frame_width = 50
    top_line = "# " * int(frame_width/2)
    name_line = f"# {item_name.upper().center(frame_width - 4)} #"

    print(top_line)
    print()
    print(name_line)
    print()
    print(top_line)
    print()
    print(f"Visit Wiki: {item_info['Wiki URL']}\n")

    sections = [
        ("NPCs Who Love Item", "LOVED BY"),
        ("NPCs Who Like Item", "LIKED BY"),
        ("NPCs Who Are Neutral Toward Item", "NEUTRAL ITEM"),
        ("NPCs Who Dislike Item", "DISLIKED BY"),
        ("NPCs Who Hate Item", "HATED BY"),
    ]

    cols = 4
    col_width = 13

    for key, header_text in sections:
        padding_total = frame_width - len(header_text) - 4
        padding_left = padding_total // 2
        padding_right = padding_total - padding_left

        header_line = f"* {'-~' * int(padding_left/2)} {header_text} {'~-' * int(padding_right/2)} *"
        print(header_line)

        npc_list = item_info[key]
        if npc_list:
            for i in range(0, len(npc_list), cols):
                row = npc_list[i:i+cols]
                print("".join(name.ljust(col_width) for name in row))
        else:
            print("NONE")
        print()




def item_directory_gui(results, letter):
    cols = 2
    col_width = 25

    frame_width = cols * col_width
    top_line = "# " * (frame_width // 2)

    header_text = f"RESULTS FOR {letter.upper()}"
    name_line = f"# {header_text.center(frame_width - 5)} #"

    print(top_line)
    print()
    print(name_line)
    print()
    print(top_line)
    print()

    if results:
        for i in range(0, len(results), cols):
            row = results[i:i+cols]
            print("".join(name.ljust(col_width) for name in row))
    else:
        print("No results, try again.")