__version__ = "1.0.0"
__doc__ = """
this is update script for item border datapack.
call CodeUpdater.code_update() to update
"""

from typing import (
    Union,
    Optional,
    TYPE_CHECKING
)
from pathlib import Path
from zipfile import ZipFile
import json

if TYPE_CHECKING:
    from zipfile import ZipInfo
    
UPDATOR_HOME: 'Path' = Path(__file__).parent
PACK_HOME: 'Path' = UPDATOR_HOME.parent

ITEMS_PER_PAGE: 'int' = 50

def folderselector(path: 'Union[Path, str, None]'=None, title: 'Optional[str]'=None) -> 'Path':
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
    
    tk = Tk()
    tk.withdraw()
    tk.attributes('-topmost', True)
    
    dir = askdirectory(
        initialdir=path,
        title=title
    )
    tk.destroy()
    if dir:
        return Path(dir)
    raise RuntimeError('user not select directory')

def collect_items(path: 'Path') -> 'list[Path]':
    result: 'list[Path]' = []
    for content in path.iterdir():
        if content.is_file(): result.append(content)
    return result

def collect_to_json(path: 'Path', fileName: 'str', items: 'list[Path]') -> None:
    path.mkdir(parents=True, exist_ok=True)
    path = path / fileName
    itemNames: 'list[str]' = [f'minecraft:{item.name.replace(item.suffix, "")}' for item in items]
    with path.open('w', encoding='utf-8') as js:
        json.dump(itemNames, js, ensure_ascii=False, indent=4)

def collect_to_csv(path: 'Path', items: 'list[str]') -> None:
    path.mkdir(parents=True, exist_ok=True)
    path = path / f'items.csv'
    with path.open('w', encoding='utf-8') as cv:
        cv.write('\n'.join(items))

def parse_registries(path: 'Path', report: 'Path') -> None:
    path = path / 'registries.json'
    with path.open(encoding='utf-8') as js:
        reg: 'dict' = json.load(js)
    items: 'list' = list(reg['minecraft:item']['entries'].keys())
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open('w',encoding='utf-8') as js:
        json.dump(items, js, ensure_ascii=False,indent=4)
        
def default_minecraft_path() -> 'Path':
    return Path.home() / 'AppData' / 'Roaming' / '.minecraft'

class CodeUpdater:
    GAME_VERSION: 'str' = ''
    PACK_VERSION: 'dict' = {}
    itemList: 'list[str]' = []

    @staticmethod
    def version_selector() -> 'Path':
        gamePath: 'Path' = default_minecraft_path()
        if gamePath.exists():
            return folderselector(path=default_minecraft_path() / 'versions', title='select minecraft version')
        else:
            return folderselector(title='select your minecraft folder and its version')

    @staticmethod
    def get_version_jar(path: 'Path') -> 'Path':
        versionJar: 'Optional[Path]' = None
        for f in path.iterdir():
            if f.suffix == '.jar':
                versionJar = f
        if versionJar is None:
            raise ValueError('minecraft is not installed or invalid path. please check valid version path or install minecraft before run this script.')
        return versionJar

    @classmethod
    def get_items_list(cls, jarFile: 'ZipFile') -> None:
        itemsFolder: 'Path' = Path('assets/minecraft/items')
        items: 'list[ZipInfo]' = [fi for fi in jarFile.filelist if not fi.is_dir() and Path(fi.filename).is_relative_to(itemsFolder)]

        def basename(f: 'Path') -> 'str':
            return f.name.replace(f.suffix, '')
        cls.itemList = [f'minecraft:{basename(Path(f.filename))}' for f in items]

    @classmethod
    def get_version_data(cls, jarFile: 'ZipFile') -> None:
        version: 'dict' = json.load(jarFile.open('version.json'))
        cls.GAME_VERSION = version.get("name", "unknown version")
        cls.PACK_VERSION = version.get("pack_version", {})
        
    @classmethod
    def get_jar_data(cls, path: 'Path') -> None:
        with ZipFile(path, 'r') as jar:
            cls.get_version_data(jar)
            cls.get_items_list(jar)

    @staticmethod
    def item_filter(items: 'list[str]') -> 'list[str]':
        with (UPDATOR_HOME / 'impossible_items.json').open(encoding='utf-8') as js:
            invalidItems: 'list[str]' = json.load(js)
        def screen(itemCode: 'str') -> 'bool':
            return not any(inv in itemCode for inv in invalidItems)
        return [item for item in items if screen(item)]

    @staticmethod
    def get_dialog_body(items: 'list[str]') -> 'str':
        ITEM_COMMAND: 'str' = '{{type:"minecraft:item",item:{{id:"{code}"}},description:{{"text":"[ ❌ ]","color":"red","bold":true}}}}'
        return f'{','.join(ITEM_COMMAND.format(code=itemName) for itemName in items)}'

    @classmethod
    def write_init_code(cls, itemCods: 'list[str]') -> None:
        CODEX_COMMAND: 'str' = 'data modify storage item_border:codex itemCodex append value {{body:[{{type:"minecraft:plain_message",contents:"Page: {index}"}},{body}]}}\n'
        INDEX_COMMAND: 'str' = 'data modify storage item_border:codex index append value {{id:"{item}", page:{index}}}\n'
        pageItem: 'dict[int, list[str]]' = {}
        for num, item in enumerate(itemCods):
            pageNums: 'int' = num // ITEMS_PER_PAGE
            if pageNums in pageItem:
                pageItem[pageNums].append(item)
            else:
                pageItem[pageNums] = [item]
        endPage: 'int' = max(pageItem.keys())
        with open(UPDATOR_HOME.parent / 'item border' / 'data' / 'item_border' / 'function' / 'dialog' / 'init_codex.mcfunction', 'w', encoding='utf-8') as mcfunc:
            mcfunc.write(f'# Game Version: 1.{cls.GAME_VERSION}\n')
            mcfunc.write('data modify storage item_border:codex itemCodex set value []\n')
            mcfunc.write('data modify storage item_border:codex index set value []\n')
            for page, items in pageItem.items():
                mcfunc.write(CODEX_COMMAND.format(body=cls.get_dialog_body(items), index=f'{page} / {endPage}'))

            for page, items in pageItem.items():
                for item in items:
                    mcfunc.write(INDEX_COMMAND.format(item=item, index=page))
                    
    @classmethod
    def update_pack_meta(cls) -> None:
        packMcMeta: 'Path' = PACK_HOME / 'item border' / 'pack.mcmeta'
        PACK_DESCRIPTION: 'str' = "item border datapack item list for {version}"
        if packMcMeta.exists():
            with open(packMcMeta, 'r', encoding='utf-8') as js:
                packData: 'dict' = json.load(js)
                packData['pack']['description'] = PACK_DESCRIPTION.format(version=cls.GAME_VERSION)
                packVersion: 'list[int]' = [cls.PACK_VERSION.get('data_major', 0), cls.PACK_VERSION.get('data_minor', 0)]
                packData['pack']['min_format'] = packVersion
                packData['pack']['max_format'] = packVersion
            with open(packMcMeta, 'w', encoding='utf-8') as js:
                json.dump(packData, js, indent=4)
        else:
            with open(packMcMeta, 'w', encoding='utf-8') as js:
                packVersion = [cls.PACK_VERSION.get('data_major', 0), cls.PACK_VERSION.get('data_minor', 0)]
                packData = {
                    "pack": {
                        "description": PACK_DESCRIPTION.format(version=cls.GAME_VERSION),
                        "min_format": packVersion,
                        "max_format": packVersion
                    }
                }
                json.dump(packData, js, indent=4)

    @classmethod
    def update_code(cls) -> None:
        vpath: 'Path' = cls.version_selector()
        cls.get_jar_data(cls.get_version_jar(vpath))
        filteredItems: 'list[str]' = cls.item_filter(cls.itemList)
        cls.write_init_code(filteredItems)
        cls.update_pack_meta()

# =======

if __name__ == '__main__':
    CodeUpdater.update_code()