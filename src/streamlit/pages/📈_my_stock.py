import streamlit as st
import numpy as np
import yaml
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
import pymysql
import os
import pandas as pd
import requests
import time


#st.session_state


#########################################################            
with open('./streamlit_config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


#Connect to MySQL DB
abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

yaml_path = abs_path + "/mysql.yaml"

with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

db_host = config['credentials']['host']
db_user = config['credentials']['user']
db_password = config['credentials']['password']
db_database = config['credentials']['database']

###########################################################
# get response from FastAPI
def getFastAPIResponse(url,data): #data_bin
    #rlt = requests.post('http://127.0.0.1:8000/api/get/fileNameAndClass/', json=data_bin).json()
    
    token_str = 'bearer ' + st.session_state["token"]
    headers = {'accept': 'application/json','authorization': str(token_str)}
    response = requests.get(url=url,params=data,headers=headers,verify=False)

    return response
###########################################################



with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
        
        isCustom = st.checkbox('custom day')
        
        con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
        c = con.cursor()
        getUserIdSQL = "SELECT userId FROM user_table WHERE username = '" + st.session_state["username"] + "';"
        c.execute(getUserIdSQL)
        userId = c.fetchall()[0][0]
        #st.write("userId = " + str(userId)) #cheng 2    
        
        sql = "SELECT stockAbbrName FROM stock_follow_table WHERE userId ='" + str(userId) +"';"
        c.execute(sql)
        result = c.fetchall()
        follow_list = []
        
        # To get user's follow list
        for i in result:
            follow_list.append(i[0])
        #st.text(follow_list)
        
        
        co_selection = st.selectbox('Which company would you like to select?',follow_list,key="co_selection")
        
        if(isCustom):
            yesterday = datetime.today()+timedelta(-1)
            
            startDate = st.date_input("Start date",yesterday,key="startDate")
            endDate = st.date_input("End date",yesterday,key="endDate")
            
        else:
            selection = st.selectbox('How would you like to select stock history?',('1 day', '1 week','1 month', '1 year', '5 years', '10 years'))
        
        options = st.multiselect(
                    'What values you want to select?',
                    ['Open', 'Close', 'High', 'Low',"Adj Close","Volume"],
                    ['Open','Close'])
        
        
        click_col,n1,pred_col = st.columns(3)
        with click_col:
            #st.write("col1")
            
            isClick = st.button("OK")
        with pred_col:
            isPredicted = st.button("Predict")
        
    
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    time_interval= 0
    tab1, tab2= st.tabs(["Stock","Predict"])
    if(isClick == True):
       

        if not isCustom:
            yesterday = datetime.today()+timedelta(-1)
       
            if(selection == "1 day"):
                time_interval = 1
                startDate = yesterday
                endDate = yesterday
            elif(selection == "1 week"):
                time_interval = 7
                startDate = datetime.today()+timedelta(-time_interval)
                endDate = yesterday
            elif(selection == "1 month"):
                time_interval = 30
                startDate = datetime.today()+timedelta(-time_interval)
                endDate = yesterday
            elif(selection == "1 year"):
                time_interval = 365
                startDate = datetime.today()+timedelta(-time_interval)
                endDate = yesterday
            else:
                st.error("Seomthign went wrong! Please contact us ASAP!")
        
        # st.write(startDate)
        # st.write(endDate)
            
            
            
        today = datetime.today()
        today = today.strftime('%Y-%m-%d')
        startDate = startDate.strftime('%Y-%m-%d')
        endDate = endDate.strftime('%Y-%m-%d')
        if(startDate >= today):
            st.warning("Do not choose a start date which is later than yesterday!")
        elif(endDate >= today):
            st.warning("Do not choose a end date which is later than yesterday!")
        elif(startDate > endDate):
            st.warning("Start date is later than end date!")
        else:
            with tab1:
                url = 'http://127.0.0.1:8000/api/get/stockprice_search_by_date/'
                data = {"compamyabbreviation": co_selection,"startdate":startDate, "enddate":endDate}
                
                response = getFastAPIResponse(url,data)
                
                res_dict = {}        
                if(response.content[0] == 123): # json style
                    res_j = response.json()
                    if "detail" in res_j.keys():
                        if res_j["detail"] == "Could not validate credentials":
                            st.warning("You should login again!")
                            st.session_state.authentication_status = None
                            time.sleep(2)
                            st.experimental_rerun()
                        elif res_j["detail"] == "Item not found":
                            st.error("There is no target stock company!")
                        else:
                            st.error("New error which is not handled. Please contact us ASAP!")
                    else:
                        st.sidebar.success("You did it! :heart:")
                        valied_days = len(list(res_j["Date"].values()))
                        st.sidebar.info("Total valied days between " + str(startDate) + " and " + str(endDate) + " : " + str(valied_days) + " days")
                        # Here is returned json format response!
                        #st.json(res_j)

                                
                elif(response.content[0] == 255): # image style
                        st.error("Return response is in image format! Something went wrong! Please contact us for help!")
                                
                else:
                        st.error("Seomthing went wrong! Please contact us ASAP!")
                
                
                
                if res_j["Date"] != {}:
                    # if we can find a way to get company full name from company abbreviation name or reverse -> That will be helpful
                    # Todo    
                    co_fullname = "Google Inc."
                    input_df = pd.DataFrame([co_selection,co_fullname,startDate,endDate],columns=["Your input"],index=["Company abbr name","official name","start date","end date"])
                                
                    
                    
                    st.subheader(co_selection)
                    #st.text(options)
                    st.table(input_df)
                        
        
                    #st.image("./pages/pic1.png")
                    date_li1 = list(res_j["Date"].values())
                    #st.text(date_li1)
                    date_list = []
                    for i in date_li1:
                        date_list.append(i.split("T")[0])
                        
                    #st.text(date_list)
                    options.append("Date")
                    date_li1 = list(res_j["Date"].values())
                    df_history = pd.DataFrame(res_j,columns=options)
                        
                    #df_history["Date"] = df_history["Date"].replace("T00:00:00","")
                    df_history["Date"] = df_history["Date"].replace(to_replace=r'T00:00:00', value='', regex=True)
                    #df_history = df_history.drop(['Date'], axis=1)
                    #df_history = df_history.assign(Date=date_list)
                        
                    # st.write(options)
                        
                    # Warning: Cannot round values to 2-decimals because of Streamlit?
                    for i in options:
                        if(i !="Volume" and i !="Date"):
                            df_history[i] = round(df_history[i],2)
                        
                    with st.expander("See results",True):
                        st.table(df_history.head(30))
                        
                        
                    if(startDate == endDate):
                        time_interval = 1
                        
                        
                        
                    if("Volume" in options):
                        options.remove("Volume")
                        df_show = pd.DataFrame(df_history, columns=options)
                        df_show = df_show.rename(columns={'Date':'index'}).set_index('index')                       
                            
                                    
                        df_volume = pd.DataFrame(df_history, columns=['Date','Volume'])
                        df_volume = df_volume.rename(columns={'Date':'index'}).set_index('index')   
                            
                        # analyze_list = ["mean","median","max","min","std dev"]
                        # volume_list = []
                        # volume_list.append(round(df_history["Volume"].mean(),2))
                        # volume_list.append(round(df_history["Volume"].std(),2))
                        # volume_list.append(round(df_history["Volume"].max(),2))
                        # volume_list.append(round(df_history["Volume"].min(),2))
                        # volume_list.append(round(df_history["Volume"].median(),2))
                            
                        #volume_list.append
                        # np_analysis = np.array(volume_list).reshape(1,-1)
                        # df_analysis = pd.DataFrame(np_analysis, columns=analyze_list)
                        
                        # st.table(df_analysis)
                            
    
                        if(time_interval != 1):
                            st.line_chart(df_show)
                            st.line_chart(df_volume)
                                
                        else:
                            # need show 1day open - close and % of open
                            open_value = list(res_j["Open"].values())[0]
                            close_value = list(res_j["Close"].values())[0]
                            #st.write(open_value)
                            #st.write(close_value)
                            value = close_value - open_value
                            delta = round((value / open_value * 100),2)
                            if(delta >= 0):
                                delta = "+ "+ str(delta) + "%"
                            else:
                                delta = "- "+ str(delta) + "%"
                            open_value = "$" + str(open_value)
                                
                            adj_colse_value = list(res_j["Adj Close"].values())[0]
                            #st.write(adj_colse_value)
                            adj_c_to_c_value = adj_colse_value - close_value
                            delta1 = round((adj_c_to_c_value / close_value * 100),2)
                                
                            if(delta1 >= 0):
                                delta1 = "+ "+ str(delta1) + "%"
                            else:
                                delta1 = "- "+ str(delta1) + "%"
                            close_value = "$" + str(close_value)
                                
                                
                            col1,col2 = st.columns(2)
                            with col1:
                                #st.write("col1")
                                st.metric(label="Yesterday Apple Inc. Stock Open to Close", value=open_value, delta=delta,delta_color="inverse")
                                    
                            # with col2:
                            #     st.metric(label="Yesterday Apple Inc. Stock Close to Adj Close", value=close_value, delta=delta1,delta_color="inverse")
                    else:
                        df_show = pd.DataFrame(df_history, columns=options)
                        df_show = df_show.rename(columns={'Date':'index'}).set_index('index')                       

                            
                        if(time_interval != 1):
                            st.line_chart(df_show)
                        else:
                            open_value = list(res_j["Open"].values())[0]
                            close_value = list(res_j["Close"].values())[0]
                            #st.write(open_value)
                            #st.write(close_value)
                            value = close_value - open_value
                            delta = round((value / open_value * 100),2)
                            if(delta >= 0):
                                delta = "+ "+ str(delta) + "%"
                            else:
                                delta = "- "+ str(delta) + "%"
                            open_value = "$" + str(open_value)
                                
                            adj_colse_value = list(res_j["Adj Close"].values())[0]
                            #st.write(adj_colse_value)
                            adj_c_to_c_value = adj_colse_value - close_value
                            delta1 = round((adj_c_to_c_value / close_value * 100),2)
                                
                            if(delta1 >= 0):
                                delta1 = "+ "+ str(delta1) + "%"
                            else:
                                delta1 = "- "+ str(delta1) + "%"
                            close_value = "$" + str(close_value)
                                
                                
                            col1,col2 = st.columns(2)
                            with col1:
                                #st.write("col1")
                                st.metric(label="Yesterday Apple Inc. Stock Open to Close", value=open_value, delta=delta,delta_color="inverse")
                                    
                            # with col2:
                            #     st.metric(label="Yesterday Apple Inc. Stock Close to Adj Close", value=close_value, delta=delta1,delta_color="inverse")    
                
                else:
                    st.warning("There is no data between  " + str(startDate) + "  and  " + str(endDate) + "!")
            
    if isPredicted:
        with tab2:
            if(isPredicted):
                #st.subheader("Predict the target company stock trend for the next 10 days")
                url = 'http://127.0.0.1:8000/api/get/predicted_stock_price/'
                data = {"compamyabbreviation": co_selection}
                #st.sidebar.success("Predict success!")        
                response = getFastAPIResponse(url,data)
                        
                res_dict = {}        
                if(response.content[0] == 123): # json style
                    res_j = response.json()
                    #st.json(res_j)
                    if "details" in res_j.keys():
                        if res_j["details"] == "Could not validate credentials":
                            st.warning("You should login again!")
                            st.session_state.authentication_status = None
                            time.sleep(2)
                            st.experimental_rerun()
                        elif res_j["details"] == "model not found!":
                            st.error("There is no target stock company model!")
                            st.sidebar.error("There is no target stock company model!")
                            st.info("All models will be trained by Airflow daily! But if you contact us, we can manually trigger Airflow NOW!")
                            
                        else:
                            st.error("New error which is not handled. Please contact us ASAP!")
                    else:
                        
                        today = datetime.today()
                        today = today.strftime('%Y-%m-%d')
                        
                        st.sidebar.success("You did it! :heart:")
                        today_close_value = "$" + str(round(res_j["predicted stock price for today"],2))
                        result = pd.DataFrame([today_close_value], columns=["today close price"])
                        
                        result["Date"] = [today]
                        result = result.set_index("Date")
                        
                        st.markdown("### Today " + co_selection +" close value: " + today_close_value)
                        st.table(result)
                                        
                elif(response.content[0] == 255): # image style
                    st.error("Return response is in image format! Something went wrong! Please contact us for help!")
                                        
                else:
                    st.error("Seomthing went wrong! Please contact us ASAP!")
                
                
