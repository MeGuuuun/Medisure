import tkinter as tk
from login_frame import create_login_frame
from join_frame import create_join_frame
from profile_frame import create_profile_frame

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

    # 나중에 프레임을 switch_frame에서 접근해야 하므로 미리 선언
    login_frame = join_frame = profile_frame = search_frame = None

    def switch_frame(target_frame):
        for frame in (login_frame, join_frame, profile_frame, search_frame):
            if frame is not None:
                frame.pack_forget()
        target_frame.pack(pady=50)

    # 프레임 생성
    profile_frame = create_profile_frame(
        root,
        on_logout=lambda: switch_frame(login_frame)
    )

    login_frame = create_login_frame(
        root,
        switch_to_join=lambda: switch_frame(join_frame),
        on_login_success=lambda: switch_frame(profile_frame)
    )

    join_frame = create_join_frame(
        root,
        switch_to_login=lambda: switch_frame(login_frame)
    )

    # 초기 화면: 로그인
    login_frame.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()
