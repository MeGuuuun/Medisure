import tkinter as tk
from tkinter import messagebox
import app_state

def create_interaction_frame(root, on_logout, switch_to_profile):
    frame = tk.Frame(root)

    tk.Button(frame, text="프로필로 돌아가기", command=switch_to_profile).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=10)

    return frame