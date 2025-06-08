import requests
import xmltodict
import xml.etree.ElementTree as ET

API_URL = "http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService06/getDrugPrdtPrmsnDtlInq05"
SERVICE_KEY = "Dx6x0CDP8qOhtEgGvlcoAyU3AG1VHeH1v63tJvau8+AyPVrZS14+ifBJ35Oe60O28Gbj33VIbV/GGWggcOTn1Q=="

def fetch_pill_info(pill_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'item_name': pill_name
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        xml_data = response.text

        data_dict = xmltodict.parse(xml_data)

        items = (
            data_dict
            .get("response", {})
            .get("body", {})
            .get("items", {})
            .get("item", {})
        )

        # 단일 item일 경우 dict → list 변환
        if isinstance(items, dict):
            items = [items]

        # item_name 항목만 추출
        product_list = [item.get("ITEM_NAME") for item in items if "ITEM_NAME" in item]
        return product_list

    except requests.exceptions.SSLError as e:
        print("❌ SSL 오류:", e)
        return []
    except requests.exceptions.RequestException as e:
        print("❌ 요청 실패:", e)
        return []

def fetch_pill_caution_text(pill_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'item_name': pill_name
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        xml_data = response.text

        root = ET.fromstring(xml_data)
        interaction_paragraphs = []
        nb_doc_data = root.find(".//NB_DOC_DATA/DOC")

        if nb_doc_data is not None:
            for article in nb_doc_data.findall(".//ARTICLE"):
                if article.get('title') == "7. 상호작용":
                    for paragraph in article.findall(".//PARAGRAPH"):
                        text_content = paragraph.text
                        if text_content:
                            text_content = text_content.replace('<BR>', '\n')
                            interaction_paragraphs.append(text_content.strip())
                    break

        return "\n".join(interaction_paragraphs)

    except requests.exceptions.SSLError as e:
        print("❌ SSL 오류:", e)
        return []
    except requests.exceptions.RequestException as e:
        print("❌ 요청 실패:", e)
        return []