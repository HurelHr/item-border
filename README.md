> DataPack Version: V1.0.3   
> Document Version: V1.0.2   
> Last Modified: 2026-07-31

# item-border

minecraft item border datapack

**State**: Stable / Active
> no critical issues are found

## Notice

> fatal [issue](https://github.com/HurelHr/item-border/issues/1) is fixed. please update 1.0.1 version or later.

# installation

releases: [Here](https://github.com/HurelHr/item-border/releases)

## singleplayer

1. launch MINECRAFT
1. Singleplayer
1. Create New World
1. goto `[More]` tab
1. click `[Data packs]`
1. drag-and-drop `zip` file from [Here](https://github.com/HurelHr/item-border/releases)
1. click `[yes]`
1. enable data pack
1. click `[Done]`
1. click `[Create New World]`
1. enjoy!

## Multiplayer

### Realms

1. create world as like as single play
2. open Realms

### server.jar or bukkit

1. launch server and create world
1. go to `<world>/datapack`
1. drag-and-drop `zip` file from [Here](https://github.com/HurelHr/item-border/releases)
1. type `/reload` or restart your server to apply datapack
  > when data pack load, world border immedietly shrink to 1 block diameter

# Supported Version

> minecraft 1.26.2

items list, datapack are built based on minecraft 1.26.2   
other minecraft version is compatible, after running updater script.

## Supported Minimum Version

> minecraft 1.21.6

since `dialog` feature added, this datapack supports minecraft greater than 1.21.6

# Features

- **Items**: collect different type of item (ignore items that are not collectable in survival mode)
- **Feedback**: notice shows on `actionbar` when new item collect
- **Dialogs**
  > - item collection dialog (press `quick action` button(default `G`) to access this dialog)
  > - dialog action button to change dialog page(s)
  > - dynamic dialog shows item lists collected/not collected
- **World Border**
  > - size syncs to variants of items collected
  > - initial world border size is 1 block distance   
  > - every new item collected, world border increase immediately
- **multiplayer** ready
  - Fully automated player registration system
- **One-Click Updater**
  - This repository contains update python script. (check [detail]())

# Updater script

- run `updater/item_collecter.py` to update items list, datapack description, pack metadata
  > python 3.9 or later required   
  > minecraft 1.21.6 or later compatible