import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from data_fetcher import fetch_pill_info

EXCEL_PATH = "USER_DOCS.xlsx"

def load_user_info(user_id):
    try:
        wb = load_workbook(EXCEL_PATH)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] == user_id:
                return row
        return None

    except Exception as e:
        print("엑셀 오류: ",e)
        return None

def center_window(win):
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_width()) // 2
    y = (win.winfo_screenheight() - win.winfo_height()) // 2
    win.geometry(f"+{x}+{y}")

def create_profile_frame(root, on_logout, user_id):
    frame = tk.Frame(root)
    user_info = load_user_info(user_id)

    tk.Label(frame, text="나의 정보", font=("Arial", 16)).pack(pady=10)

    # ==== 사용자 정보 ====
    top_frame = tk.Frame(frame, bg='lightblue', height=100, width=400)
    top_frame.pack(fill="x", padx=10, pady=10)
    top_frame.pack_propagate(False)  # 고정 높이 유지

    # user_info가 있는 경우 줄바꿈 포함한 문자열 생성
    if user_info:
        info_text = "\n".join(str(item) for item in user_info[:5])
        user_pills = user_info[5:]
    else:
        info_text = "사용자 정보가 없습니다."

    # 라벨을 정중앙에 배치
    label = tk.Label(top_frame, text=info_text, bg='lightblue', justify="center")
    label.place(relx=0.5, rely=0.5, anchor="center")

    # ==== 약물 검색 ====

    search_frame = tk.Frame(frame, bg='green', height=100, width=400)
    search_frame.pack(fill="x", padx=10, pady=10)
    search_frame.pack_propagate(False)

    # 약물 검색
    tk.Label(search_frame, text="약물명 입력").pack()
    pill_entry = tk.Entry(search_frame)
    pill_entry.pack()


    def search_pill():
        pill_name = pill_entry.get().strip()
        if not pill_name:
            messagebox.showwarning("입력 오류", "약물명을 입력하세요.")
            return

        results = fetch_pill_info(pill_name)
        if results:
            print("🔍 검색 결과:")
            print(results)
        else:
            print("❌ 검색 실패 또는 결과 없음")

        # 검색 결과 팝업 창 생성
        popup = tk.Toplevel(search_frame)
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.transient(search_frame)
        popup.grab_set()

        center_window(popup)

        scrollbar = tk.Scrollbar(popup)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(popup, yscrollcommand=scrollbar.set, width=50, height=15)
        for name in results:
            listbox.insert(tk.END, name)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        def on_select(event):
            if listbox.curselection():
                index = listbox.curselection()[0]

                # 선택된 항목 배경색 변경
                listbox.itemconfig(index, bg="#d3d3d3")

                selected = listbox.get(index)
                print("선택한 약물 : ", selected)

                # 5초 후 팝업 사라짐
                popup.after(5000, popup.destroy())

        listbox.bind("<<ListboxSelect>>", on_select)

    tk.Button(search_frame, text="약물 검색 (콘솔 출력)", command=lambda:search_pill()).pack(pady=10)


    # ==== 약물 정보 ====

    bottom_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    bottom_frame.pack(fill="x", padx=10, pady=10)
    bottom_frame.pack_propagate(False)

    pill_list_label = tk.Label(bottom_frame,text="복용 중인 약들", bg='white')
    pill_list_label.pack(pady=10)

    if user_pills and user_pills[0] is not None and len(user_pills[0]) > 0:
        for pill in user_pills:
            print(pill)
            tk.Label(bottom_frame, text=pill).pack()
    else:
        print("no")
        tk.Label(bottom_frame, text="⚠️ 저장된 약물이 없습니다.").pack()


    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=20)

    return frame