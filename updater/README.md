> Datapack Version: V1.0.1   
> Document Version: V1.0.0   
> Last Modified: 2026-07-31

# Manual

## Preparation

- python installed
- minecraft installed

## step-by-step tutorial

1. run python script: `updater/item_collecter.py`
1. folder selector screen will show
    > if select screen title is: `select minecraft version`, this script catch minecraft path.
    > if select screen title is: `select your minecraft folder and its version`, which means script failled to select correct minecraft path. please launch minecraft once or select **your** minecraft path
1. select correct minecraft folder
    > e.g. click folder `26.2` for minecraft `1.26.2` version
    > e.g. click folder `26.3-snapshot-6` for minecraft `1.26.3 snapshot 6` version
1. wait untill updates are done
1. done! now you can apply this datapack to other versions of minecraft!

> Note: this datapack requires `dialog` feature on minecraft. since, select minecraft version greater than `1.21.6`
> Also: if minecraft version changed, whis datapack not automatically update to new version. if you enjoy this datapack on up-to-date minecraft(or changed version), run python script: `updater/item_collecter.py` to update

## Exceptions

- `RuntimeError: user not select directory`: close folder select window without select any folder
- `ValueError: minecraft is not installed or invalid path. please check valid version path or install minecraft before run this script.`: select correct minecraft folder or install minecraft(launch minecraft once to solve this)
- `FileNotFoundError: ...`: select correct minecraft folder
- `KeyError: ...`: select correct minecraft folder. if folder is not wrong, please report it with minecraft version you failled, `key` value not found 