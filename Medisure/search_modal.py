import tkinter as tk
from tkinter import messagebox
from data_fetcher import fetch_pill_info

def open_modal(parent):
    modal = tk.Toplevel(parent)
    modal.title("약 추가")
    modal.geometry("400x400")
    modal.resizable(False, False)

    modal.transient(parent)
    modal.grab_set()

    # 약물 검색
    tk.Label(modal, text="약물명 입력").pack()
    pill_entry = tk.Entry(modal)
    pill_entry.pack()

    def search_pill():
        pill_name = pill_entry.get().strip()
        if not pill_name:
            messagebox.showwarning("입력 오류", "약물명을 입력하세요.")
            return

        result = fetch_pill_info(pill_name)
        if result:
            print("🔍 검색 결과:")
            print(result)
            modal.destroy()
        else:
            print("❌ 검색 실패 또는 결과 없음")
            modal.destroy()

    tk.Button(modal, text="약물 검색 (콘솔 출력)", command=lambda:search_pill()).pack(pady=10)
    tk.Button(modal, text="취소", command=modal.destroy).pack(pady=5)

    parent.wait_window(modal)