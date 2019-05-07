import requests
import datetime
import pandas as pd
import pandas_datareader.data as web
import fix_yahoo_finance as yf

start_date = datetime.datetime(2014, 1, 1)
end_date = datetime.datetime(2018, 12, 31)
list_company = []
total = open('total_data.csv', 'w')
total.write('Company_ID, Date, Open, High, Low, Close, Adj Close, Volumn\n')

def stock_name():
    res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    
    df = pd.read_html(res.text)[0]

    # 設定column名稱
    df.columns = df.iloc[0]
    # 刪除第一行
    df = df.iloc[1:]
    # 先移除row，再移除column，超過三個NaN則移除
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    df = df.set_index('有價證券代號及名稱')
    for i in range(935):
        a=df.index[i]
        if i==649:
            b=a.split(' ',2)[0]
            list_company.append(b)
            list_company[i]+=".TW"
        else:
            b=a.split('\u3000',2)[0]
            list_company.append(b)    
            list_company[i]+=".TW"
    del list_company[0]
    

def crawl_price(stock_id):
    #執行修正函數
    yf.pdr_override()
    try:
        df_stock = web.get_data_yahoo([stock_id],start_date, end_date)
    except:
        pass
    df_stock.to_csv('stock/%s.csv'%stock_id)

# 取得公司代碼列表
stock_name()

# 將資料統一存進total_data.csv
for company in list_company:
    print('stock/%s.csv'%company)
    try:
        file = open('stock/%s.csv'%company, 'rt')
    except FileNotFoundError:
        continue
    company_name = company.replace('.TW', '')
    file.readline()
    lines = file.readlines()
    for item in lines:
        item_fix = company_name + ',' + item
        total.write(item_fix)

    file.close()

total.close()

