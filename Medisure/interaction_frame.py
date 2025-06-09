import tkinter as tk
from data_fetcher import fetch_pill_caution_text
from profile_frame import load_user_info
from google import generativeai as genai
from PIL import Image, ImageTk

GENAI_API_KEY = "AIzaSyCtYuY1Rp2TGhCtUIMDaUtr5gqEo5GJXYE"
IMAGE_PATH = "Medisure_logo.png"
EXCEL_PATH = "USER_DOCS.xlsx"

# Gemini API
genai.configure(api_key=GENAI_API_KEY)
gemini_model = "gemini-2.0-flash"

# gemini 요청 및 응답 처리
def ask_to_gemini(pill_dict):
    if not pill_dict:
        return "⚠️ 분석할 약물 정보가 없습니다."

    prompt_parts = [
        "아래는 여러 약물에 대한 주의사항 정보입니다. 이 약물들을 함께 복용하는 것이 안전한지 종합적으로 판단해주세요.",
        "각 약물 간에 잠재적인 위험한 상호작용이 있는지, 특히 금기되거나 신중해야 할 조합이 있는지 알려주세요."
    ]

    for pill_name, caution_text in pill_dict.items():
        prompt_parts.append(f"\n--- 약물명 : {pill_name} ---")
        prompt_parts.append(f"\n> 주의사항 : {caution_text}")

    prompt_parts.append("이 약물들 간에 심각하거나 주의해야 할 상호작용이 있다면 심각도에 따라 '안전','주의','위험' 중 하나를 대답하고, '주의' 또는 '위험'의 경우 어떤 이유 때문인지 간략하게 설명해주세요.")
    prompt_parts.append("\n 약물 상호 작용에 관한 자세한 내용을 5줄 이내로 짧고 명확하게 요약한 내용만 대답하세요.")
    prompt_parts.append("\n 만약 입력받은 정보의 약물이 단 한 가지라면 '안전'을 대답하고 복용 시 주의사항만 3줄 이내로 간단하게 대답하세요.")

    full_prompt = "\n".join(prompt_parts)

    try:
        model = genai.GenerativeModel(gemini_model)
        response = model.generate_content(contents=full_prompt)
        return response.text.strip() if response.text else "Gemini 응답이 비어 있습니다."
    except Exception as e:
        print("❌ Gemini API 오류:", e)
        return "⚠️ Gemini 분석 중 오류가 발생했습니다. 다시 시도해주세요."

# 상호작용 frame
def create_interaction_frame(root,user_id, on_logout, back_to_profile):
    frame = tk.Frame(root)

    # ==== Frame 선언 ====
    logo_frame = tk.Frame(frame, height=150, width=150)
    logo_frame.pack(fill="x", pady=(30, 10))
    logo_frame.pack_propagate(False)

    logo_img_raw = Image.open(IMAGE_PATH)
    logo_img_resized = logo_img_raw.resize((150, 150), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img_resized)

    logo_label = tk.Label(logo_frame, image=logo_img)
    logo_label.image = logo_img
    logo_label.pack()

    tk.Label(frame, text="약물 상호작용 분석 결과", font=("Arial", 16)).pack(pady=10)

    # === 약물들 상호작용 확인 ====

    def check_interaction(user_id):
        try:
            user_info = load_user_info(user_id)
            user_pills = user_info[5:]
            if not user_pills:
                return {}, "등록된 약물이 없습니다."
        except Exception as e:
            print(f"⚠️ 사용자 정보 로드 실패: {e}")
            return {}, "사용자 정보를 불러오는 데 실패했습니다."

        pill_dict = {}
        for pill in user_pills:
            try:
                caution_text = fetch_pill_caution_text(pill)
                if caution_text:
                    pill_dict[pill] = caution_text
                else:
                    pill_dict[pill] = "주의사항 정보를 찾을 수 없습니다."
            except Exception as e:
                print(f"⚠️ 약물 주의사항 로드 실패 ({pill}): {e}")
                pill_dict[pill] = "주의사항 불러오기 오류"

        return pill_dict, None

    # ==== 상호작용 검사 ====

    pill_dict, error_message = check_interaction(user_id)
    result_text = error_message if error_message else ask_to_gemini(pill_dict)

    text_widget = tk.Text(frame, wrap="word", height=15, width=70, font=("Arial", 14))
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    text_widget.insert(tk.END, result_text)
    text_widget.config(state=tk.DISABLED)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)

    btn_profile = tk.Button(btn_frame, text="프로필로 돌아가기", font=("Arial", 12), width=18, command=back_to_profile)
    btn_profile.pack(side="left", padx=10)

    btn_logout = tk.Button(btn_frame, text="로그아웃", font=("Arial", 12), width=10, command=on_logout)
    btn_logout.pack(side="left", padx=10)

    return frame