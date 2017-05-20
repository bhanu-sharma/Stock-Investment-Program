import pandas as pd
import os
from datetime import datetime
import time
from time import mktime
import matplotlib
import matplotlib.pyplot as plt 
from matplotlib import style
import pylab

style.use("dark_background")

path = "C:/Users/DJB/Desktop/Course Lectures/Machine Learning with Python/intraQuarter"
lis=[]
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    
    #statespath = "C:/Users/DJB/Desktop/Course Lectures/Machine Learning with Python/intraQuarter/_KeyStats"
    
    statspath = path + "/_KeyStats"
    #print "statspath", statspath
    #stock_list : Lists only the directories under the _KeyStats, now given in a list. i.e [a, aa, aapl, abbv ...] 
    stock_list = [i[0] for i in os.walk(statspath)]
    #print "stock_list", statspath
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    for each_dir in stock_list[1:5]:
        #each_dir = statspath + "<-name of the company->". for eg. C:/Users/DJB/Desktop/Course Lectures/Machine Learning with Python/intraQuarter/_KeyStats\a
        #print "each_dir", each_dir
        each_file = os.listdir(each_dir)
        #each_file : All the files contained in the respective directory of the company being iterated
        #print "each_file", each_file
        #ticker holds the name of the company being iterated
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        #print "ticker", ticker
        if len(each_file) > 0:
            for file in each_file:
                #file eg. 20040130190102.html, 20040413040711.html
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir +'/' + file
                source = open(full_file_path,"r").read()
                try:
                    ''' value : It is the value of Debt/Equity ratio, parsed from the document
                        df : DataFrame, In which the Debt/Equity ratio, unix_time, ticker and values are structured 
                    '''
                    value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    '''
                    sp500_date : the date of which the current company's stock data is. eg. 2004-01-30
                    sp500 value : the value at which the stock market closed ("Adjusted Close") on the sp500_date
                    stock_price : price of the stock on the sp500_date

                    We will be entering the price of the stock, it's DE ratio and the value at which the market closed 
                    that day, if the stock of the company performed better than the market, we'll
                    label the stock as performing good for that day, (i.e if the %change in the stock price at the end of the
                    day is higher than the %change in market's value, then it performed better.) if it performed worse or below the market close value, we'll label it 
                    underperforms.
                    '''
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                        #print sp500_date, sp500_value
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                        #print sp500_date, sp500_value

                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    #print stock_price

                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value


                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100


                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference': stock_p_change - sp500_p_change}, ignore_index = True)
                    
                except Exception as e:
                    pass

    for each_ticker in ticker_list:

        try:

            plot_df = df[(df["Ticker"] == each_ticker)]
            #print plot_df
            plot_df = plot_df.set_index(["Date"])

            plot_df["Difference"].plot(label=each_file)
            plt.legend()
        except:
            pass

        
    plt.show() 


    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)         
   
Key_Stats()
