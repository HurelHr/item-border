$execute if data storage item_border:database collected[{id: "$(id)"}] as @s run return fail
$execute as @s run data modify storage item_border:temp itemPage_$(id) set value {id:"$(id)",page:-1}
$execute as @s store result storage item_border:temp itemPage_$(id).page int 1 run data get storage item_border:codex index[{id:"$(id)"}].page
$execute as @s run function item_border:item/new_collection with storage item_border:temp itemPage_$(id)