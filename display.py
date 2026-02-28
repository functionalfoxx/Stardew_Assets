def item_search_gui(results):
    item_name, item_info = list(results.items())[0]

    frame_width = 74
    inner_width = frame_width - 4
    left_padding = 8

    print("✦ " + "═" * (frame_width - 4) + " ✦")
    print(f"╞{'':^{inner_width}}╡")
    print(f"╞{'┳┏┳┓┏┓┳┳┓  ┏┓┏┓┏┓┳┓┏┓┓┏':^{inner_width}}╡")
    print(f"╞{'┃ ┃ ┣ ┃┃┃  ┗┓┣ ┣┫┣┫┃ ┣┫':^{inner_width}}╡")
    print(f"╞{'┻ ┻ ┗┛┛ ┗  ┗┛┗┛┛┗┛┗┗┛┛┗':^{inner_width}}╡")
    print(f"╞{'':<{inner_width}}╡")
    print("✧ " + "═" * (frame_width - 4) + " ✧")

    print(f"╞{'':^{inner_width}}╡")
    print(f"╞{item_name.upper():^{inner_width}}╡")
    print(f"╞{'':^{inner_width}}╡")
    print(f"╞{item_info['Wiki URL']:^{inner_width}}╡")
    print(f"╞{'':^{inner_width}}╡")
    print("✧ " + "─" * (frame_width - 4) + " ✧")

    sections = [
        ("NPCs Who Love Item", "LOVED BY", "♥"),
        ("NPCs Who Like Item", "LIKED BY", "★"),
        ("NPCs Who Are Neutral Toward Item", "NEUTRAL ITEM", "✦"),
        ("NPCs Who Dislike Item", "DISLIKED BY", "⊘"),
        ("NPCs Who Hate Item", "HATED BY", "✕"),
    ]

    cols = 4
    col_width = (inner_width - left_padding) // cols

    for index, (key, header_text, symbol) in enumerate(sections):
        header = f"{symbol}  {header_text}  {symbol}"
        print(f"╞{header:^{inner_width}}╡")

        print(f"╞{'':<{inner_width}}╡")

        npc_list = item_info[key]
        if npc_list:
            for i in range(0, len(npc_list), cols):
                row = npc_list[i:i + cols]
                formatted_row = " " * left_padding + "".join(name.ljust(col_width) for name in row)
                print(f"╞{formatted_row:<{inner_width}}╡")
        else:
            formatted_row = " " * left_padding + "None"
            print(f"╞{formatted_row:<{inner_width}}╡")

        print(f"╞{'':<{inner_width}}╡")

        if index < len(sections) - 1:
            print("✧ " + "─" * (frame_width - 4) + " ✧")
        else:
            print("✦ " + "═" * (frame_width - 4) + " ✦")

def item_directory_gui(results, letter):
    cols = 2
    col_width = 35

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
    print()