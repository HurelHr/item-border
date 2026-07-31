execute as @s at @s if score @s cursorPage matches 0..4 run scoreboard players set @s cursorPage 0
execute as @s at @s if score @s cursorPage matches 5.. run scoreboard players operation @s cursorPage -= #item_border:codex_page_5 cursorPage

execute as @s at @s run function item_border:dialog/show_dialog