import pandas as pd
import yaml, os
from sqlalchemy import create_engine

#################################################################
# @Description: API Functions
# @Author: Meihu Qin
# @UpdateDate: 2022/8/17

"""
    This function needs you to choose a company stock name and the start/end date of the data you want to look up. It returns the historical stock price data for that 
    time period.
    """
def getStockPrice(compamyabbreviation, start_date, end_date):

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

        start_date = str(start_date)
        end_date = str(end_date)
        df = pd.read_sql(f"select * from {compamyabbreviation} WHERE Date BETWEEN '{start_date}' AND '{end_date}'", dbConnection)
        data = df.to_dict()
        return data







      
      


                   

