import pandas as pd
import numpy as np
import yaml, os
from sqlalchemy import create_engine
from datetime import datetime
import pandas_datareader as pdr
# Scale the data
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# @Description: API Functions
# @Author: Meihu Qin
# @UpdateDate: 2022/8/17

#Connect to MySQL DB
abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

yaml_path = abs_path + "\\mysql.yaml"

with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

db_host = config['credentials']['host']
db_user = config['credentials']['user']
db_password = config['credentials']['password']
db_database = config['credentials']['database']
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=db_host, db=db_database, user=db_user, pw=db_password))
dbConnection = engine.connect()

"""
    This function needs you to choose a company stock name and the start/end date of the data you want to look up. It returns the historical stock price data for that 
    time period.
    """
def SaveStockPrice(compamyabbreviation):

        # connect to DB
        abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

        yaml_path = abs_path + "\\mysql.yaml"

        with open(yaml_path, 'r') as file:
                config = yaml.safe_load(file)

        db_host = config['credentials']['host']
        db_user = config['credentials']['user']
        db_password = config['credentials']['password']
        db_database = config['credentials']['database']

        #datetime.datetime is a data type within the datetime module
        end = datetime.now()
        start = datetime(end.year - 10, end.month, end.day)
        #DataReader method name is case sensitive
        df = pdr.DataReader(compamyabbreviation, 'yahoo', start, end)
        df = df.reset_index()
        df = df.round(2)
        # Create SQLAlchemy engine to connect to MySQL Database
        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                        .format(host=db_host, db=db_database, user=db_user, pw=db_password))
        # Insert data in to MySQL using SQLAlchemy engine
        # engine.execute("INSERT INTO  `database_name`.`student` (`name` ,`class` ,`mark` ,`sex`) \VALUES ('King1',  'Five',  '45',  'male')")
        # Convert dataframe to sql table                                   
        df.to_sql(f'{compamyabbreviation}_stock', engine, if_exists='replace', index=False)
        engine.dispose()


"""
    This function needs you to choose a company stock name and the start/end date of the data you want to look up. It returns the historical stock price data for that 
    time period.
    """
def getStockPrice(compamyabbreviation, start_date, end_date):

        start_date = str(start_date)
        end_date = str(end_date)
        df = pd.read_sql(f"select * from {compamyabbreviation}_stock WHERE Date BETWEEN '{start_date}' AND '{end_date}'", dbConnection)
        data = df.to_dict()
        return data

"""
    This function takes a company stock name as an input, and it returns the data from the past 7 days.
    """
def getRecent7StockPrice(compamyabbreviation):
        end = datetime.now()
        if end.day -7 >= 1:
                start = datetime(end.year, end.month, end.day - 7)
        else:
                if end.month == 1:
                        start = datetime(end.year-1, 12, 24+end.day)
                if end.month in [3,5,7,8,10,12]:
                        start = datetime(end.year, end.month-1, 25+end.day)
                if end.month in [2,4,6,9,11]:
                        start = datetime(end.year, end.month-1, 24+end.day)
        df = pd.read_sql(f"select * from {compamyabbreviation}_stock WHERE Date BETWEEN '{start}' AND '{end}'", dbConnection)
        data = df.to_dict()
        return data

"""
    This function takes a company stock name as an input, and it returns the data from the past 30 days.
    """
def getRecent30StockPrice(compamyabbreviation):
        end = datetime.now()
        if end.month > 1:
                start = datetime(end.year, end.month-1, end.day)
        else:
                start = datetime(end.year-1, 12, end.day)
        df = pd.read_sql(f"select * from {compamyabbreviation}_stock WHERE Date BETWEEN '{start}' AND '{end}'", dbConnection)
        data = df.to_dict()
        return data


"""
    This function takes a company stock name as an input, and it returns the data from the past year.
    """
def getRecent1YStockPrice(compamyabbreviation):
        end = datetime.now()

        start = datetime(end.year-1, end.month, end.day)
        
        df = pd.read_sql(f"select * from {compamyabbreviation}_stock WHERE Date BETWEEN '{start}' AND '{end}'", dbConnection)
        data = df.to_dict()
        return data

"""
    This function takes a company stock name as an input and return its predicted stock price
    """
def PredictStockPrice(compamyabbreviation):
        
        model = load_model(f"{compamyabbreviation}_model.h5")

        df = pd.read_sql(f"select Close from {compamyabbreviation}_stock ", dbConnection)

        dataset = df.values
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)
        test_data = scaled_data[2446: , :]
        # Create the data sets x_test and y_test
        x_test = []
        
        for i in range(60, len(test_data)):
                x_test.append(test_data[i-60:i, 0])
        
        # Convert the data to a numpy array
        x_test = np.array(x_test)

        print(len(x_test))
        # Reshape the data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

        #Get the models predicted price values 
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        predictions = predictions.reshape(10).tolist()
        print(predictions)
        result = {}
        for i in range(1,11):
                result[i] = predictions[i-1]
        
        return result