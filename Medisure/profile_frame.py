import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from data_fetcher import fetch_pill_info
import app_state

EXCEL_PATH = "USER_DOCS.xlsx"

user_id = app_state.user_id

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

# 약물 추가 함수
def add_selected_to_excel(selected):
    try:
        wb = load_workbook(EXCEL_PATH)
    except Exception as e:
        print("error")

    ws = wb.active

    id_col = 1
    user_id = app_state.user_id

    pill_cols = list(range(6,10))

    target_row = None

    for row in range(2, ws.max_row + 1):
        cell_value = ws.cell(row=row, column=id_col).value
        if cell_value == user_id:
            target_row = row
            break

    inserted = False
    for col in pill_cols:
        if not ws.cell(row=target_row, column=col).value:
            ws.cell(row=target_row, column=col, value=selected)
            inserted = True
            break

    if not inserted:
        print("⚠️ 더 이상 약물 정보를 추가할 공간이 없습니다.")

    wb.save(EXCEL_PATH)


# 약물 정보 불러오는 함수
def refresh_pill_list(user_id, target_frame):
    # 기존에 표시된 약물 리스트 삭제 (중복 방지)
    for widget in target_frame.winfo_children():
        widget.destroy()

    pill_list_label = tk.Label(target_frame,text="복용 중인 약들", bg='white')
    pill_list_label.pack(pady=10)

    user_info = load_user_info(user_id)
    user_pills = user_info[5:]

    # 약물 삭제 함수
    def delete_pill(pill_name):
        wb = load_workbook(EXCEL_PATH)
        ws = wb.active

        row_index = None
        for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True),start=2):
            if str(row[0]) == user_id:
                row_index = i
                break

        if row_index is None:
            wb.close()
            print("error")
            return

        pills = [ws.cell(row=row_index, column=col).value for col in range(6,11)]

        # 삭제할 약 제거하고 순서 당기기
        pills = [pill for pill in pills if pill != pill_name]
        while len(pills) < 5 :
            pills.append(None)

        for idx, pill in enumerate(pills):
            ws.cell(row=row_index, column=5 + idx).value = pill

        wb.save(EXCEL_PATH)
        wb.close()

        refresh_pill_list(user_id, target_frame)

    for pill in user_pills:
        if pill:
            row_frame = tk.Frame(target_frame, bg='white')
            row_frame.pack(fill='x', padx=20, pady=3)

            label = tk.Label(row_frame, text=f"- {pill}", anchor="w", bg='white')
            label.pack(side='left', fill='x', expand=True)

            del_btn = tk.Button(row_frame, text="❌", command=lambda p=pill: delete_pill(p),
                                bg='white', fg='black', relief='solid', bd=1, padx=5, pady=1)
            del_btn.pack(side='right', padx=(5, 0))

def create_profile_frame(root, on_logout, switch_to_interaction):
    frame = tk.Frame(root)
    user_info = load_user_info(user_id)

    tk.Label(frame, text="나의 정보", font=("Arial", 16)).pack(pady=10)


    # ==== Frame 선언 ====
    top_frame = tk.Frame(frame, bg='lightblue', height=100, width=400)
    top_frame.pack(fill="x", padx=10, pady=10)
    top_frame.pack_propagate(False)  # 고정 높이 유지

    search_frame = tk.Frame(frame, bg='green', height=100, width=400)
    search_frame.pack(fill="x", padx=10, pady=10)
    search_frame.pack_propagate(False)

    bottom_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    bottom_frame.pack(fill="x", padx=10, pady=10)
    bottom_frame.pack_propagate(False)

    # ==== 사용자 정보 ====
    # user_info가 있는 경우 줄바꿈 포함한 문자열 생성
    if user_info:
        info_text = "\n".join(str(item) for item in user_info[:5])
    else:
        info_text = "사용자 정보가 없습니다."

    # 라벨을 정중앙에 배치
    label = tk.Label(top_frame, text=info_text, bg='lightblue', justify="center")
    label.place(relx=0.5, rely=0.5, anchor="center")

    # ==== 약물 검색 =====
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
                selected = listbox.get(listbox.curselection())
                print("선택한 약물 : ", selected)

                # 엑셀에 저장
                add_selected_to_excel(selected)

                refresh_pill_list(user_id, bottom_frame)

                # 배경색 바꾸기 (선택된 항목만)
                index = listbox.curselection()[0]
                listbox.itemconfig(index, bg="lightgray")

                # 0.5초 딜레이 후 팝업 닫기
                popup.after(500, popup.destroy)

        listbox.bind("<<ListboxSelect>>", on_select)

    tk.Button(search_frame, text="약물 검색 (콘솔 출력)", command=lambda:search_pill()).pack(pady=10)


    # ==== 약물 정보 ====

    refresh_pill_list(user_id, bottom_frame)

    # === 약물 상호작용 ====

    tk.Button(bottom_frame, text="약물 상호작용 확인하기",command=switch_to_interaction)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=20)

    return frame