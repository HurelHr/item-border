scoreboard players add @s cursorPage 0
scoreboard players add @s dialogEvent 0
scoreboard players enable @s dialogEvent
execute positioned 0.5 0 0.5 positioned over world_surface run tp 0.5 ~1 0.5
execute as @s run tag @s add registered