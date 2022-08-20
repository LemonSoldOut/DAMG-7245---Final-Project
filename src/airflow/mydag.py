from urllib import response
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import requests, pymysql, yaml, os


doc_md = """
### DAG
#### Purpose
"""


abs_path = os.path.dirname((os.path.abspath(__file__)))

yaml_path = abs_path + "/mysql.yaml"

with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

db_host = config['credentials']['host']
db_user = config['credentials']['user']
db_password = config['credentials']['password']
db_database = config['credentials']['database']
con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
c = con.cursor()

# usernamesql = "select username from user_table WHERE userid = 6"
# c.execute(usernamesql + ";")
# username = c.fetchall()[0][0]

# passwordsql = "select hassedpassword from user_table WHERE userid = 6"
# c.execute(usernamesql + ";")
# password = c.fetchall()[0][0]


# url1 = 'http://127.0.0.1:8000/api/get/update_stock_price/'
# url2 = 'http://127.0.0.1:8000/api/train/models/'
# def getToken():
#     headers = {'accept': 'application/json','Content-Type': 'application/x-www-form-urlencoded',}
#     url = 'http://127.0.0.1:8000/token'
#     data = {'grant_type':'','username': f"{username}","password": f"{password}",'scope':'','client_id':'','client_secret':''}
#     res = requests.post(url=url,params=data,headers=headers)
#     token = res.json()["access_token"]
#     return token

def updatestockprice():
    response = requests.get("http://127.0.0.1:8000/api/get/update_stock_price/").json()
    count = response["Companies that has been updated"]
    return count

def trainmodel(**kwargs):
    ti = kwargs['ti']
    count = ti.xcom_pull(task_ids='stock_price')
    
    if count > 0:
        nowTime = datetime.now()
        c.execute('INSERT INTO daily_update(username,updateTime,isAuto,total_company) VALUES(%s,%s,%s,%s)',('airflow',nowTime,'1',count))
        con.commit()
        requests.get('http://127.0.0.1:8000/api/train/models/')
    


with DAG("my_dag",start_date=datetime(2022, 1, 1),schedule_interval="@daily",catchup=False,) as dag:


    update_stock_price = PythonOperator(task_id='stock_price', python_callable=updatestockprice)
    update_model = PythonOperator(task_id='model', python_callable=trainmodel)
    
    
    
    # getToken >> 
    update_stock_price >> update_model

