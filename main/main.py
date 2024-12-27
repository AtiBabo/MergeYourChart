import ttkbootstrap as tb
import infocounter
import tkinter
import json
import sys
import os
import subprocess
from tkinter import filedialog, ttk, messagebox

#TODO Changhyeon 타일pos찍을수있게만들어주세요 <- 나중에 할게요 계산 뜯어고쳐야 해서 너무 힘들듯
#TODO Jongyeol 언어팩 + 시간 <- 언어팩은 만들었어요 / 시간은 계산하기 힘든데 해볼게요
#TODO Jongyeol 총합 <- 나중에 할게요 2222 가 아니라 지금해볼게요
#TODO 선택적인 병합
#TODO 제대로된 adofai파일인지 확인
#TODO 내보낼때 경로선택

# 문제가 있는 얼불춤 파일이 아닌지 확인
def valid_adofai():
    pass # 나 졸려 잘랭

def resource_path(relative_path):
    """PyInstaller 빌드 후 리소스 파일의 경로를 반환"""
    try:
        # PyInstaller 실행 환경에서 임시 디렉토리를 반환
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경에서는 현재 디렉토리를 반환
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 재시작
def running_ide():
    return not hasattr(sys, 'frozen')  # exe로 빌드되면 frozen 속성이 생김

def restart():
    if running_ide():
        print("IDE에서 실행 중입니다. exit()로 종료합니다.")
        exit()  # IDE에서는 exit()로 종료
    else:
        print("EXE 파일로 실행 중입니다. 재시작합니다.")
        try:
            current_exe = sys.executable
            subprocess.Popen([current_exe])
            sys.exit(0)
        except Exception as e:
            print(f"프로그램 재시작 실패: {e}")

# 번역을 하다
def load_language(lang_code):
    with open(resource_path(f"lang/{lang_code}.json"), "r", encoding="utf-8") as file:
        return json.load(file)

# 언어를 적용하다
with open(resource_path("save.json"), "r", encoding="utf-8-sig") as file:
    data: dict = json.loads(file.read())

if data["lang"]:
    try: lang = load_language(data["lang"])
    except FileNotFoundError: lang = load_language("en")
else:
    lang = load_language("en")

# 메인 윈도우 생성
window = tb.Window(themename="darkly")
window.title(lang["Merge Your Charts ( No virus ) ( FOR FREE! ) ( But free version ) ( Buy PRO! )"])
window.geometry("640x400+100+100")
window.resizable(False, False)

# 파일 선택 함수
def choosing_func():
    # 최종 병합 함수
    def merging_func(tree):
        # Treeview에서 모든 항목을 가져와 리스트로 정리
        order = []
        for item in tree.get_children(): order.append(tree.item(item)["values"])
        
        result = messagebox.askyesno(lang["Info"], lang["Are you sure you want to merge it like this?"])
        if result == False: return
        
        title = order[0][1]
        
        # 병합
        final = {
            "angleData": [],
            "settings": {},
            "actions": [],
            "decorations": []
        }
        
        for index, file in enumerate(order, 1):
            with open(resource_path(file[-1]), "r", encoding="utf-8-sig") as json_file:
                data: dict = json.loads(infocounter.adofai_jeongsanghwa(json_file.read()))
            
            if index == 1: final["settings"].update(data["settings"]) # 1번일 경우 settings옮기기
            
            for line in data["actions"]: # 이벤트 병합
                try:
                    line["floor"] = int(line["floor"]) + len(final["angleData"])
                    final["actions"].append(line)
                except: print("Can't find the floor")
            
            for line in data["decorations"]: # 장식 병합
                try:
                    line["floor"] = int(line["floor"]) + len(final["angleData"])
                    final["decorations"].append(line)
                except: print("Can't find the floor")
            
            final["angleData"] += data["angleData"] # 타일 병합
        
        folder_path = filedialog.askdirectory(title=lang["Choice the folder"])
        name, extension = os.path.splitext(title)
        
        with open(resource_path(f"{folder_path}/{name}_MYC{extension}"), "w", encoding="utf-8-sig") as file_write: # 최종 저장
            json.dump(final, file_write, indent=4, ensure_ascii=False)
        
        messagebox.showinfo(lang["Info"], lang["Merge success."])
        
        merging_window.quit()
        merging_window.destroy()
        window.deiconify() # 메인 윈도우 복원
    
    file_paths = filedialog.askopenfilenames(
        title=lang["Select files"], 
        filetypes=[(".adofai", "*.adofai")]
    )
    
    if file_paths:
        window.withdraw() # 메인 윈도우 숨기기
        
        merging_window = tb.Toplevel()
        merging_window.title("Merge Manager")
        merging_window.geometry("950x400+100+100")
        merging_window.resizable(False, False)
        
        # 왼쪽 프레임 생성
        left_frame = tkinter.Frame(merging_window, bg="black")
        left_frame.pack(side="left", fill="y")
        
        # 오른쪽 프레임 생성
        right_frame = tkinter.Frame(merging_window, bg="black")
        right_frame.pack(side="right", fill="y")
        
        # Treeview 위젯 생성
        tree = ttk.Treeview(
            left_frame, 
            columns=("index", "file_name", "tiles", "events", "decorations", "directory"), 
            show="headings", 
            style="Treeview"
        )
        
        # 열 설정
        tree.heading("index", text=lang["Index"])
        tree.heading("file_name", text=lang["File Name"])
        tree.heading("tiles", text=lang["Tiles"])
        tree.heading("events", text=lang["Events"])
        tree.heading("decorations", text=lang["Decorations"])
        tree.heading("directory", text="")
        
        # 열 너비 설정
        tree.column("index", width=50, anchor="center")
        tree.column("file_name", width=300)
        tree.column("tiles", width=100, anchor="center")
        tree.column("events", width=100, anchor="center")
        tree.column("decorations", width=100, anchor="center")
        tree.column("directory", width=0, stretch=tkinter.NO)
        
        # 데이터 삽입
        for idx, file in enumerate(file_paths, 1):
            tree.insert(
                "", 
                "end", 
                value=(
                    idx, 
                    file.split("/")[-1], 
                    infocounter.counter(path=file, mod="angleData"), 
                    infocounter.counter(path=file, mod="actions"), 
                    infocounter.counter(path=file, mod="decorations"),
                    file
                )
            )
        
        export_button = tb.Button(
            merging_window, 
            text=lang["Export"],
            style="Custom.TButton",
            bootstyle="primary",
            command=lambda: merging_func(tree=tree)
        )
        
        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y", expand=True, pady=10)
        
        # Treeview와 스크롤바 연결
        tree.config(yscrollcommand=scrollbar.set)
        
        # 드래그 앤 드롭 이벤트 바인딩
        tree.bind("<ButtonPress-1>", lambda event: start_drag(event, tree))
        tree.bind("<B1-Motion>", lambda event: dragging(event, tree))
        tree.bind("<ButtonRelease-1>", lambda event: drop(event, tree))
        
        # 위젯 배치
        tree.pack(fill="y", expand=True, padx=10, pady=10, anchor="w")
        export_button.pack(side="top", expand=True, padx=10, pady=10)
        
        merging_window.protocol('WM_DELETE_WINDOW', lambda: restore_mainwindow(merging_window)) # 윈도우가 닫혔을 경우 restore_mainwindow함수 실행
        
        merging_window.mainloop()
    else: print("No file selected")

# 드래그 앤 드롭 기능을 위한 함수
dragged_item = None
target_item = None

def start_drag(event, tree):
    global dragged_item
    item = tree.identify_row(event.y)
    
    if item:
        dragged_item = item
        tree.item(dragged_item, tags=("dragged",))  # 태그 추가
        update_styles(tree)

def dragging(event, tree):
    global target_item
    target_item = tree.identify_row(event.y)
    
    if target_item and target_item != dragged_item: update_styles(tree)

def drop(event, tree):
    global dragged_item, target_item
    target_item = tree.identify_row(event.y)
    
    if dragged_item and target_item and dragged_item != target_item:
        dragged_index = tree.index(dragged_item)
        target_index = tree.index(target_item)
        
        # 데이터 재정렬
        children = tree.get_children()
        data = [tree.item(child)["values"] for child in children]
        data.insert(target_index, data.pop(dragged_index))
        
        # Treeview 비우고 데이터 다시 추가
        for item in tree.get_children():
            tree.delete(item)
        for idx, row in enumerate(data, 1):
            tree.insert("", "end", values=(idx,) + tuple(row[1:]))
    
    dragged_item = None
    target_item = None
    update_styles(tree)

def update_styles(tree):
    for item in tree.get_children():
        tree.item(item, tags=())
    
    if dragged_item:
        tree.item(dragged_item, tags=("dragged",))
    
    if target_item:
        tree.item(target_item, tags=("target",))
    
    tree.tag_configure("dragged", background="lightblue")
    tree.tag_configure("target", background="lightgreen")

# 메인 윈도우 복원 함수
def restore_mainwindow(merging_window):
    merging_window.destroy() # 새로운 윈도우 종료
    window.deiconify() # 메인 윈도우 복원

# 메인 윈도우
def main_window():
    # 스타일 생성
    style = tb.Style()
    style.configure('Custom.TButton', font=("Helvetica", 14))
    
    # 언어 선택
    def change_language(lang_code):
        global lang
        
        result = messagebox.askyesno(lang["Info"], lang["You must restart the program to change the language. Would you like to restart?"])
        if result == False: return
        
        with open(resource_path("save.json"), "r", encoding="utf-8-sig") as file:
            data: dict = json.loads(file.read())
        
        data["lang"] = lang_code
        
        with open(resource_path("save.json"), "w", encoding="utf-8-sig") as file:
            json.dump(data, file, indent=4)
        
        restart()
    
    language_label = tb.Label(window, text=lang["Select language"], bootstyle="primary", font=("Helvetica", 16))
    
    # 언어 선택 콤보박스 추가
    language_selector = ttk.Combobox(window, values=["en", "ko-KR"], state="readonly")
    language_selector.bind("<<ComboboxSelected>>", lambda e: change_language(language_selector.get()))
    
    choice_button = tb.Button(
        window, 
        text=lang["Import"],
        style="Custom.TButton",
        bootstyle="primary",
        command=choosing_func
    )
    
    language_label.pack(anchor="center", pady=20)
    language_selector.pack()
    choice_button.pack(side="top", pady=100)
    
    window.mainloop()

if __name__ == "__main__":
    main_window()