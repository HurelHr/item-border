$data modify storage item_border:database play_data[{uuid:$(UUID)}].temp.current_item set from storage item_border:database play_data[{uuid:$(UUID)}].snapshot.current_inventory[0]
$data modify storage item_border:database play_data[{uuid:$(UUID)}].temp.current_item.uuid set value $(UUID)

$execute run function item_border:comp_item with storage item_border:database play_data[{uuid:$(UUID)}].temp.current_item

$data remove storage item_border:database play_data[{uuid:$(UUID)}].snapshot.current_inventory[0]

$execute if data storage item_border:database play_data[{uuid:$(UUID)}].snapshot.current_inventory[0] run function item_border:get_changes with entity @s