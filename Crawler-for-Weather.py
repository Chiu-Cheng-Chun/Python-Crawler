# -*- coding: utf-8 -*-
"""
@author: Chiu-Cheng-Chung

*ATTENTION:
1. You can use it at will, but please mark the source if you quote it for commercial use. Thanks~
2. If you have any questions feel free to contact me: craigchiu0619@gmail.com
"""

#導入模塊
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime
import urllib

print("歡迎使用氣象站爬蟲程式!\n此程式可以將下方網站的資料抓下來存成Excel檔!\n")
print("https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp\n")
print("使用上有幾個注意事項:\n")
print("1.測站編號要查，測站名稱別打錯，台X 臺O\n2.注意日期輸入格式，以及日期範圍\n3.注意儲存路徑，預設為此程式檔案位置\n")

測站編號 = input("請輸入測站編號(eg.467080):\n")
測站名稱 = input("請輸入測站名稱(eg.宜蘭):\n")
開始日期 = input("請輸入開始日期(eg.2018-11-03):\n")
結束日期 = input("請輸入結束日期(eg.2018-11-04):\n")

title = np.array(["觀測時間","測站氣壓","海平面氣壓","氣溫","露點溫度","相對溼度","風速","風向",
                  "最大陣風","最大陣風風向","降水量","降水時數","日照時數","全天空日射量","能見度","紫外線指數","總雲量"])#定義title
儲存之名稱 = "氣象站-"+測站名稱+"-"

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

def url_name(測站名稱):
    full_name = ""
    for item in urllib.parse.quote(測站名稱).split("%")[1:]:
        full_name = full_name + "%25"+item
    return full_name

#搜尋日期範圍
date = dateRange(開始日期, 結束日期)
full_name = url_name(測站名稱)

for d in range(len(date)):
    day = date[d]#搜尋日期
    
    #搜尋URL
    index = ('http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station='+測站編號+'&stname='+full_name+'&datepicker='+day) 
    res = requests.get(index) #請求資料
    
    #資料剖析
    soup = BeautifulSoup(res.text, "lxml")
    pattern = soup.find_all("td")
    
    #創建表格
    frame = np.ones([24,17])
    
    row = 0 #計算小時用的基底
    column = 0 #決定是屬於哪個Title
    start = 8 #濾掉不要的開頭資訊

    for item in pattern:
        if start > 0:
            start = start - 1
            continue
        
        if column == 17:
            column = 0
            row = row + 1
            if row == 24:
                break
        try:
            frame[row, column] = float(item.string)
            
        except:
            frame[row, column] = np.nan
        column = column + 1
        
    new_frame = np.vstack((np.array(title, dtype='O'), np.array(frame, dtype='O')))#合併Title和表格
    
    #儲存至excel
    output = pd.DataFrame(new_frame)
    writer = pd.ExcelWriter(儲存之名稱 + day + '.xlsx')
    output.to_excel(writer, sheet_name = 'Data', index = False, header = False)
    writer.save()


