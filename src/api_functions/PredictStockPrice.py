import pandas as pd
import numpy as np
import yaml, os
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
#################################################################
# @Description: API Functions
# @Author: Meihu Qin
# @date   8/17/2022
"""
            Predict today's closing price
            @params:
                    1. compamyabbreviation -> company ticker symbol
                
            @return:
                    1. predicted stock price for today
                    2. "model not found!" if the model has not been created
    """
def PredictStockPrice(compamyabbreviation):
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
        try:
                model_path = abs_path + f"/models/{compamyabbreviation.upper()}.h5"    
                model = load_model(model_path)

        except:
                result = {"details": "model not found!"}
                return result
        try:

                df = pd.read_sql(f"select Close from {compamyabbreviation.upper()}", dbConnection)
        except:    
                result = {"details": "table not found!"}
                return result
        # dataset = df[-60:].values
        # scaler = MinMaxScaler(feature_range=(0,1))
        # scaled_data = scaler.fit_transform(dataset)
        
        # data = scaled_data[-70: , :]
        # x_test = []

        # for i in range(60, len(data)):
        #         x_test.append(data[i-60:i, 0])
        #         print(data[i-60:i, 0])

        last_60_days = df[-60:].values
        scaler = MinMaxScaler(feature_range=(0,1))
        last_60_days_scaled = scaler.fit_transform(last_60_days)

        x_test = []

        x_test.append(last_60_days_scaled)

        # Convert the data to a numpy array
        x_test = np.array(x_test)

        # Reshape the data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

        #Get the models predicted price values 
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        predictions = predictions.reshape(len(predictions)).tolist()
        result["predicted stock price for today"] = predictions[0]

        return result