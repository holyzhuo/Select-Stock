import baostock as bs
import pandas as pd
import numpy as np
import datetime

beginDate = '2019-01-01'
nowDate = datetime.datetime.now().strftime('%Y-%m-%d')

roeYearRange = range(2016, 2020)


# 获取净资产收益率(ROF)
def getROEQuery(stock, year, quarter):
    dupont_list = []
    rs_dupont = bs.query_dupont_data(stock['code'], year, quarter)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list,
                                 columns=rs_dupont.fields)
    return result_profit


def getMeanROE(stock):
    result_profit = pd.DataFrame()
    for year in roeYearRange:
        df = getROEQuery(stock, year, 4)
        if df.empty:
            continue
        else:
            if result_profit.empty:
                result_profit = df
            else:
                result_profit = result_profit.append(df)

    result_profit['dupontROE'] = result_profit['dupontROE'].astype(float)
    return result_profit['dupontROE'].mean()


def getHistoryKDataQuery(stock):
    rs = bs.query_history_k_data_plus(stock['code'],
                                      "date,code,close,peTTM,pbMRQ,psTTM",
                                      start_date=beginDate, end_date=nowDate,
                                      frequency="d", adjustflag="3")
    # print('query_history_k_data_plus respond error_code:' + rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    result_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())
    return pd.DataFrame(result_list, columns=rs.fields)[['peTTM', 'pbMRQ']]


def getHistoryKData(stock):
    df = getHistoryKDataQuery(stock)

    astype_cols = ['peTTM', 'pbMRQ']
    df[astype_cols] = df[astype_cols].astype(float)
    return df.mean()


# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

stocks = pd.read_csv('./base_stocks.csv', encoding="utf8")

# stocks = stocks.head(50)

# 对股票添加roe列
stocks['roe'] = stocks.apply(getMeanROE, axis=1)

# 增加 滚动市盈率 peTTM
#  市净率 pbMRQ
stocks[['peTTM', 'pbMRQ']] = stocks.apply(getHistoryKData, axis=1, result_type="expand")  # 按行

# 筛选基本面
# roe 在 [0.15, 0.25]
stocks = stocks[(stocks.roe > 0.15) & (stocks.roe < 0.25)]

# 滚动市盈率 peTTM < 45
stocks = stocks[stocks.peTTM < 45]

#  市净率 pbMRQ
stocks = stocks[stocks.pbMRQ < 10]

# 数值归一化处理
max_min_scaler = lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
stocks[['roe', 'peTTM', 'pbMRQ']] = stocks[['roe', 'peTTM', 'pbMRQ']].apply(max_min_scaler)  # 按列

# 计算分数
stocks["score"] = stocks[['roe', 'peTTM', 'pbMRQ']].apply(lambda x: x["roe"] - x["peTTM"] - x["pbMRQ"], axis=1)

stocks = stocks.sort_values(by=['score'], ascending=False)

stocks.to_csv("./filter_stocks.csv", encoding="utf_8_sig", index=False)

bs.logout()
