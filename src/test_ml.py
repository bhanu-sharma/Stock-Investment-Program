import pandas as pd
import os
from datetime import datetime
import time

path = "C:/Users/DJB/Desktop/Course Lectures/Machine Learning with Python/intraQuarter"
lis=[]
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + "/_KeyStats"
    stock_list = [i[0] for i in os.walk(statspath)]
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time), file
                #time.sleep(15)
   
Key_Stats()
