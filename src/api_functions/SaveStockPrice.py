import yaml, os
from sqlalchemy import create_engine
from datetime import datetime
import pandas_datareader as pdr

#################################################################
# @Description: API Functions
# @Author: Meihu Qin
# @UpdateDate: 2022/8/17


"""
    This function needs you to choose a company stock name and the start/end date of the data you want to look up. It returns the historical stock price data for that 
    time period.
    """
def SaveStockPrice(compamyabbreviation):
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
    #datetime.datetime is a data type within the datetime module
    end = datetime.now()
    start = datetime(end.year - 10, end.month, end.day)
    #DataReader method name is case sensitive
    try:
        df = pdr.DataReader(compamyabbreviation, 'yahoo', start, end)
        df = df.reset_index()
        df = df.round(2)
        # Insert data in to MySQL using SQLAlchemy engine
        # engine.execute("INSERT INTO  `database_name`.`student` (`name` ,`class` ,`mark` ,`sex`) \VALUES ('King1',  'Five',  '45',  'male')")
        # Convert dataframe to sql table                                   
        df.to_sql(f'{compamyabbreviation.upper()}', engine, if_exists='replace', index=False)

        res = compamyabbreviation.upper() + " Table created! Saving success!"
        return {"details":res}
    except:
        res = compamyabbreviation.upper() + " is not a valid company stock name!"
        return {"details":res}

    