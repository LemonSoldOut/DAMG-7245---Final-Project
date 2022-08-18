import pandas as pd
import yaml, os
from sqlalchemy import create_engine
from datetime import datetime
"""
    This function takes a company stock name as an input, and it returns the data from the past 30 days.
    """
def getRecent30StockPrice(compamyabbreviation):
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
    end = datetime.now()
    if end.month > 1:
            start = datetime(end.year, end.month-1, end.day)
    else:
            start = datetime(end.year-1, 12, end.day)
    df = pd.read_sql(f"select * from {compamyabbreviation}_stock WHERE Date BETWEEN '{start}' AND '{end}'", dbConnection)
    data = df.to_dict()
    return data