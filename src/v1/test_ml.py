import pandas as pd
import os
from datetime import datetime
import time

path = "C:/Users/DJB/Desktop/Course Lectures/Machine Learning with Python/intraQuarter"
lis=[]
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + "/_KeyStats"
    stock_list = [i[0] for i in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date','Unix','Ticker','DE Ratio'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    for each_dir in stock_list[1:10]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir +'/' + file
                source = open(full_file_path,"r").read()
                try:
                	value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                	df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,}, ignore_index = True)
                except Exception as e:
                    pass

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)         
   
Key_Stats()
