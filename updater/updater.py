__version__ = "1.1.0"
__doc__ = """
this is update script for item border datapack.
call CodeUpdater.code_update() to update
"""

from typing import (
    Iterable,
    Union,
    Optional,
    TYPE_CHECKING
)
from pathlib import Path
from zipfile import ZipFile
import json
from fnmatch import fnmatch
import sys

if TYPE_CHECKING:
    from zipfile import ZipInfo
    from typing import TypeAlias
    
    AvailableFileTypeOptions: 'TypeAlias' = Optional[Iterable[tuple[str, str | list[str] | tuple[str, ...]]]]

UPDATOR_HOME: 'Path' = Path(__file__).parent
"""directory that contains this file"""
PACK_HOME: 'Path' = UPDATOR_HOME.parent
"""directory of datapack"""

ITEMS_PER_PAGE: 'int' = 50
"""the number of items in single dialog page"""

def folder_selector(path: 'Union[Path, str, None]'=None, title: 'Optional[str]'=None) -> 'Path':
    """
    to use tkinter
    shows window to select directory
    
    Args:
        path (Path|str|None): directory path to show initially. Defaults to None
        title (str|None): window title
        
    Raises:
        RuntimeError: this raises when user not select directory on tkinter window.
        
    Returns:
        Path: pathlib.Path instance contains selected directory path
    """
    
    # use tkinter
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
    # create window
    tk = Tk()
    tk.withdraw()
    tk.attributes('-topmost', True)
    # get user input
    dir = askdirectory(
        initialdir=path,
        title=title
    )
    # kill tk
    tk.destroy()
    
    # if user reply
    if dir:
        return Path(dir)
    # user close the window without response
    raise RuntimeError('user not select directory')

def file_selector(
    path: 'Union[Path, str, None]'=None,
    title: 'Optional[str]'=None,
    extensions: 'AvailableFileTypeOptions'=None
) -> 'Path':
    """
    to use tkinter
    shows window to select directory
    
    Args:
        path (Path|str|None): directory path to show initially. Defaults to None
        title (str|None): window title
        extensions (Iterable[tuple[str, str | list[str] | tuple[str, ...]]]|None): iterable of str, list or tuple with extension string to filter the file list when shows on file asking window
        
    Raises:
        RuntimeError: this raises when user not select directory on tkinter window.
        
    Returns:
        Path: pathlib.Path instance contains selected directory path
    """
    
    # use tkinter
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    # create window
    tk = Tk()
    tk.withdraw()
    tk.attributes('-topmost', True)
    # get user input
    file = askopenfilename(
        initialdir=path,
        title=title,
        filetypes=extensions
    )
    # kill tk
    tk.destroy()
    
    # if user reply
    if file:
        return Path(file)
    # user close the window without response
    raise RuntimeError('user not select file')
    

def collect_items(path: 'Path') -> 'list[Path]':
    """
    collect all file and return the files list
    
    Args:
        path (Path): directory path to collect files
        
    Returns:
        list[Path]: list of Path instances that contains files under given `path` directory
    """
    
    # result list
    result: 'list[Path]' = []

    # file/folder under given path
    for content in path.iterdir():
        # collect if file
        if content.is_file(): result.append(content)
    return result

# for test only
def collect_to_json(path: 'Path', fileName: 'str', items: 'list[Path]') -> None:
    """
    create `json` file under given directory Path with given `items`
    get a file name from `items` then store it into json file with 'minecraft:' suffix (without extension)
    result json file contains single list array with item codes

    Args:
        path (Path): directory Path json file stored
        fileName (str): file name of json it should be ends with '.json'
        items (list[Path]): list of Path instances that contains file directory to store to json file
    """
    
    # create final directory if not exist
    path.mkdir(parents=True, exist_ok=True)
    # make result json
    path = path / fileName
    # get a filename without extension then attatch prefix 'minecraft:'
    itemNames: 'list[str]' = [f'minecraft:{item.name.replace(item.suffix, "")}' for item in items]
    # dump to json
    with path.open('w', encoding='utf-8') as js:
        json.dump(itemNames, js, ensure_ascii=False, indent=4)

# for test only
def collect_to_csv(path: 'Path', items: 'list[str]') -> None:
    """
    create `items.csv` file under given path with given `items`
    get a item id from `items` then store it into `items.csv` file

    Args:
        path (Path): directory Path csv file stored
        items (list[str]): list of item ids to store to csv file
    """
    
    # create final directory if not exist
    path.mkdir(parents=True, exist_ok=True)
    # make result csv
    path = path / f'items.csv'
    # write to csv
    with path.open('w', encoding='utf-8') as cv:
        cv.write('\n'.join(items))

# deprecated
def parse_registries(path: 'Path', report: 'Path') -> None:
    """
    parse `registries.json` from decomposed `server.jar`
    then re-collect to single json with item ids
    
    Args:
        path (Path): directory Path of `registries.json` file
        report (Path): directory Path of result json file
    """
    
    # find registries.json
    path = path / 'registries.json'
    # open and load it
    with path.open(encoding='utf-8') as js:
        reg: 'dict' = json.load(js)
    # get item ids under registries.json
    items: 'list' = list(reg['minecraft:item']['entries'].keys())
    # create result directory if not exist
    report.parent.mkdir(parents=True, exist_ok=True)
    # dump it
    with report.open('w',encoding='utf-8') as js:
        json.dump(items, js, ensure_ascii=False,indent=4)
        
def default_minecraft_path() -> 'Path':
    """
    get the directory that minecraft installed
    supported OS: `Windows`, `MAC OS`, `Linux`
    this not guarantee the directory exists
    
    Returns:
        Path: directory Path of minecraft
    """
    # depends on each platform
    match sys.platform:
        # windows
        case 'win32':
            return Path.home() / 'AppData' / 'Roaming' / '.minecraft'
        # mac os
        case 'darwin':
            return Path.home() / 'Library' / 'Application Support' / '.minecraft'
        # linux
        case 'linux':
            return Path.home() / '.minecraft'
    # not supported os
    raise OSError(f'not supported os: {sys.platform}')

class CodeUpdater:
    """datapack code updator"""
    GAME_VERSION: 'str' = ''
    """minecraft game version from selected version of minecraft client"""
    PACK_VERSION: 'dict' = {}
    """datapack versions from selected version of minecraft client"""
    itemList: 'list[str]' = []
    """existing all list of items from selected version of minecraft client"""

    @staticmethod
    def select_version() -> 'Path':
        """
        to use tkinter to select specific version of minecraft client to parse.   
        tkinter askfolder window will show
        
        Returns:
            Path: directory Path of minecraft client data `<version>.jar` file
        """
        # get default game client path
        gamePath: 'Path' = default_minecraft_path()
        # check client exist
        if gamePath.exists():
            # ask version directory
            return file_selector(path=default_minecraft_path() / 'versions', title='select minecraft client ".jar" file.', extensions=[('minecraft client file', '*.jar')])
        else:
            # ask to find minecraft and its version
            return file_selector(title='failed to detect minecraft folder. please select your own minecraft client ".jar" under your own directory path.', extensions=[('minecraft client file', '*.jar')])

    @staticmethod
    def check_version_jar(path: 'Path') -> 'bool':
        """
        check given `<version>.jar` is valid game client or not
        
        Args:
            path (Path): directory Path of `<version>.jar`
        
        Returns:
            bool: validation of `<version>.jar`
        """
        # extesion check
        if path.suffix != '.jar':
            return False
        # file list check
        with ZipFile(path) as jarFile:
            contains: 'list[str]' = jarFile.namelist()
            if 'version.json' not in contains:
                return False
            elif not any(f.startswith('assets/minecraft/items') for f in contains):
                return False
            return True

    @classmethod
    def get_items_list(cls, jarFile: 'ZipFile') -> None:
        """
        parse `<version>.jar` then get list of items under given game client
        
        Args:
            jarFile (ZipFile): `<version>.jar` to parse
        """
        # set items path under jar file
        itemsFolder: 'Path' = Path('assets/minecraft/items')
        # get files list under items path
        items: 'list[ZipInfo]' = [fi for fi in jarFile.filelist if not fi.is_dir() and Path(fi.filename).is_relative_to(itemsFolder)]

        # set a function to get file basename
        def basename(f: 'Path') -> 'str':
            """
            remove suffix from given Path
            
            Args:
                f (Path): Path to remove suffix
                
            Returns:
                str: file name without suffix
            """
            # replace suffix to empty string: ''
            return f.name.replace(f.suffix, '')
        # convert all ZipInfo to string
        # get file name, convert to file name without suffix
        # attatch 'minecraft:' suffix
        cls.itemList = [f'minecraft:{basename(Path(f.filename))}' for f in items]

    @classmethod
    def get_version_data(cls, jarFile: 'ZipFile') -> None:
        """
        parse `version.json` under jar file
        set GAMEVERSION: client version
        set PACK_VERSION: datapack version
        
        Args:
            jarFile (ZipFile): `<version>.jar` to parse
        """
        # get version.json
        version: 'dict' = json.load(jarFile.open('version.json'))
        # get game version
        cls.GAME_VERSION = version.get("name", "unknown version")
        # get datapack version
        cls.PACK_VERSION = version.get("pack_version", {})
        
    @classmethod
    def get_jar_data(cls, path: 'Path') -> None:
        """
        auto-parser with client version and items list
        
        Args:
            path (Path): `<version>.jar` path
        """
        # open jar file
        with ZipFile(path, 'r') as jar:
            # set client version
            cls.get_version_data(jar)
            # set items list
            cls.get_items_list(jar)

    @staticmethod
    def item_filter(items: 'list[str]') -> 'list[str]':
        """
        filter function to remove unoptainable items from list
        this method relied to `impossible_items.json`
        this uses `fnmatch` module to screen

        prepared `impossible_items.json` with special character: (`*`, `?`) can screen multiple items
        
        Args:
            items (list[str]): list of item id to filter
        """
        
        # open `impossible_items.json` and load
        with (UPDATOR_HOME / 'impossible_items.json').open(encoding='utf-8') as js:
            invalidItems: 'list[str]' = json.load(js)
        # internal filter function
        def screen(itemCode: 'str') -> 'bool':
            """
            filter function
            check one of term under impossible_items.json matchs to given item code

            Args:
                itemCode (str): item code string to match
            
            Returns:
                bool: True if given item code not matches to `impossible_items.json`
            """
            # inspect all terms under `impossible_items.json`
            return not any(fnmatch(itemCode, inv) for inv in invalidItems)
        # return screened list
        return [item for item in items if screen(item)]

    @staticmethod
    def get_dialog_body(items: 'list[str]') -> 'str':
        """
        create `dialig.body` element
        
        Args:
            items (list[str]): list of item ids to make `dialog.body`
            
        Returns:
            str: single string of `dialog.body`
        """
        # set body structure
        ITEM_COMMAND: 'str' = '{{type:"minecraft:item",item:{{id:"{code}"}},description:{{contents:{{"text":"[ ❌ ]","color":"red","bold":true}},width:50}},show_decoration:false}}'
        # create body element then return
        return ','.join(ITEM_COMMAND.format(code=itemName) for itemName in items)

    @classmethod
    def write_init_code(cls, itemCods: 'list[str]') -> None:
        """
        write `init_codex.mcfunction` with given items list
        
        Args:
            itemCodes (list[str]): list of item ids
        """
        # set page indicator string command
        CODEX_COMMAND: 'str' = 'data modify storage item_border:codex itemCodex append value {{body:[{{type:"minecraft:plain_message",contents:"Page: {index}"}},{body}]}}\n'
        # set inverted item index command
        INDEX_COMMAND: 'str' = 'data modify storage item_border:codex index append value {{id:"{item}", page:{index}}}\n'
        # result dictionary for divided items into page
        pageItem: 'dict[int, list[str]]' = {}
        # divide items with given amount: `ITEMS_PER_PAGE`
        for num, item in enumerate(itemCods):
            pageNums: 'int' = num // ITEMS_PER_PAGE
            if pageNums in pageItem:
                pageItem[pageNums].append(item)
            else:
                pageItem[pageNums] = [item]
        # get a maximum number of page
        endPage: 'int' = max(pageItem.keys())
        # write `init_codex.mcfunction`
        with open(UPDATOR_HOME.parent / 'item border' / 'data' / 'item_border' / 'function' / 'dialog' / 'init_codex.mcfunction', 'w', encoding='utf-8') as mcfunc:
            # set client version
            mcfunc.write(f'# Game Version: {cls.GAME_VERSION}\n')
            # storage initialize
            mcfunc.write('data modify storage item_border:codex itemCodex set value []\n')
            mcfunc.write('data modify storage item_border:codex index set value []\n')
            # set `dialog`
            for page, items in pageItem.items():
                mcfunc.write(CODEX_COMMAND.format(body=cls.get_dialog_body(items), index=f'{page} / {endPage}'))
            # set inverted index storage
            for page, items in pageItem.items():
                for item in items:
                    mcfunc.write(INDEX_COMMAND.format(item=item, index=page))
                    
    @classmethod
    def update_pack_meta(cls) -> None:
        """
        write `pack.mcmeta` with datapack version from game client
        
        Note:
            this method supports minecraft 1.21.9 or later (for snapshot: 25w31a or later)
            datapack itself can run without any error, but since pack.mcmeta is not supported, datapack may shows with curropted aleart
        """
        # set `pack.mcmeta` path
        packMcMeta: 'Path' = PACK_HOME / 'item border' / 'pack.mcmeta'
        # set `pack.mcmeta` description template
        PACK_DESCRIPTION: 'str' = "item border datapack item list for {version}"
        # create `pack.mcmeta`
        with open(packMcMeta, 'w', encoding='utf-8') as js:
            # version for 1.21.9, 25w31a or later
            if 'data_major' in cls.PACK_VERSION:
                # get pack version
                packVersion = [cls.PACK_VERSION.get('data_major', 0), cls.PACK_VERSION.get('data_minor', 0)]
                # create content of `pack.mcmeta`
                packData = {
                    "pack": {
                        "description": PACK_DESCRIPTION.format(version=cls.GAME_VERSION),
                        "min_format": packVersion,
                        "max_format": packVersion
                    }
                }
            # version for 1.21.8 or older
            elif 'data' in cls.PACK_VERSION:
                packData = {
                    "pack": {
                        "description": PACK_DESCRIPTION.format(version=cls.GAME_VERSION),
                        "pack_format": cls.PACK_VERSION.get('data', 0)
                    }
                }
            else:
                raise ValueError('PACK VERSION is not parsed.')
            # dump it
            json.dump(packData, js, indent=4)

    @classmethod
    def update_code(cls) -> None:
        """
        update datapack with selected game client version
        
        Preparation:
            before run this method, you should check following instructions
            
            1. move `updator`folder under the directory that datapack exists
                so, the structure should be like:
                <folder>/
                    ├─item border/
                    │   ├─data/
                    │   └─pack.mcmeta
                    └─updator/
                        ├─impossible_items.json
                        ├─README.md
                        └─updator.py
            2. run this method
            3. select directory
                .minecraft/
                    └─versions/
                        └─<version>     << select this then click `select folder`
            4. this method will parse game client version, datapack version, items list
        """
        # set user input: select game client version under .minecraft/versions
        client: 'Path' = cls.select_version()
        # validation test
        if not cls.check_version_jar(client):
            raise RuntimeError('selected .jar file is not supported minecraft client or not a minecraft client.')
        # set list, version data from `<version>.jar`
        cls.get_jar_data(client)
        # screen items list
        filteredItems: 'list[str]' = cls.item_filter(cls.itemList)
        # write to `mcfunction`
        cls.write_init_code(filteredItems)
        # write `pack.mcmeta`
        cls.update_pack_meta()

# =======

if __name__ == '__main__':
    # when this script runs standalone
    CodeUpdater.update_code()