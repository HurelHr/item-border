execute as @s at @s run data modify storage item_border:temp currentPage set value {page: 0}
execute as @s at @s store result storage item_border:temp currentPage.page int 1 run scoreboard players get @s cursorPage

execute as @s at @s run function item_border:dialog/render_dialog with storage item_border:temp currentPage