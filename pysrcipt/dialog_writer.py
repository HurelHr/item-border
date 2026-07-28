from pathlib import Path

WORKSPACE: 'Path' = Path(__file__).parent.parent

COMMAND: 'str' = """$dialog show @s {{
type:"minecraft:multi_action",
title:{{"text":"Collections"}},
body:[{items},actions:[{{label:"prev"}},{{label:"nxt"}}]]
}}
"""

BODY_ELEMENT: 'str' = '{{type:"minecraft:item",item:{{id:"$(itemCodex[{index}].name)",description:"$(itemCodex[{index}].collected)"}}}}'

ITEMS_PER_PAGE: 'int' = 2

def write_dialog() -> None:
    elements: 'list[str]' = [BODY_ELEMENT.format(index=index) for index in range(ITEMS_PER_PAGE)]
    command: 'str' = COMMAND.replace('\n', '')
    command = command.format(items=",".join(elements))
    with (WORKSPACE / 'item border' / 'data' / 'item_border' / 'function' / 'dialog_page.mcfunction').open('w', encoding='utf-8') as mcfunc:
        mcfunc.write(command)

# dialog list는 고정.
# page, start index, pagesize -> scoreboard에 등록
# start index = page * pagesize 로 등록
# temp = all[start_index..]으로 슬라이싱

    # slicinig #1
    # # 1. 계산용 임시 점수판에 현재 유저의 페이지 번호(예: 2페이지)를 복사합니다.
    # scoreboard players operation #calc_idx item_border = @s current_page

    # # 2. 한 페이지당 슬롯 개수인 고정 상수 45를 등록합니다.
    # scoreboard players set #page_size item_border 45

    # # 3. [★수학적 연산]: 현재페이지(2) * 45 = 90 점을 계산해 냅니다.
    # scoreboard players operation #calc_idx item_border *= #page_size item_border

    # # 4. 계산된 90 점을 매크로 함수가 읽을 수 있도록 스토리지 변수에 캐스팅 대입합니다.
    # execute store result storage item_border:database temp.start_idx int 1 run scoreboard players get #calc_idx item_border

    # # 5. 완성된 동적 start_idx 주머니를 들고 구간 슬라이싱 부모 함수 호출!
    # function item_border:page_render with storage item_border:database temp
    
    # =====
    
    # slicinig #2
    # 1. 임시 연산용 렌더링 버퍼에 1,531개 전체 원본 데이터를 통째로 Deep Copy 복사합니다 (O(1) 비용).
    # data modify storage item_border:database page_buffer set from storage item_border:database all

    # # 2. 앞선 곱셈 연산으로 계산된 start_idx (예: 90점)를 카운터 스코어보드 변수로 탑재합니다.
    # scoreboard players operation #count item_border = @s start_idx

    # # 3. [★이것이 진짜 바닐라 슬라이싱 우회] 
    # # 앞부분 90개를 잘라내기 위한 초고속 카운터다운 서브루틴 함수 호출
    # execute if score #count item_border matches 1.. run function item_border:slice_remover

    # `slice_remover.mcfunction`
    # 배열의 맨 앞인 [0]번 원소를 영구 파괴(삭제)합니다. 
    # # 0번이 지워지는 순간, 뒤에 있던 1번, 2번... 1500번 원소들이 메모리 상에서 자동으로 한 칸씩 앞으로 당겨집니다.
    # data remove storage item_border:database page_buffer[0]

    # # 카운트 1 감소 후, 남아있다면 나 자신을 재귀 호출 (90번 연타)
    # scoreboard players remove #count item_border 1
    # execute if score #count item_border matches 1.. run function item_border:slice_remover

    # =====
    
    # slicinig #2

    # all_items에 [{id, text, page}]로 정의
    # python에서 page_length마다 page 키에 대한 값 주입
    # {page:"$(page)"}로 조회할때 배열로 반환됨.

# temp를 dialog에 던짐(with temp)
# 경계값 처리:
    # # [이전 페이지 트리거 함수: prev_page.mcfunction]
    # # 해설: 현재 유저의 페이지 번호가 '2페이지 이상'일 때만 안전하게 1페이지를 깎고 화면을 새로고침합니다.
    # execute if score @s current_page matches 2.. run scoreboard players remove @s current_page 1
    # execute if score @s current_page matches 2.. run function item_border:page_control

    # # 만약 1페이지인데 억지로 이전을 눌렀다면 가벼운 경고 사운드나 텍스트를 출력합니다.
    # execute if score @s current_page matches 1 run title @s actionbar {"text":"🚫 첫 번째 페이지입니다.", "color":"red"}

    # # [다음 페이지 트리거 함수: next_page.mcfunction]
    # # 1. 다음 페이지로 가기 위해 가상으로 계산해 볼 예견 점수판(#next_check)을 준비합니다.
    # scoreboard players operation #next_check item_border = @s current_page
    # scoreboard players add #next_check item_border 1  # (예: 2페이지였다면 다음인 3페이지로 세팅)

    # # 2. 다음 페이지의 시작 인덱스(3 * 45 = 135)를 미리 연산하여 임시 스토리지 변수에 대입합니다.
    # scoreboard players set #page_size item_border 45
    # scoreboard players operation #next_check item_border *= #page_size item_border
    # execute store result storage item_border:database temp.next_start int 1 run scoreboard players get #next_check item_border

    # # 3. [★질문하신 핵심 예외처리] 호출 직전, 다음 인덱스 주소록(예: all[135])에 진짜 데이터가 들어있는지 검사합니다.
    # # 데이터가 실존할 때만(if data) 안전하게 유저의 진짜 페이지 변수를 1 올리고 다음 화면을 렌더링합니다!
    # $ execute if data storage item_border:database all[$(temp.next_start)] run scoreboard players add @s current_page 1
    # $ execute if data storage item_border:database all[$(temp.next_start)] run function item_border:page_control

    # # 만약 다음 인덱스가 텅 비어있다면(unless data) 마지막 페이지이므로 넘기지 않고 막아버립니다.
    # $ execute unless data storage item_border:database all[$(temp.next_start)] run title @s actionbar {"text":"🚫 마지막 페이지입니다.", "color":"red"}

    # =====
    # for `page` key:
    # [다음 페이지 트리거: next_page.mcfunction]
    # # 1. 예견용 임시 점수판에 다음 페이지 번호를 계산합니다.
    # scoreboard players operation #next_page item_border = @s current_page
    # scoreboard players add #next_page item_border 1

    # # 2. 계산된 다음 페이지 번호를 매크로가 읽을 수 있도록 스토리지에 캐스팅 대입합니다.
    # execute store result storage item_border:database temp.next_page int 1 run scoreboard players get #next_page item_border

    # # 3. [★개발자님의 소름 돋는 1줄 예외처리]
    # # 다음 페이지용 {page: N} 그룹 뭉텅이에서 0번 인덱스가 실존하는지 찔러봅니다.
    # # 데이터가 들어있다면(if data) 안전하게 유저의 실제 페이지 번호를 1 올리고 화면을 갱신합니다!
    # $ execute if data storage item_border:database all[{page: $(temp.next_page)}][0] run scoreboard players add @s current_page 1
    # $ execute if data storage item_border:database all[{page: $(temp.next_page)}][0] run function item_border:page_control

    # # 만약 다음 페이지의 0번 원소가 텅 비어있다면(unless data) 마지막 페이지이므로 철저히 막아버립니다.
    # $ execute unless data storage item_border:database all[{page: $(temp.next_page)}][0] run title @s actionbar {"text":"🚫 마지막 페이지입니다.", "color":"red"}
