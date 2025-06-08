import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from bcrypt_utils import check_password
import app_state

EXCEL_PATH = "USER_DOCS.xlsx"

def load_credentials(path):
    credentials = {}
    try:
        wb = load_workbook(path)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            credentials[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return credentials

def create_login_frame(root, switch_to_join, on_login_success):
    frame = tk.Frame(root)

    tk.Label(frame, text="로그인", font=("Arial", 16)).pack(pady=10)

    tk.Label(frame, text="ID").pack()
    entry_id = tk.Entry(frame)
    entry_id.pack()

    tk.Label(frame, text="Password").pack()
    entry_pw = tk.Entry(frame, show="*")
    entry_pw.pack()

    def try_login():
        user_id = entry_id.get().strip()
        password = entry_pw.get().strip()

        credentials = load_credentials(EXCEL_PATH)

        if user_id not in credentials:
            messagebox.showinfo("로그인 실패", "존재하지 않는 아이디입니다.")
        elif not check_password(password, credentials[user_id]):
            messagebox.showwarning("로그인 실패", "비밀번호가 틀렸습니다.")
        else:
            messagebox.showinfo("로그인 성공", f"{user_id}님 환영합니다!")
            app_state.user_id = user_id
            on_login_success(user_id)

    tk.Button(frame, text="로그인", command=try_login).pack(pady=10)
    tk.Button(frame, text="회원가입", command=switch_to_join).pack()

    return frame
