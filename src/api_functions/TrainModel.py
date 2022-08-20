import pandas as pd
import numpy as np
import yaml, os
from sqlalchemy import create_engine
from datetime import datetime,timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

#################################################################
# @Description: API Functions
# @Author: Meihu Qin
# @date   8/17/2022
"""
            Train model for each followed company
            @params:
                
            @return: company name + date +model generated!
                    
    """
def TrainModel():
    #Connect to MySQL DB
    abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    yaml_path = abs_path + "/mysql.yaml"

    with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)

    db_host = config['credentials']['host']
    db_user = config['credentials']['user']
    db_password = config['credentials']['password']
    db_database = config['credentials']['database']
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                    .format(host=db_host, db=db_database, user=db_user, pw=db_password))
    dbConnection = engine.connect()
    result = {}
    #datetime.datetime is a data type within the datetime module
    yesterday = datetime.today()+timedelta(-1)
    yesterday_format = yesterday.strftime('%Y-%m-%d')
    #DataReader method name is case sensitive
    stockname = pd.read_sql(f"select distinct stockAbbrName from stock_follow_table", dbConnection)
    compamyabbreviations = stockname['stockAbbrName'].values.tolist()
    for name in compamyabbreviations:
        df = pd.read_sql(f"select * from {name.upper()}", dbConnection)
        # Create a new dataframe with only the 'Close column 
        data = df.filter(['Close'])

        # Convert the dataframe to a numpy array
        dataset = data.values

        # Get the number of rows to train the model on
        training_data_len = len(dataset)

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
        model_path = abs_path + f"/models/{name}.h5"
        model.save(model_path)
        result[name] = f"{yesterday_format} model generated!"
    return result
        