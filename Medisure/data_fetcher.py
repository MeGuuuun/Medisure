import requests
import xmltodict
import json

API_URL = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
SERVICE_KEY = "Dx6x0CDP8qOhtEgGvlcoAyU3AG1VHeH1v63tJvau8+AyPVrZS14+ifBJ35Oe60O28Gbj33VIbV/GGWggcOTn1Q=="

def fetch_drug_info(drug_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'itemName': drug_name
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        xml_data = response.text

        data_dict = xmltodict.parse(xml_data)

        json_data = json.dumps(data_dict, indent=2, ensure_ascii=False)

        print(json_data)

        return json_data
    except requests.exceptions.SSLError as e:
        print("❌ SSL 오류:", e)
    except requests.exceptions.RequestException as e:
        print("❌ 요청 실패:", e)