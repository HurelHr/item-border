execute as @a[tag=!registered] run function item_border:player_register
execute as @a[scores={dialogEvent=1..}] run function item_border:dialog/dialog_event
execute as @a[scores={dialogEvent=1..}] run scoreboard players set @s dialogEvent 0