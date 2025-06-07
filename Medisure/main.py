import tkinter as tk
from login_frame import create_login_frame
from join_frame import create_join_frame

def default_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - width) / 2)
    center_y = int((screen_height - height) / 2)
    root.geometry(f"{width}x{height}+{center_x}+{center_y}")
    root.resizable(False, False)

def main():
    root = tk.Tk()
    root.title("Login System")
    default_window(root, 450, 650)

    login_frame = create_login_frame(
        root,
        switch_to_join=lambda: switch_frame(join_frame),
        on_login_success=lambda: print("로그인 성공 이후 로직 실행")
    )

    join_frame = create_join_frame(
        root,
        switch_to_login=lambda: switch_frame(login_frame)
    )

    def switch_frame(target_frame):
        for frame in (login_frame, join_frame):
            frame.pack_forget()
        target_frame.pack(pady=50)

    login_frame.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()
