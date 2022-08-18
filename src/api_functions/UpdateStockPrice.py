import pandas as pd
import yaml, os
from sqlalchemy import create_engine
from datetime import datetime,timedelta
def UpdateStockPrice():
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
    dbConnection = engine.connect()
    #DataReader method name is case sensitive
    stockname = pd.read_sql(f"select distinct stockAbbrName from stock_follow_table", dbConnection)
    compamyabbreviations = stockname['stockAbbrName'].values.tolist()
    for name in compamyabbreviations:
            dbConnection = engine.connect()
            #Get yesterday stock data
            last_record_date = pd.read_sql(f"select Date from {name} ORDER BY Date DESC LIMIT 1", dbConnection)
            last_record_date = last_record_date['Date'].to_string(index = False)
            print(last_record_date)
            if last_record_date == yesterday_format:
                    result[name] = f"Record for {yesterday_format} is already exist!"

            else:
                    yesterdaydata = pdr.DataReader(name, 'yahoo', f"'{yesterday_format}'", f"'{yesterday_format}'")
                    yesterdaydata = yesterdaydata.reset_index()
                    yesterdaydata = yesterdaydata.round(2)
                    #Save one row data into stock table                                     
                    yesterdaydata.to_sql(f'{name}', engine, if_exists='append', index=False)
                    result[name] = f"Record for {yesterday_format} has beed added!"
                    
    return result