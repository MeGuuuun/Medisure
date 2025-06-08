import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from data_fetcher import fetch_pill_info
import app_state

EXCEL_PATH = "USER_DOCS.xlsx"

user_id = app_state.user_id

def create_interaction_frame(root, on_logout, switch_to_profile):
    frame = tk.Frame(root)

    # ==== Frame 선언 ====

    result_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    result_frame.pack(fill="x", padx=10, pady=10)
    result_frame.pack_propagate(False)

    details_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    details_frame.pack(fill="x", padx=10, pady=10)
    details_frame.pack_propagate(False)

    tk.Button(frame, text="프로필로 돌아가기", command=switch_to_profile).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=10)

    return frame