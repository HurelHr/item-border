> Script Version: V1.1.0   
> Document Version: V1.0.0   
> Last Modified: 2026-08-10

# 사용 방법

## 사전 준비

- python 3.9 이상
- minecraft 1.21.6 이상

- 이 `updater` 폴더를 데이터팩이 있는 폴더로 옮겨 주세요.

    다음과 같은 구조여야 합니다:
    ```
    <아무 폴더>/
        ├─item border/
        │   ├─data/
        │   └─pack.mcmeta
        └─updater/
            ├─impossible_items.json
            ├─README.md
            └─updator.py
    ```

## 사용 방법

1. `updater` 폴더내의 `updater.py`를 python IDLE나 python IDE를 이용해 실행합니다.
1. 새 창이 뜹니다.
    > 뜬 창의 제목이 `select minecraft client ".jar" file.`이면:   
    > 이 updater가 설치된 minecraft 경로를 제대로 찾은것입니다.

    > 뜬 창의 제목이 `failed to detect minecraft folder. please select your own minecraft client ".jar" under your own directory path.`이면:   
    > 이 updater가 설치된 minecraft 경로를 찾지 못하였습니다.   
    > 띄워진 창에서 **올바른** minecraft경로를 찾아가주시길 바랍니다.   
    > 이후 `.minecraft/versions`폴더로 이동해 줍니다.
1. 설치된 minecraft 클라이언트 파일을 선택합니다. 기본적으로 `.jar`의 확장자를 가지고 있습니다.

    > 예: minecraft `1.26.2` 버전을 선택 하려면 `26.2` 폴더 내의 `26.2.jar` 파일을 선택하십시오.   
    > 예: minecraft `1.26.3 snapshot 6` 버전을 선택 하려면 `26.3-snapshot-6` 폴더 내의 `26.3-snapshot-6.jar` 파일을 선택하십시오.

    일반적으로 .minecraft는 다음의 구조를 가지고 있습니다.:
    ```
    .minecraft/
        └─versions/
            └─<version>/
                └─<version>.jar     << 이 파일을 선택하고, `열기`버튼을 클릭하십시오.
    ```
1. updater가 datapack의 업데이트를 완료할때까지 기다려 주십시오.
1. `Update Done!  now you can enjoy new datapack` 메시지가 나오면 업데이트가 끝났습니다. 이제 선택한 버전에 맞는 datapack으로 변환 되었습니다.

> Note: 이 datapack은 minecraft의 `dialog` 기능을 사용합니다. 따라서 minecraft `1.21.6` 이후의 버전에서만 datapack이 작동합니다.   
> Also: minecraft버전이 바뀌어도, `updater/updater.py` 업데이트 스크립트를 작동시키지 않는 한 자동으로 datapack이 업데이트 되지 않습니다.   

> Note: 이 업데이트 스크립트는 다음의 datapack파일을 수정합니다.   
> - `function/dialog/init_codex.mcfunction`   
> - `item border/pack.mcmeta`

## 발생 가능한 `Exceptions`

- `RuntimeError: user not select directory`: 폴더를 선택하지 않고 창을 닫았을 때 발생합니다.
- `RuntimeError: user not select file`: 파일을 선택하지 않고 창을 닫았을 때 발생합니다.
- `OSError: not supported os: <...>`: 지원되지 않는 OS[Windows, MAC OS, Linux외]에서 업데이트 스크립트를 동작시켰을 때 발생합니다.
- `ValueError: PACK VERSION is not parsed`: 선택한 `.jar` 파일이 손상되었거나, minecraft 클라이언트가 아닙니다. minecraft를 다시 설치하여 게임 클라이언트의 `version.json`을 복구하세요. 혹은 `CodeUpdater.get_jar_data` 메서드를 실행하여 pack data를 확보한 뒤에 `CodeUpdator.update_pack_meta` 메서드를 실행하세요.