execute store result score item_border:border collectItems run data get storage item_border:database collected
scoreboard players operation item_border:border collectItems += item_border:border minimumDistance

execute store result storage item_border:border distance int 1 run scoreboard players get item_border:border collectItems

function item_border:item/border_set with storage item_border:border