from osrsbox import monsters_api, items_api
import json
import csv
import os

drop_dict = dict()
drop_hashes = list()

items_table_header = ["id", "name", "is_members", "lowalch", "highalch", "examine"]
items_table_rows = []
monsters_table_header = ["id", "name", "combat_level", "wiki_url"]
monsters_table_rows = []
drops_table_header = ["id", "item_id", "monster_id", "is_members", "quantity", "is_noted", "rarity"]
drops_table_rows = []
drops_table_counter = 0

if __name__ == '__main__':
    all_db_monsters = monsters_api.load()
    all_db_items = items_api.load()

    for monster in all_db_monsters:

        if monster.drops and not monster.duplicate:
            monsters_table_rows.append([monster.id, monster.name, monster.combat_level, monster.wiki_url])
            for drop in monster.drops:
                drop_hash = hash((monster.name, monster.combat_level,
                                  drop.members, drop.quantity, drop.noted, drop.rarity))
                if drop_hash in drop_hashes:
                    continue
                drop_hashes.append(drop_hash)
                if drop.id not in drop_dict:
                    item = all_db_items.lookup_by_item_id(drop.id)
                    item_info = {
                        "name": item.name,
                        "members": item.members,
                        "lowalch": item.lowalch,
                        "highalch": item.highalch,
                        "examine": item.examine,
                        "drops": []
                    }
                    print(item_info)
                    drop_dict[drop.id] = item_info
                    items_table_rows.append(
                        [drop.id, item.name, item.members, item.lowalch, item.highalch, item.examine])
                drop_info = {
                    "id": monster.id,
                    "name": monster.name,
                    "combat_level": monster.combat_level,
                    "wiki_url": monster.wiki_url,
                    "members": drop.members,
                    "quantity": drop.quantity,
                    "noted": drop.noted,
                    "rarity": drop.rarity
                }
                drop_dict[drop.id]["drops"].append(drop_info)
                drops_table_rows.append(
                    [drops_table_counter, drop.id, monster.id, drop.members, drop.quantity, drop.noted, drop.rarity])
                drops_table_counter += 1

    path = 'output'
    os.makedirs(path, exist_ok=True)
    with open("output/drop_table_per_item.json", "w") as outfile:
        json.dump(drop_dict, outfile)

    with open("output/items_table.csv", "w", newline='') as items_table_csv:
        writer = csv.writer(items_table_csv, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(items_table_header)
        writer.writerows(items_table_rows)

    with open("output/monsters_table.csv", "w", newline='') as monsters_table_csv:
        writer = csv.writer(monsters_table_csv, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(monsters_table_header)
        writer.writerows(monsters_table_rows)

    with open("output/drops_table.csv", "w", newline='') as drops_table_csv:
        writer = csv.writer(drops_table_csv, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(drops_table_header)
        writer.writerows(drops_table_rows)
