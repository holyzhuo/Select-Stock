import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取中证500成分股
rs = bs.query_zz500_stocks()
print('query_zz500 error_code:'+rs.error_code)
print('query_zz500  error_msg:'+rs.error_msg)

all_stocks = []
while (rs.error_code == '0') & rs.next():
    all_stocks.append(rs.get_row_data())

# 获取沪深300
rs = bs.query_hs300_stocks()
print('query_hs300 error_code:'+rs.error_code)
print('query_hs300  error_msg:'+rs.error_msg)

while (rs.error_code == '0') & rs.next():
    all_stocks.append(rs.get_row_data())


result = pd.DataFrame(all_stocks, columns=rs.fields)

# 去除创业板
result = result[result['code'].str.contains("300") == False]

# 结果集输出到csv文件
result.to_csv("./base_stocks.csv", encoding="utf_8_sig", index=False)
print(result)

# 登出系统
bs.logout()