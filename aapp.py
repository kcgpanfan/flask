import streamlit as st
import requests
import pandas as pd
import base64

# 设置网页的标题
st.title("高雄市救護即時資訊")

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

    # 定义一个函数，用于将数据框转换为 HTML 表格，并添加一些样式和脚本
    def df_to_html(df):
        # 将数据框转换为 HTML 代码
        html = df.to_html(index=False)

        # 添加一些样式和脚本
        html = """
        <html>
        <head>
        <meta charset="UTF-8" />
        <meta http-equiv="refresh" content="15">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0" />
        <style type="text/css">
                body {
                    background-image: url("data:image/png;base64,{bg}");
                    background-repeat: no-repeat;
                    background-size: cover;
                }
           

        #caseListTable td, #caseListTable th {
            font-size: 23px; 
          }


        #caseListTable {
            transform: rotate(180deg);
            -ms-transform: rotate(180deg); /* IE 9 */
            -webkit-transform: rotate(180deg); /* Safari and Chrome */
            direction: rtl;
        }

        #caseListTable td, #caseListTable th {
            transform: rotate(-180deg);
            -ms-transform: rotate(-180deg); /* IE 9 */
            -webkit-transform: rotate(-180deg); /* Safari and Chrome */
            direction: ltr;
        }


        .tablelist {
            border-collapse: collapse;
            padding-left: 2px;
            padding-right: 2px;
            padding-top: 1px;
        }
        .tablelist th {
            border-right: 1px solid #6CBF95;
            border-left: 1px solid #6CBF95;
            font-weight: bold;
            background-color: #48B28E;
            padding: 4px;
            color:#FFFFFF;
        }
        .table_tr1 {
            background-color: #F6E6C8;
        }

        .tablelist td {
            border-top: 1px solid #D9D9D9;
            border-right: 1px solid #6BC1A4;
            border-left: 1px solid #6BC1A4;
            padding: 4px;
        }

        .map_btn {
            color:#004eb9;
        }
        </style>
        </head>
        <body>

        <span style="width: 100%; height: 600px; text-align: center; display: inline-block;">

        {table}

        <script type=text/javascript>
        (function () {
          var script = document.createElement('script');
          script.src = "https://cdn.jsdelivr.net/npm/eruda";
          document.body.append(script);
          script.onload = function () {
            eruda.init();
          }
        })();
        </script>
        </body>
        </html>
        """.format(table=html, bg=bg)

        return html

    # 读取背景图片的二进制数据
    with open("bg.png", "rb") as f:
        bg = base64.b64encode(f.read()).decode()

    # 调用函数，将数据框转换为 HTML 表格
    html = df_to_html(df[columns])

    # 在网页上显示 HTML 表格
    st.markdown(html, unsafe_allow_html=True)
