import pandas as pd
import numpy as np
import yaml, os
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

"""
    This function takes a company stock name as an input and return its predicted stock price
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
    model_path = abs_path + f"/models/{compamyabbreviation}.h5"    
    model = load_model(model_path)

    df = pd.read_sql(f"select Close from {compamyabbreviation}", dbConnection)

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