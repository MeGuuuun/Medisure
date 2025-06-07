import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook, Workbook
from data_fetcher import fetch_drug_info

EXCEL_PATH = "USER_DOCS.xlsx"

def create_profile_frame(root, on_logout):
    frame = tk.Frame(root)

    tk.Label(frame, text="마이페이지", font=("Arial", 16)).pack(pady=10)

    # 약물 검색
    tk.Label(frame, text="약물명 입력").pack()
    drug_entry = tk.Entry(frame)
    drug_entry.pack()

    def search_drug():
        drug_name = drug_entry.get().strip()
        if not drug_name:
            messagebox.showwarning("입력 오류", "약물명을 입력하세요.")
            return

        result = fetch_drug_info(drug_name)
        if result:
            print("🔍 검색 결과:")
            print(result)
        else:
            print("❌ 검색 실패 또는 결과 없음")

    tk.Button(frame, text="약물 검색 (콘솔 출력)", command=search_drug).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=20)

    return frame