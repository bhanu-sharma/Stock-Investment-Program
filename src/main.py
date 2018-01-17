import numpy as np
import pandas as pd
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
from sklearn import svm, preprocessing
from sklearn.metrics import accuracy_score


FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']


def Build_Data_Set():
    data_df = pd.read_csv("Stock-Investment-Program/Documents/key_stats.csv")
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN",0).replace("N/A",0)
    

    X = np.array(data_df[FEATURES].values)#.tolist())

    y = (data_df["Status"]
         .replace("underperform",0)
         .replace("outperform",1)
         .values.tolist())

    X = preprocessing.scale(X)


    return X,y


def svm_model():

    test_size = 1000
    X, y = Build_Data_Set()
    print(len(X))

    
    clf = svm.SVC(kernel="linear", C= 1.0)
    clf.fit(X[:-test_size],y[:-test_size])
    y_ = clf.predict(X[test_size:])


    accuracy = ("Accuracy:" + accuracy_score(y[test_size:], y_))
    return accuracy

def lstm_model():

    test_size = 1000
    X, y = Build_Data_Set()

    # train test split

    train_x, train_y = X[:-test_size], y[:-test_size]
    test_x, test_y   = X[test_size:], y[test_size:]

    # reshape input to be [samples, time steps, features]

    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))

    # create and fit the LSTM network

    model = Sequential()
    model.add(LSTM(300, input_shape=(1, 35)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.fit(train_x, train_y, epochs=10, batch_size=1, verbose=2)

    # make predictions

    trainPredict = model.predict(train_x)
    testPredict = model.predict(test_x)

    # determine loss and accuracy

    score = model.evaluate(train_x, train_y, batch_size=1)

    return score
    

if __name__ == '__main__':

    loss, accuracy = lstm_model() 

    print ("Accuracy of the model:", accuracy)
