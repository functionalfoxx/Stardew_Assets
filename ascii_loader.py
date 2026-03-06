import re

NPC_ORDER = [
    "Abigail","Alex","Caroline","Clint","Demetrius","Dwarf","Elliott","Emily",
    "Evelyn","George","Gus","Haley","Harvey","Jas","Jodi","Kent","Krobus",
    "Leah","Leo","Lewis","Linus","Marnie","Maru","Pam","Penny","Pierre",
    "Robin","Sam","Sandy","Sebastian","Shane","Vincent","Willy","Wizard"
]
def load_name_blocks(filename="ascii_names.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()
    blocks = content.split("\n\n")
    name_dict = {}
    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue
        header = lines[0].strip()
        if header.startswith("#"):
            name = header[1:].strip().upper()
            name_dict[name] = lines
    return name_dict

def load_sprite_blocks(filename="ascii_sprites.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()
    blocks = content.split("\n\n")
    sprite_dict = {}
    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue
        header = lines[0].strip()
        if header.startswith("#"):
            name = header[1:].strip().upper()
            sprite_dict[name] = lines[1:]
    return sprite_dict

def get_name_block_by_name(name, name_blocks):
    block = name_blocks.get(name.upper())
    if block:
        return block[1:]
    else:
        return ["<no name>"]

def get_sprite_by_name(name, sprite_blocks):
    return sprite_blocks.get(name.upper(), ["<no sprite>"])