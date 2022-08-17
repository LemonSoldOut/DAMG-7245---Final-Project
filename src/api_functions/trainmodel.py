#import external pandas_datareader library with alias of web
from ast import main
from unicodedata import name
import pandas_datareader as pdr
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pickle
#import datetime internal datetime module
#datetime is a Python module
from datetime import datetime

def train_model(compamyabbreviation):
    #datetime.datetime is a data type within the datetime module
    end = datetime.now()
    start = datetime(end.year - 10, end.month, end.day)

    
    #DataReader method name is case sensitive
    df = pdr.DataReader(compamyabbreviation, 'yahoo', start, end)
    df.to_csv(f'{compamyabbreviation}.csv')
    #invoke to_csv for df dataframe object from 
    #DataReader method in the pandas_datareader library

    # Create a new dataframe with only the 'Close column 
    data = df.filter(['Close'])
    # Convert the dataframe to a numpy array
    dataset = data.values
    # Get the number of rows to train the model on
    training_data_len = int(np.ceil( len(dataset) * .95 ))

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # Create the training data set 
    # Create the scaled training data set
    train_data = scaled_data[0:int(training_data_len), :]

    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 61:
            print(x_train)
            print(y_train)
            print()
            
    # Convert the x_train and y_train to numpy arrays 
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))


    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    pickle.dump(model, open(f'{compamyabbreviation}_model.pkl', 'wb'))
    

if __name__ == "__main__":
    train_model("goog")