import requests
import xmltodict
import xml.etree.ElementTree as ET

API_URL = "http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService06/getDrugPrdtPrmsnDtlInq05"
SERVICE_KEY = "Dx6x0CDP8qOhtEgGvlcoAyU3AG1VHeH1v63tJvau8+AyPVrZS14+ifBJ35Oe60O28Gbj33VIbV/GGWggcOTn1Q=="

# 공통 API 요청 함수
def request_pill_api(pill_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'item_name': pill_name
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.SSLError as e:
        print(f"⚠️ SSL 오류: {e}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ 요청 실패: {e}")
    except Exception as e:
        print(f"⚠️ 알 수 없는 오류 발생: {e}")

    return None

# 약 이름을 기반으로 유사 약물명을 리스트로 반환
def fetch_pill_info(pill_name):
    xml_data = request_pill_api(pill_name)
    if not xml_data:
        return []

    try:
        data_dict = xmltodict.parse(xml_data)

        items = (
            data_dict
            .get("response", {})
            .get("body", {})
            .get("items", {})
            .get("item", {})
        )

        if isinstance(items, dict):
            items = [items]

        product_list = [item.get("ITEM_NAME") for item in items if "ITEM_NAME" in item]
        return product_list

    except Exception as e:
        print(f"⚠️ XML 파싱 실패: {e}")
        return []

# 약 이름을 기반으로 주의사항 텍스트 추출
def fetch_pill_caution_text(pill_name):
    xml_data = request_pill_api(pill_name)
    if not xml_data:
        return ""

    try:
        root = ET.fromstring(xml_data)
        interaction_paragraphs = []

        nb_doc_data = root.find(".//NB_DOC_DATA/DOC")
        if nb_doc_data is None:
            print("⚠️ NB_DOC_DATA/DOC 섹션을 찾을 수 없습니다.")
            return ""

        for article in nb_doc_data.findall(".//ARTICLE"):
            for paragraph in article.findall(".//PARAGRAPH"):
                text_content = paragraph.text
                if text_content:
                    clean_text = text_content.replace('<BR>', '\n').strip()
                    interaction_paragraphs.append(clean_text)

        return "\n".join(interaction_paragraphs) if interaction_paragraphs else "주의사항 정보가 없습니다."

    except ET.ParseError as e:
        print(f"⚠️ XML 파싱 오류: {e}")
    except Exception as e:
        print(f"⚠️ 주의사항 추출 실패: {e}")

    return ""
