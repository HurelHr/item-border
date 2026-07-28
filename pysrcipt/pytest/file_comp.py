from pathlib import Path
import json

def compare(li1: 'list', li2: 'list') -> 'list':
    result: 'list[dict[str, str]]' = []

    for item in li1:
        result.append({
            'item': item,
            'found': 'found' if item in li2 else '-'
        })
    
    return result

def store_result(name: 'str', obj) -> None:
    path = Path.home()/'desktop'/'result'
    path.mkdir(parents=True,exist_ok=True)
    path = path / name
    with path.open('w',encoding='utf-8') as js:
        json.dump(obj,js,ensure_ascii=False,indent=4)

def get_json() -> 'list':
    from tkinter import Tk
    from tkinter.filedialog import askopenfile
    tk = Tk()
    tk.withdraw()
    tk.attributes('-topmost',True)

    file = askopenfile('r')
    if file:
        return json.load(file)
    raise RuntimeError('user cancel to open the file')

def found_comp() -> None:
    js: 'list' = get_json()
    totalItems: 'int' = len(js)
    count: 'int' = 0
    for dt in js:
        if dt['found'] == 'found':
            count += 1
    print(f'result: {count}/{totalItems}')