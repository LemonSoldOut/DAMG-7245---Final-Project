import yaml, os
from datetime import datetime
import pymysql
from api_functions import SaveStockPrice
# @author Cheng Wang
# @date   8/17/2022
def userFollowCompanyStatusCheck(username,co_abbr):
    """
            Check if the user whether could follow the given Company stock
            @params:
                    1. username -> user who sign in to FastAPI (we will check it from local MySQL database)
                    2. co_abbr -> company abbrivation name
            @return:
                    1. already followed
                    2. we will create one row of data into stock_follow_table
                            2.1 download target company abbrivation name stock history(max 10 years)
                    3. something wrong (we need check...)
    """
    abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    yaml_path = abs_path + "/mysql.yaml"

    with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)

    db_host = config['credentials']['host']
    db_user = config['credentials']['user']
    db_password = config['credentials']['password']
    db_database = config['credentials']['database']
    con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
    c = con.cursor()
    sql = "select userId from user_table WHERE username = '"
    c.execute(sql + username + "';")
    userId = c.fetchall()[0][0]
    #print(result)
    
    checkUserFollowStatus = "select count(1) from stock_follow_table where userId = '" + str(userId) + "' and stockAbbrName = '" + str(co_abbr.upper()) + "';"
    c.execute(checkUserFollowStatus)
    result = c.fetchall()[0][0]
    res_dict = {}
    if(result == 1):
            res_dict[username] = "You already followed!"
            checkTableSQL = "show tables like '"+ co_abbr.upper() +"';"
            #c.execute(checkTableSQL)
            #test = c.fetchall()[0][0]
            #print("========================================\n",test)
            
            
    elif(result == 0):
            #res_dict[username] = "You need follow it! Check DB if exists!"
            nowTime = datetime.now()
            c.execute('INSERT INTO stock_follow_table(userId,createDate,updateDate,disabled,stockAbbrName) VALUES(%s,%s,%s,%s,%s)',(userId,nowTime,nowTime,0,co_abbr.upper()))
            con.commit()
            # c.execute(checkUserFollowStatus)
            # status = c.fetchall()[0][0]
            # To download target Company Max (10 years) history 
            
            checkTableSQL = "show tables like '"+ co_abbr.upper() +"';"
            c.execute(checkTableSQL)
            getResultFromSQL = c.fetchall()
            if getResultFromSQL == ():
                    SaveStockPrice(co_abbr)
                    res_dict[username] = co_abbr.upper() + " Table created! Saving success!"
            else:
                    table_name = getResultFromSQL[0][0]
                    
                    if(table_name.upper() != co_abbr.upper()):
                            SaveStockPrice(co_abbr)
                            res_dict[username] = co_abbr.upper() + " Table created! Saving success!"
                    else:
                            res_dict[username] = co_abbr.upper() + " Table already exists!"
                    
    else:
        res_dict[username] = "Something went wrong!" 
    return res_dict