from pathlib import Path

WORKSPACE: 'Path' = Path(__file__).parent.parent

COMMAND: 'str' = 'execute as @s at @s run function item_border:item/check_collection with entity @s Inventory[{index}]\n'
INVENTORY_MAX: 'int' = 35
fileName: 'str' = 'inventory.mcfunction'
srcLoc: 'Path' = WORKSPACE / 'item border' / 'data' / 'item_border' / 'function' / 'item'

def code_update() -> None:
    with open(srcLoc / fileName, 'w', encoding='utf-8') as mc:
        for i in range(0, INVENTORY_MAX + 1):
            mc.write(COMMAND.format(index=i))


if __name__ == '__main__':
    match input("update code?(Y/n): "):
        case "Y" | 'y':
            code_update()