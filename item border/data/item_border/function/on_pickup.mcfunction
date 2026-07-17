advancement revoke @s only item_border:item_obtain

title @s title {text: ""}
title @s subtitle {text:"inventory changed."}
function item_border:snapshot with entity @s

function item_border:get_changes with entity @s
function item_border:snapshot_move with entity @s

function item_border:boarder_decide with entity @s