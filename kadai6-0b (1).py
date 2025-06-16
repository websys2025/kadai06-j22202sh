import requests
import pandas as pd
from pathlib import Path

APP_ID = "5eae086a5bcf914684686b0785f8cb03a3412c28" 
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0000020201",             
    "cdArea": "12101,12102,12103,12104,12105,12106", 
    "cdCat01": "A1101",                 
    "metaGetFlg": "Y",                     
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",           
    "annotationGetFlg": "Y",          
    "sectionHeaderFlg": "1",  
    "replaceSpChars": "0",
    "lang": "J"                           
}


response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status() 

data = response.json() 

values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
df = pd.DataFrame(values)


meta_info = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]


for class_obj in meta_info:
    column_name = "@" + class_obj["@id"] 


    id_to_name = {}
    if isinstance(class_obj["CLASS"], list):
        for obj in class_obj["CLASS"]:
            id_to_name[obj["@code"]] = obj["@name"]
    else:  # CLASS が1件だけの場合は dict
        c = class_obj["CLASS"]
        id_to_name[c["@code"]] = c["@name"]

   
    if column_name in df.columns:
        df[column_name] = df[column_name].replace(id_to_name)


col_replace = {"@unit": "単位", "$": "値"}
for class_obj in meta_info:
    col_replace["@" + class_obj["@id"]] = class_obj["@name"]

df.columns = [col_replace.get(c, c) for c in df.columns]


print("\n=== 取得結果 (head) ===")
print(df.head())
