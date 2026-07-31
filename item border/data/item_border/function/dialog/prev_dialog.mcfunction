execute as @s at @s if score @s cursorPage matches 1.. run scoreboard players operation @s cursorPage -= #item_border:codex_page cursorPage

execute as @s at @s run function item_border:dialog/show_dialog