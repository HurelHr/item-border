scoreboard objectives add collectItems dummy
scoreboard objectives add maxPage dummy
scoreboard objectives add cursorPage dummy
scoreboard objectives add itemPage dummy

scoreboard players set item_border:codex_dialog cursorPage 1

function item_border:dialog/init_codex

execute store result score item_border:codex_dialog maxPage run data get storage item_border:codex itemCodex
scoreboard players operation item_border:codex_dialog maxPage -= item_border:codex_dialog cursorPage