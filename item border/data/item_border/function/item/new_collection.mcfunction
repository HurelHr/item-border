# $execute run worldborder add 1

$execute as @s run data modify storage item_border:codex itemCodex[$(page)].body[{item:{id:"$(id)"}}].description set value {"text":"[ ✅ ]","color":"green","bold":true}
title @a title {"text":"New Item collected."}
$title @a subtitle {"text":"$(id)"}
execute as @a run playsound entity.experience_orb.pickup

$execute run data modify storage item_border:database collected append value {id: "$(id)"}