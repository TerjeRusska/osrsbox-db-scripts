from osrsbox import monsters_api, items_api
import json
import os

drop_dict = dict()
drop_hashes = list()

if __name__ == '__main__':
    all_db_monsters = monsters_api.load()
    all_db_items = items_api.load()

    for monster in all_db_monsters:

        if monster.drops and not monster.duplicate:
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
                    drop_dict[drop.id] = item_info
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

    path = 'output'
    os.makedirs(path, exist_ok=False)
    with open("output/drop_table_per_item.json", "w") as outfile:
        json.dump(drop_dict, outfile)
