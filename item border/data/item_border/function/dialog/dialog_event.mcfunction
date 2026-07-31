# open item list
execute as @s[scores={dialogEvent=1}] run function item_border:dialog/show_dialog

# page
execute as @s[scores={dialogEvent=2}] run function item_border:dialog/prev_dialog
execute as @s[scores={dialogEvent=3}] run function item_border:dialog/next_dialog
execute as @s[scores={dialogEvent=4}] run function item_border:dialog/fr_prev_dialog
execute as @s[scores={dialogEvent=5}] run function item_border:dialog/ff_next_dialog

# permission
scoreboard players enable @s dialogEvent