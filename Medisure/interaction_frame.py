import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from data_fetcher import fetch_pill_caution_text
from profile_frame import load_user_info
from google import generativeai as genai
import requests

GENAI_API_KEY = "AIzaSyCtYuY1Rp2TGhCtUIMDaUtr5gqEo5GJXYE"

EXCEL_PATH = "USER_DOCS.xlsx"

genai.configure(api_key=GENAI_API_KEY)
gemini_model = "gemini-2.0-flash"

def ask_to_gemini(pill_dict):
    prompt_parts = [
        "아래는 여러 약물에 대한 주의사항 정보입니다. 이 약물들을 함께 복용하는 것이 안전한지 종합적으로 판단해주세요.",
        "각 약물 간에 잠재적인 위험한 상호작용이 있는지, 특히 금기되거나 신중해야 할 조합이 있는지 알려주세요."
    ]

    for pill_name, caution_text in pill_dict.items():
        prompt_parts.append(f"\n--- 약물명 : {pill_name} ---")
        prompt_parts.append(f"\n> 주의사항 : {caution_text}")

    prompt_parts.append("이 약물들 간에 심각하거나 주의해야 할 상호작용이 있다면 심각도에 따라 '안전','주의','위험' 중 하나를 대답하고, '주의' 또는 '위험'의 경우 어떤 이유 때문인지 간략하게 설명해주세요.")

    full_prompt = "\n".join(prompt_parts)

    try:
        model = genai.GenerativeModel(gemini_model)
        response = model.generate_content(contents=full_prompt)
        print(response.text)
        return response.text.strip()

    except Exception as e:
        print("error : ", e)

def create_interaction_frame(root,user_id, on_logout, back_to_profile):
    frame = tk.Frame(root)

    # ==== Frame 선언 ====

    result_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    result_frame.pack(fill="x", padx=10, pady=10)
    result_frame.pack_propagate(False)

    details_frame = tk.Frame(frame, bg='yellow', height=300, width=400)
    details_frame.pack(fill="x", padx=10, pady=10)
    details_frame.pack_propagate(False)

    # === 약물들 상호작용 확인 ====

    def check_interaction(user_id):
        user_info = load_user_info(user_id)
        user_pills = user_info[5:]

        if not user_pills:
            print("처리할 약물 목록 없음")
        else:
            pill_dict = {}

            for pill in user_pills:
                caution_text = fetch_pill_caution_text(pill)
                if caution_text:
                    pill_dict[pill] = caution_text
                else:
                    print("상호 작용 정보를 찾을 수 없습니다.")

        return pill_dict

        # ==== 상호작용 검사 ====

    pill_dict = check_interaction(user_id)
    ask_to_gemini(pill_dict)

    tk.Button(frame, text="프로필로 돌아가기", command=back_to_profile).pack(pady=10)

    tk.Button(frame, text="로그아웃", command=on_logout).pack(pady=10)

    return frame