import requests
import os

# 59-上海黄金交易所 - 代码参考（根据实际业务情况修改）
# 基本参数配置
apiUrl = 'http://web.juhe.cn/finance/gold/shgold'  # 接口请求URL
apiKey = os.getenv('GOLD_API_KEY','')

# 接口请求入参配置
requestParams = {
    'key': apiKey,
    'v': '1',
}

# 发起接口网络请求
response = requests.get(apiUrl, params=requestParams)

# 解析响应结果
if response.status_code == 200:
    responseResult = response.json()
    # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
    print(responseResult)
else:
    # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
    print('请求异常')

"""
#接口返回结果示例：
{'resultcode': '200', 'reason': 'SUCCESSED!', 'result': [{'Au100g': {'variety': 'Au100g', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': 'NaN%', 'yespri': '1034.23', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'Au(T+N1)': {'variety': 'Au(T+N1)', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': 'NaN%', 'yespri': '--', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'Au(T+D)': {'variety': 'Au(T+D)', 'latestpri': '1034.79', 'openpri': '1022.07', 'maxpri': '1044.26', 'minpri': '1017.60', 'limit': '0.82%', 'yespri': '1034.79', 'totalvol': '49346.00', 'time': '2026-04-04 18:15:52'}, 'Au99.99': {'variety': 'Au99.99', 'latestpri': '1034.00', 'openpri': '1022.00', 'maxpri': '1042.00', 'minpri': '1020.00', 'limit': '0.63%', 'yespri': '1034.42', 'totalvol': '425104.00', 'time': '2026-04-04 18:15:52'}, 'Au99.95': {'variety': 'Au99.95', 'latestpri': '1025.50', 'openpri': '1119.00', 'maxpri': '1119.00', 'minpri': '1025.50', 'limit': '-3.31%', 'yespri': '1060.56', 'totalvol': '16.00', 'time': '2026-04-04 18:15:52'}, 'Au50g': {'variety': 'Au50g', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': 'NaN%', 'yespri': '--', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'Ag99.99': {'variety': 'Ag99.99', 'latestpri': '18000.00', 'openpri': '18045.00', 'maxpri': '18045.00', 'minpri': '18000.00', 'limit': '1.47%', 'yespri': '18036.00', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'Ag(T+D)': {'variety': 'Ag(T+D)', 'latestpri': '17800.00', 'openpri': '17619.00', 'maxpri': '18280.00', 'minpri': '17270.00', 'limit': '0.68%', 'yespri': '17803.00', 'totalvol': '250724.00', 'time': '2026-04-04 18:15:52'}, 'Au(T+N2)': {'variety': 'Au(T+N2)', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': '--', 'yespri': '1030.00', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'Pt99.95': {'variety': 'Pt99.95', 'latestpri': '502.26', 'openpri': '502.26', 'maxpri': '502.26', 'minpri': '502.26', 'limit': '3.49%', 'yespri': '502.26', 'totalvol': '2.00', 'time': '2026-04-04 18:15:52'}, 'AU995': {'variety': 'AU995', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': '--', 'yespri': '370.50', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'AU99.99': {'variety': 'AU99.99', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': 'NaN%', 'yespri': '--', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'MAUTD': {'variety': 'MAUTD', 'latestpri': '1036.00', 'openpri': '1021.50', 'maxpri': '1043.00', 'minpri': '1018.00', 'limit': '0.88%', 'yespri': '1034.42', 'totalvol': '32592.00', 'time': '2026-04-04 18:15:52'}, 'IAU99.99': {'variety': 'IAU99.99', 'latestpri': '1031.00', 'openpri': '1025.91', 'maxpri': '1039.00', 'minpri': '1017.86', 'limit': '1.03%', 'yespri': '1032.60', 'totalvol': '620.00', 'time': '2026-04-04 18:15:52'}, 'IAU100G': {'variety': 'IAU100G', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': '--', 'yespri': '343.55', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}, 'IAU99.5': {'variety': 'IAU99.5', 'latestpri': '--', 'openpri': '--', 'maxpri': '--', 'minpri': '--', 'limit': '--', 'yespri': '1033.00', 'totalvol': '--', 'time': '2026-04-04 18:15:52'}}], 'error_code': 0}
"""
