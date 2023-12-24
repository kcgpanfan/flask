import streamlit as st
import requests
import pandas as pd

# 设置网页的标题
st.title("台中市救護車即時資訊")

# 获取 JSON 数据的网址和请求头
url = "https://gis.fdkc.gov.tw/rescue/getnowcase/json?getalls=1"
headers = {
    'Referer': 'https://gis.fdkc.gov.tw/rescue/'
}

# 发送请求并获取响应
response = requests.get(url, headers=headers)

# 判断响应状态是否正常
if response.status_code != 200:
    st.error('請求資料失敗')
else:
    # 解析 JSON 数据为 Python 字典
    json_data = response.json()

    # 将字典转换为 pandas 数据框
    df = pd.DataFrame(json_data)

    # 选择要显示的列
    columns = ["dept", "in_time", "nt_tel", "dis_code", "cs_place", "nt_name", "memo"]

    # 在网页上显示数据框
    st.dataframe(df[columns])
