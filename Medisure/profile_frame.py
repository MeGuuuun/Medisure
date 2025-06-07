import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook, Workbook

EXCEL_PATH = "USER_DOCS.xlsx"

def create_profile_frame(root, on_logout):
    frame = tk.Frame(root)

    tk.Label(frame, text="마이페이지", font=("Arial", 16)).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=20)

    return frame