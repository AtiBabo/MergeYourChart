import ttkbootstrap as tb
import infocounter
import tkinter
import json
from tkinter import filedialog, ttk, messagebox

#TODO 메인화면 꾸미면 끝 ㅈㅈ
#TODO Changhyeon 타일pos찍을수있게만들어주세요
#TODO Changhyeon 테마변경
#TODO Jongyeol 언어팩?

# 메인 윈도우 생성
window = tb.Window(themename="darkly")
window.title("Merge Your Charts ( No virus ) ( FOR FREE! ) ( But free version ) ( Buy PRO! )")
window.geometry("640x400+100+100")
window.resizable(False, False)

# # 번역을 하다
# def load_language(lang_code):
#     with open(f"lang/{lang_code}.json", "r", encoding="utf-8") as file:
#         return json.load(file)

# 파일 선택 함수
def choosing_func():
    # 최종 병합 함수
    def merging_func(tree):
        # Treeview에서 모든 항목을 가져와 리스트로 정리
        order = []
        for item in tree.get_children(): order.append(tree.item(item)["values"])
        
        result = messagebox.askyesno("Info", "Are you sure you want to merge it like this?")
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
            with open(file[-1], "r", encoding="utf-8-sig") as json_file:
                data: dict = json.loads(infocounter.adofai_jeongsanghwa(json_file.read()))
            
            if index == 1: final["settings"].update(data["settings"]) # 1번일 경우 settings옮기기
            
            for line in data["actions"]: # 이벤트 병합
                try:
                    line["floor"] = int(line["floor"]) + len(final["angleData"])
                    print(line)
                    final["actions"].append(line)
                except: print("Can't find the floor")
            
            for line in data["decorations"]: # 장식 병합
                try:
                    line["floor"] = int(line["floor"]) + len(final["angleData"])
                    print(line)
                    final["decorations"].append(line)
                except: print("Can't find the floor")
            
            final["angleData"] += data["angleData"] # 타일 병합
        
        folder_path = filedialog.askdirectory(title="Choic the folder")
        
        with open(f"{folder_path}/{title}", "w", encoding="utf-8-sig") as file_write: # 최종 저장
            json.dump(final, file_write, indent=4, ensure_ascii=False)
        
        messagebox.showinfo("info", "Merge success.")
        
        merging_window.quit()
        merging_window.destroy()
        window.deiconify() # 메인 윈도우 복원
    
    file_paths = filedialog.askopenfilenames(
        title="Select files", 
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
        tree.heading("index", text="Index")
        tree.heading("file_name", text="File Name")
        tree.heading("tiles", text="Tiles")
        tree.heading("events", text="Events")
        tree.heading("decorations", text="Decorations")
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
            text="Export",
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
    
    choice_button = tb.Button(
        window, 
        text="Import",
        style="Custom.TButton",
        bootstyle="primary",
        command=choosing_func
    )
    choice_button.pack(side="top", expand=True)
    
    window.mainloop()

if __name__ == "__main__":
    main_window()