import textwrap

def item_search_gui(results):
    item_name, item_info = list(results.items())[0]

    frame_width = 74
    inner_width = frame_width - 2
    left_padding = 8
    cols = 4
    col_width = (inner_width - left_padding) // cols

    def alternating_line(left_border, content=""):
        right_border = "╞" if left_border == "╡" else "╡"
        print(f"        {left_border}{content}{right_border}")
        return right_border

    print("        ✦ " + "╨╥" * int((frame_width / 2) - 2) + " ✦")

    left = "╡"
    left = alternating_line(left, f"{'':^{inner_width}}")
    left = alternating_line(left, f"{'┳┏┳┓┏┓┳┳┓  ┏┓┏┓┏┓┳┓┏┓┓┏':^{inner_width}}")
    left = alternating_line(left, f"{'┃ ┃ ┣ ┃┃┃  ┗┓┣ ┣┫┣┫┃ ┣┫':^{inner_width}}")
    left = alternating_line(left, f"{'┻ ┻ ┗┛┛ ┗  ┗┛┗┛┛┗┛┗┗┛┛┗':^{inner_width}}")
    left = alternating_line(left, f"{'':<{inner_width}}")
    print("        ✧ " + "─" * (frame_width - 3) + "✧")

    left = "╡"
    left = alternating_line(left, f"{'':^{inner_width}}")
    left = alternating_line(left, f"{item_name.upper():^{inner_width}}")
    left = alternating_line(left, f"{'':^{inner_width}}")
    left = alternating_line(left, f"{item_info['Wiki URL']:^{inner_width}}")
    left = alternating_line(left, f"{'':^{inner_width}}")
    print("        ✧ " + "─" * (frame_width - 3) + "✧")

    sections = [
        ("NPCs Who Love Item", "LOVED BY", "♥"),
        ("NPCs Who Like Item", "LIKED BY", "★"),
        ("NPCs Who Are Neutral Toward Item", "NEUTRAL ITEM", "✦"),
        ("NPCs Who Dislike Item", "DISLIKED BY", "⊘"),
        ("NPCs Who Hate Item", "HATED BY", "✕"),
    ]

    for index, (key, header_text, symbol) in enumerate(sections):
        left = "╡"
        header = f"{symbol}  {header_text}  {symbol}"
        left = alternating_line(left, f"{header:^{inner_width}}")
        left = alternating_line(left, f"{'':<{inner_width}}")

        npc_list = item_info[key]
        if npc_list:
            for i in range(0, len(npc_list), cols):
                row = npc_list[i:i + cols]
                formatted_row = " " * left_padding + "".join(name.ljust(col_width) for name in row)
                left = alternating_line(left, f"{formatted_row:<{inner_width}}")
        else:
            formatted_row = " " * left_padding + "None"
            left = alternating_line(left, f"{formatted_row:<{inner_width}}")

        left = alternating_line(left, f"{'':<{inner_width}}")

        if index < len(sections) - 1:
            print("        ✧ " + "─" * (frame_width - 3) + "✧")
        else:
            print("        ✦ " + "╨╥" * int((frame_width / 2) - 2) + " ✦")

    print("\n\n")

def item_directory_gui(results, letter):
    cols = 3
    col_width = 35
    indent = "        "
    left_pad = 4

    frame_width = cols * col_width
    top_line = "╨╥" * (frame_width // 2)
    header_text = f"RESULTS FOR {letter.upper()}"

    def alternating_line(left_border, content=""):
        right_border = "╞" if left_border == "╡" else "╡"
        print(f"{indent}{left_border}{content}{right_border}")
        return right_border

    print(f"{indent}✦ {top_line} ✦")

    left = "╡"
    left = alternating_line(left, header_text.center(frame_width))
    left = alternating_line(left, "─" * frame_width)
    left = alternating_line(left, " " * frame_width)

    if results:
        for i in range(0, len(results), cols):
            row = results[i:i + cols]
            row_text = " " * left_pad

            total_cols = len(row)
            widths = [col_width] * total_cols
            widths[0] -= left_pad

            for w, name in zip(widths, row):
                row_text += name.ljust(w)

            missing_cols = cols - len(row)
            row_text += " " * (missing_cols * col_width)

            left = alternating_line(left, row_text)

        left = alternating_line(left, " " * frame_width)
    else:
        left = alternating_line(left, " " * left_pad + "No results, try again.".center(frame_width - left_pad))
        left = alternating_line(left, " " * frame_width)

    print(f"{indent}✦ {top_line} ✦\n\n")
def npc_directory_gui(results):
    cols = 2
    col_width = 18
    indent = "        "

    frame_width = cols * col_width
    top_line = "╨╥" * (frame_width // 2)
    header_text = "ALL GIFTABLE NPCS"

    def alternating_line(left_border, content=""):
        right_border = "╞" if left_border == "╡" else "╡"
        print(f"{indent}{left_border}{content}{right_border}")
        return right_border

    print(f"{indent}✦ {top_line} ✦")

    left = "╡"
    left = alternating_line(left, header_text.center(frame_width))

    left = alternating_line(left, "─" * frame_width)

    left = alternating_line(left, " " * frame_width)

    if results:
        for i in range(0, len(results), cols):
            row = results[i:i + cols]
            row_text = "".join(name.center(col_width) for name in row)
            left = alternating_line(left, row_text)

        left = alternating_line(left, " " * frame_width)
    else:
        left = alternating_line(left, "No results.".center(frame_width))
        left = alternating_line(left, " " * frame_width)

    print(f"{indent}✦ {top_line} ✦\n\n")

def npc_preferences_gui(npc_name, preference_info):
    frame_width = 120
    inner_width = frame_width - 4
    left_padding = 2

    def line(left, content=""):
        right = "╞" if left == "╡" else "╡"
        print(f"        {left} {content:<{inner_width}} {right}")

    print("        ✦ " + "╨╥" * int((frame_width / 2) - 2) + " ✦")
    line("╡")
    line("╞", "NPC GIFT PREFERENCES".center(inner_width))
    line("╡")
    print("        ✧ " + "─" * (frame_width - 3) + "✧")

    line("╞")
    line("╡", npc_name.upper().center(inner_width))
    line("╞")
    print("        ✧ " + "─" * (frame_width - 3) + "✧")

    sections = [
        ("Loved", "LOVED ITEMS", "♥"),
        ("Liked", "LIKED ITEMS", "★"),
        ("Neutral", "NEUTRAL ITEMS", "✦"),
        ("Disliked", "DISLIKED ITEMS", "⊘"),
        ("Hated", "HATED ITEMS", "✕"),
    ]

    cols = 4
    col_width = (inner_width - left_padding) // cols

    for index, (key, header_text, symbol) in enumerate(sections):
        header = f"{symbol}  {header_text}  {symbol}"
        line("╡", header.center(inner_width))
        line("╞")

        item_list = preference_info[key]

        if item_list:
            for i in range(0, len(item_list), cols):
                row = item_list[i:i + cols]
                formatted_row = " " * left_padding + "".join(item.ljust(col_width) for item in row)
                line("╡", formatted_row)
        else:
            formatted_row = " " * left_padding + "None"
            line("╡", formatted_row)

        line("╞")

        if index < len(sections) - 1:
            print("        ✧ " + "─" * (frame_width - 3) + "✧")
        else:
            print("        ✦ " + "╨╥" * int((frame_width / 2) - 2) + " ✦")

    print("\n\n")

def heart_calc_gui(friendship, marriage):
    total_width = 100

    def line(left, content=""):
        right = "╞" if left == "╡" else "╡"
        padding = total_width - len(content)
        if padding < 0:
            padding = 0
        print(f"        {left} {content}{' ' * padding} {right}")

    print("        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥ ✦")

    line("╡")
    line("╞", "     .o    .oooo.         _   _")
    line("╡", f"   o888   d8P'`Y8b     ,d88b.d88b,      {friendship['points_needed']} Friendship Points Needed")
    line("╞", f"    888  888    888    88888888888      {friendship['loved_qty']} more loved items ({friendship['loved_weeks']} weeks of consistent gifting)")
    line("╡", f"    888  888    888    `Y8888888Y'      {friendship['liked_qty']} more liked items ({friendship['liked_weeks']} weeks of consistent gifting)")
    line("╞", f"    888  888    888      `Y888Y'        {friendship['neutral_qty']} more neutral items ({friendship['neutral_weeks']} weeks of consistent gifting)")
    line("╡", "    888  `88b  d88'        `Y'")
    line("╞", "   o888o  `Y8bd8P'")
    line("╡")
    line("╞")

    line("╡", "      .o        .o        _   _")
    line("╞", f"    o888      .d88     ,d88b.d88b,      {marriage['points_needed']} Friendship Points Needed")
    line("╡", f"     888    .d'888     88888888888      {marriage['loved_qty']} more loved items ({marriage['loved_weeks']} weeks of consistent gifting)")
    line("╞", f"     888  .d'  888     `Y8888888Y'      {marriage['liked_qty']} more liked items ({marriage['liked_weeks']} weeks of consistent gifting)")
    line("╡", f"     888  88ooo888oo     `Y888Y'        {marriage['neutral_qty']} more neutral items ({marriage['neutral_weeks']} weeks of consistent gifting)")
    line("╞", "     888       888         `Y'")
    line("╡", "    o888o     o888o")
    line("╞")

    print("        ✦ ╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥╨╥ ✦")
    print("\n\n")


def route_user_gui(npc_route):
    frame_width = 125
    inner_width = frame_width - 6
    left_padding = 3

    print("        ✦ " + "╨╥" * int((frame_width / 2) - 4) + " ✦")

    print(f"        ╞{' ' * left_padding:<{inner_width}}╡")

    for idx, stop in enumerate(npc_route):
        line = f"{stop['Arrival Time']} - {stop['NPC Name']}: {stop['Schedule Description']}"
        padded_line = f"{' ' * left_padding}{line}"
        if idx % 2 == 0:
            print(f"        ╞{padded_line:<{inner_width}}╡")
        else:
            print(f"        ╡{padded_line:<{inner_width}}╞")

    print(f"        ╞{' ' * left_padding:<{inner_width}}╡")

    print("        ✦ " + "╨╥" * int((frame_width / 2) - 4) + " ✦")
    print("\n\n")

SPRITE_WIDTH = 60      
NAME_HEIGHT = 9        
PADDING = 4            

def print_npc_profile(profile, npc_sprite, ascii_name_lines, max_width=120):
    """
    profile: dict from search_by_npc
    npc_sprite: list of strings (sprite lines)
    ascii_name_lines: list of strings (ASCII name)
    max_width: optional total width of profile box
    """

    def top_bottom_border():
        repeat = "╨╥" * ((max_width - 4)//2)
        return f"✦ {repeat} ✦"

    def side_line(content=""):
        content_len = len(content)
        padding = max_width - 2 - content_len
        return f"╞{content}{' ' * padding}╡"

    def format_name_section(name_lines):
        section = []
        for i in range(NAME_HEIGHT):
            line = name_lines[i] if i < len(name_lines) else ""
            section.append(line)
        return section

    def divider_line():
        content = "_" * (max_width - 4)
        return f"╡  {content}  ╡"

    def format_loved_trivia(loved_items, trivia_lines):
        lines = []
        left_width = (max_width - SPRITE_WIDTH - PADDING) // 2 - 1
        right_width = max_width - SPRITE_WIDTH - PADDING - left_width - 1
        max_rows = max((len(loved_items) + 1)//2, len(trivia_lines))
    
        wrapped_trivia = []
        for line in trivia_lines:
            wrapped_trivia.extend(textwrap.wrap(line, width=right_width))
        for i in range(max_rows):
            li1 = loved_items[i*2] if i*2 < len(loved_items) else ""
            li2 = loved_items[i*2+1] if i*2+1 < len(loved_items) else ""
            left_content = f"{li1:<15}{li2:<15}"
            tri_line = wrapped_trivia[i] if i < len(wrapped_trivia) else ""
            tri_line = f"{tri_line:<{right_width}}"
            lines.append(f"╞  {left_content}│{tri_line}╡")
        return lines

    print(top_bottom_border())

    name_section = format_name_section(ascii_name_lines)
    sprite_height = len(npc_sprite)
    right_section_height = sprite_height
    for i in range(right_section_height):
        sprite_line = npc_sprite[i] if i < len(npc_sprite) else " " * SPRITE_WIDTH
        name_line = name_section[i] if i < len(name_section) else ""
        right_padding = max_width - SPRITE_WIDTH - PADDING - len(name_line) - 2
        print(f"╡  {sprite_line}{' ' * PADDING}{name_line}{' ' * right_padding}╡")

    print(divider_line())

    marry_symbol = "♥" if profile['can_marry'] else "⊘"
    marry_line = f"{'Can Marry' if profile['can_marry'] else 'Cannot Marry'} {marry_symbol}"
    marry_line += f" | Birthday: {profile['birthday_season']} {profile['birthday_day']}"
    print(side_line(marry_line))

    print(divider_line())

    loved_items = profile.get('loved_items', [])
    trivia_lines = [profile.get('trivia_fact', '')]
    lt_lines = format_loved_trivia(loved_items, trivia_lines)
    for line in lt_lines:
        print(line)

    print(top_bottom_border())