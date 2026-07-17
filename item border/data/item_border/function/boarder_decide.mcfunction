$data modify storage item_border:database play_data[{uuid:$(UUID)}].temp.new_item.id set from storage item_border:database play_data[{uuid:$(UUID)}].delta_result.id
$data modify storage item_border:database play_data[{uuid:$(UUID)}].temp.new_item.uuid set value $(UUID)

$function item_border:new_collection with storage item_border:database play_data[{uuid:$(UUID)}].temp.new_item