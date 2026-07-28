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

ITEMS_PER_PAGE: 'int' = 50
GAME_VERSION: 'str' = ''

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
    global GAME_VERSION
    path.mkdir(parents=True, exist_ok=True)
    path = path / f'1.{GAME_VERSION}_items.csv'
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

def version_selector() -> 'Path':
    gamePath: 'Path' = default_minecraft_path()
    if gamePath.exists():
        return folderselector(path=default_minecraft_path() / 'versions', title='select minecraft version')
    else:
        return folderselector(title='select your minecraft folder and its version')

def get_version_data(path: 'Path') -> 'Path':
    global GAME_VERSION
    versionJar: 'Optional[Path]' = None
    for f in path.iterdir():
        if f.suffix == '.jar':
            versionJar = f
    if versionJar is None:
        raise ValueError('minecraft is not installed or invalid path. please check valid version path or install minecraft before run this script.')
    GAME_VERSION = versionJar.parent.name
    return versionJar

def get_items_list(jarFile: 'Path') -> 'list[str]':
    itemsFolder: 'Path' = Path('assets/minecraft/items')
    with ZipFile(jarFile, 'r') as jar:
        items: 'list[ZipInfo]' = [fi for fi in jar.filelist if not fi.is_dir() and Path(fi.filename).is_relative_to(itemsFolder)]

    def basename(f: 'Path') -> 'str':
        return f.name.replace(f.suffix, '')
    return [f'minecraft:{basename(Path(f.filename))}' for f in items]

def item_filter(items: 'list[str]') -> 'list[str]':
    with (UPDATOR_HOME / 'impossible_items.json').open(encoding='utf-8') as js:
        invalidItems: 'list[str]' = json.load(js)
    def screen(itemCode: 'str') -> 'bool':
        return not any(inv in itemCode for inv in invalidItems)
    return [item for item in items if screen(item)]

def get_dialog_body(items: 'list[str]') -> 'str':
    ITEM_COMMAND: 'str' = '{{type:"minecraft:item",item:{{id:"{code}"}},description:{{"text":"[ ❌ ]","color":"red","bold":true}}}}'
    return f'{','.join(ITEM_COMMAND.format(code=itemName) for itemName in items)}'

def write_init_code(itemCods: 'list[str]') -> None:
    global GAME_VERSION
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
        mcfunc.write(f'# Game Version: 1.{GAME_VERSION}\n')
        mcfunc.write('data modify storage item_border:codex itemCodex set value []\n')
        mcfunc.write('data modify storage item_border:codex index set value []\n')
        for page, items in pageItem.items():
            mcfunc.write(CODEX_COMMAND.format(body=get_dialog_body(items), index=f'{page} / {endPage}'))

        for page, items in pageItem.items():
            for item in items:
                mcfunc.write(INDEX_COMMAND.format(item=item, index=page))

def code_updator() -> None:
    vpath: 'Path' = version_selector()
    items: 'list[str]' = get_items_list(get_version_data(vpath))
    items = item_filter(items)
    write_init_code(items)


if __name__ == '__main__':
    code_updator()