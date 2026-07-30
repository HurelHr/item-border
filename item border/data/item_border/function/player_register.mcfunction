scoreboard players add @s cursorPage 0
scoreboard players add @s dialogEvent 0
scoreboard players enable @s dialogEvent
execute as @s run tp @s 0.5 ~ 0.5
effect give @s minecraft:resistance 10 5 true
execute as @s run tag @s add registered