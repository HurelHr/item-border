data remove storage item_border:temp currentPage

scoreboard objectives add collectItems dummy
scoreboard objectives add minimumDistance dummy
scoreboard objectives add maxPage dummy
scoreboard objectives add cursorPage dummy
scoreboard objectives add dialogEvent trigger

scoreboard players set item_border:codex_dialog cursorPage 1
scoreboard players set item_border:border minimumDistance 1

worldborder center 0.5 0.5

execute unless data storage item_border:codex itemCodex run function item_border:dialog/init_codex

execute store result score item_border:codex_dialog maxPage run data get storage item_border:codex itemCodex
scoreboard players operation item_border:codex_dialog maxPage -= item_border:codex_dialog cursorPage

function item_border:item/sync

gamerule command_block_output false
gamerule send_command_feedback false