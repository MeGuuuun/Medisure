import requests
import xmltodict
import xml.etree.ElementTree as ET
import json

API_URL = "http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService06/getDrugPrdtMcpnDtlInq06"
# API_URL = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
SERVICE_KEY = "Dx6x0CDP8qOhtEgGvlcoAyU3AG1VHeH1v63tJvau8+AyPVrZS14+ifBJ35Oe60O28Gbj33VIbV/GGWggcOTn1Q=="

def fetch_pill_info(drug_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'Prduct': drug_name
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
            .get("item", [])
        )

        # 단일 item일 경우 dict → list 변환
        if isinstance(items, dict):
            items = [items]

        # PRDUCT 항목만 추출
        product_list = [item.get("PRDUCT") for item in items if "PRDUCT" in item]
        return product_list

    except requests.exceptions.SSLError as e:
        print("❌ SSL 오류:", e)
        return []
    except requests.exceptions.RequestException as e:
        print("❌ 요청 실패:", e)
        return []