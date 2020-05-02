from Nfunction import NomuraData
import matplotlib.pyplot as plt
import pandas as pd

Data = NomuraData()
pdatano= []
ndatano= []

for i in range(len(Data)):                  #先把資料分群（未來10天比起現金狀況正負號）
    if Data[i][2] >= 0:
        pdatano.append(Data[i][2])
    elif Data[i][2] <= 0:
        ndatano.append(Data[i][2])

pdatano = sorted(pdatano)                   #正項小到大
ndatano = sorted(ndatano,reverse = True)    #負向大到小

pd1 = (pdatano[round(len(pdatano)*.6826)-1])    #把正項當成普通常態分配的右半邊然後取1個標準差
pd2 = (pdatano[round(len(pdatano)*.9544)-1])    #把正項當成普通常態分配的右半邊然後取2個標準差
pd3 = (pdatano[round(len(pdatano)*.9974)-1])    #把正項當成普通常態分配的右半邊然後取3個標準差

nd1 = (ndatano[round(len(ndatano)*.6826)-1])    #把負項當成普通常態分配的左半邊然後取1個標準差
nd2 = (ndatano[round(len(ndatano)*.9544)-1])    #把負項當成普通常態分配的左半邊然後取2個標準差
nd3 = (ndatano[round(len(ndatano)*.9974)-1])    #把負項當成普通常態分配的左半邊然後取3個標準差

for i in range(len(Data)):
    if Data[i][2] > 0:
        if Data[i][2] <= pd1:                   #根據標準差位置來將正項分組
            Data[i].append("low")
        elif pd1 < Data[i][2] <= pd2:
            Data[i].append("bit low")
        elif pd2 < Data[i][2] <= pd3:
            Data[i].append("very low")
        elif pd3 < Data[i][2]:
            Data[i].append("extremely low")
    elif Data[i][2] < 0:                        #根據標準差位置來將正項分組
        if Data[i][2] >= nd1:
            Data[i].append("high")
        elif nd1 > Data[i][2] >= nd2:
            Data[i].append("bit high")
        elif nd2 > Data[i][2] >= nd3:
            Data[i].append("very high")
        elif nd3 > Data[i][2]:
            Data[i].append("extremely high")
    elif Data[i][2] == 0:
        Data[i].append("none")      
    
for i in range(len(Data)):                      #找出適合進場的水準
    if Data[i][2] > pd2:
        Data[i].append(1)
    elif Data[i][2] <= pd2:
        Data[i].append(0)

for i in range(len(Data)):                      #為了解決連續兩天下跌都進場狀況/兼具前後一天
    if i > 0:
        if Data[i][4]==1 and Data[i-1][4]==1:
            if Data[i][1] > Data[i-1][1]:
                Data[i][4] = 0
            elif Data[i][1] <= Data[i-1][1]:
                Data[i-1][4] = 0

for i in range(len(Data)):                      #為了解決兩天後下跌又進場狀況/兼具前後兩天
    if Data[i][4]==1:
        if Data[i][1] > Data[i-2][1]:
            Data[i][4] = 0
        elif Data[i][1] <= Data[i-2][1]:
            Data[i-2][4] = 0

for i in range(len(Data)):                      #為了解決三天後下跌又進場狀況/兼具前後三天
    if Data[i][4]==1:
        if Data[i][1] > Data[i-3][1]:
            Data[i][4] = 0
        elif Data[i][1] <= Data[i-3][1]:
            Data[i-3][4] = 0

for i in range(len(Data)):                      #為了解決四天後下跌又進場狀況/兼具前後四天
    if Data[i][4]==1:
        if Data[i][1] > Data[i-4][1]:
            Data[i][4] = 0
        elif Data[i][1] <= Data[i-4][1]:
            Data[i-4][4] = 0

for i in range(len(Data)):                      #為了解決無天後下跌又進場狀況/兼具前後五天
    if Data[i][4]==1:
        if Data[i][1] > Data[i-5][1]:
            Data[i][4] = 0
        elif Data[i][1] <= Data[i-5][1]:
            Data[i-5][4] = 0

transac = 0                                     #觀察目前可以被進場的次數（23年內有35次）
for i in range(len(Data)):
    transac += Data[i][4]
print(transac)

df = pd.DataFrame(Data,columns = ["Date","Adj Close","Δ% next 10d","Current Status","Investing State"])
df.to_csv('labeled_nomura.csv')

yyy = []
for i in range(len(Data)):
    if Data[i][4] == 1:
        yyy.append(Data[i][1])
print(yyy)                                      #觀察有哪些進場點（如果這些進場點比最後交易價格低，則有用）