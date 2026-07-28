execute as @s at @s run scoreboard players operation @s cursorPage += item_border:codex_dialog cursorPage

execute as @s at @s if score @s cursorPage > item_border:codex_dialog maxPage if score @s cursorPage matches 0.. run scoreboard players operation @s cursorPage -= item_border:codex_dialog cursorPage

execute as @s at @s run function item_border:dialog/show_dialog