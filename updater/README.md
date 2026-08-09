> Script Version: V1.1.0   
> Document Version: V1.1.0   
> Last Modified: 2026-08-10

# Manual

## Preparation

- python installed
- minecraft installed

- move this `updater` folder under the directory of datapack exists

    folder tree should be like:
    ```
    <folder>/
        ├─item border/
        │   ├─data/
        │   └─pack.mcmeta
        └─updater/
            ├─impossible_items.json
            ├─README.md
            └─updator.py
    ```

## step-by-step tutorial

1. run python script: `updater/updater.py`
1. file selector window will show
    > if the select window's title is: `select minecraft client ".jar" file.`,   
    > this script catch correct minecraft path.

    > if the select window's title is: `failed to detect minecraft folder. please select your own minecraft client ".jar" under your own directory path.`,   
    > which means script failled to detect correct minecraft path.   
    > please launch minecraft once or move to **your** minecraft path   
    > after that, move to `.minecraft/versions` directory
1. select correct minecraft client .jar

    > e.g. click file `26.2/26.2.jar` for minecraft `1.26.2` version   
    > e.g. click file `26.3-snapshot-6/26.3-snapshot-6.jar` for minecraft `1.26.3 snapshot 6` version

    folder should be like:
    ```
    .minecraft/
        └─versions/
            └─<version>/
                └─<version>.jar     << select this then click `open`
    ```
1. wait untill updates are done
1. done! now you can apply this datapack for selected version of minecraft!

> Note: this datapack requires `dialog` feature on minecraft. since, select minecraft version greater than `1.21.6`   
> Also: if minecraft version changed, this datapack not automatically update to new version.   
> if you use this datapack on up-to-date minecraft(or other version), run python script: `updater/updater.py` to update the datapack code.   

> Note: this datapack updator rewrite following files under the datapack:   
> - `function/dialog/init_codex.mcfunction`   
> - `item border/pack.mcmeta`

## Exceptions

- `RuntimeError: user not select directory`: close folder-select-window without select any folder
- `RuntimeError: user not select file`: close folder-select-window without select any file
- `RuntimeError: selected .jar file is not supported minecraft client or not a minecraft client.`: select correct minecraft client `.jar` file. or, launch minecraft once to install minecraft client
- `OSError: not supported os: <...>`: run this script not on windows, macos or linux
- `ValueError: PACK VERSION is not parsed`: select correct minecraft client `.jar` file. if this exception occured, try re-install minecraft client. `version.json` file under the client may damaged. or, run `CodeUpdater.get_jar_data` method before run `CodeUpdator.update_pack_meta` method