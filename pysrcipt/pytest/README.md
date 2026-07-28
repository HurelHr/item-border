# file comparison test

## test method

1. build item lists.

    1. prepare server.jar

    in the minecraft launcher, can download server.jar for specific version.

    1. prepare item list from server
    
    run following command in cmd

    > Note: set prompt directory to the 'directory' of server.jar exists.   
    > Note: also up-to-date JDK is required for up-to-date minecraft.

    ### bundler based version

    > version 1.18 -

    ```
    java -DbundlerMainClass=net.minecraft.data.Main -jar server.jar --reports
    ```

    ### classic version

    > version 1.14 - 1.17
    ```
    java -cp server.jar net.minecraft.data.Main --reports
    ```
    
    1. parse `registries.json`
        1. run `item_collector.py`
        2. run `parse_registry`
        > `path` means the directory path of `registries.json`. you can found it in `<server.jar-directory>/generated/reports`
        > `report` means the `Path` instance of reporter saved. it should be `.json` extension.

    1. collect `%appdata%/.minecraft/versions/<version>/resources/items`
        1. run `item_collector.py`
        2. you can use `folderselector` to select `%appdata%/.minecraft/versions/<version>/resources/items`
        > or, you can use `Path` class to transform items directory to `Path`
        3. pass `Path` instance to `collect_items`
        4. catch the return from `collect_items` then passes to `collect_to_json`
        > `path` means directory path to reporter saved.
        > `fileName` means reporter file name(should be `.json` extension)
        > `items` means list of items from returns of `collect_items`
    1. comparison
        1. run `pyscript.pytest.file_comp.py`
        2. use `get_json` to get list of items `.json`
        3. use `compare` to compare two list
        4. you can save result using `store_result`.
        > `name` means file name of reporter.
        > `obj` means compared result from `compare` function.
        >
        > reporter will saved under `Deaktop/result`
    1. count findings
        1. run `pyscript.pytest.file_comp.py`
        2. run `found_comp`
        3. select reporter `.json` under `Desktop/result`, the creation of `store_result` function.
        4. findings will appears using `print`.