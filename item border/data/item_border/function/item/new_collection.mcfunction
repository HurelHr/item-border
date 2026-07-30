$data modify storage item_border:codex itemCodex[$(page)].body[{item:{id:"$(id)"}}].description set value {"text":"[ ✅ ]","color":"green","bold":true}
$data modify storage item_border:database collected append value {id: "$(id)"}

title @a actionbar {"text":"New Item Collected."}
playsound entity.experience_orb.pickup master @a ~ ~ ~ 0.03

function item_border:item/sync