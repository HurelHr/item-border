execute as @s at @s run scoreboard players operation @s cursorPage += #item_border:codex_page_5 cursorPage

execute as @s at @s if score @s cursorPage > #item_border:codex_page maxPage if score @s cursorPage matches 0.. run execute store result score @s cursorPage run scoreboard players get #item_border:codex_page maxPage

execute as @s at @s run function item_border:dialog/show_dialog