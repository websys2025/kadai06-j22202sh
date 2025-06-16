import requests
import pprint


APP_ID = "5eae086a5bcf914684686b0785f8cb03a3412c28"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0003142313",      # 文部科学省 学校基本調査（高等学校）
    "cdTime": "20230000",             # 2023年度
    "cdCat01": "0",                   # 性別：総数（"1":男、"2":女）
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"  # 日本語
}
# APIへリクエスト
response = requests.get(API_URL, params=params)
response.raise_for_status()
data = response.json()
#表示
values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
print(f"取得件数: {len(values)} 件\n")
for i, v in enumerate(values[:5], start=1):
    pprint.pprint({
        "No": i,
        "value": v["@value"],
        "area": v.get("@area"),
        "class": v.get("@cat02", "N/A")
    })
