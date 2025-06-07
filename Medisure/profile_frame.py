import tkinter as tk
from openpyxl import load_workbook
from search_modal import open_modal

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

def create_profile_frame(root, on_logout, user_id):
    frame = tk.Frame(root)
    user_info = load_user_info(user_id)

    tk.Label(frame, text="나의 정보", font=("Arial", 16)).pack(pady=10)

    # ==== 사용자 정보 ====
    top_frame = tk.Frame(frame, bg='lightblue', height=150, width=400)
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


    tk.Button(bottom_frame, text="약 추가", command=lambda: open_modal(root)).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=20)

    return frame