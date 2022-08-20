import streamlit as st
import numpy as np
import yaml
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests
import time
#import matplotlib as plt


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

###########################################################

# get response from FastAPI
def getFastAPIResponse(url,data): #data_bin
    #rlt = requests.post('http://127.0.0.1:8000/api/get/fileNameAndClass/', json=data_bin).json()
    
    token_str = 'bearer ' + st.session_state["token"]
    headers = {'accept': 'application/json','authorization': str(token_str)}
    response = requests.get(url=url,params=data,headers=headers,verify=False)

    return response

# it will comes out conflict when we set a default for date and also change date by on_change callback
# def check_startDate():
#     if(st.session_state.startDate > st.session_state.endDate):
#         st.sidebar.warning("startDate should be earlier than or equal to endDate!")
#         st.session_state.startDate = st.session_state.endDate

# def check_endDate():
#     if(st.session_state.endDate < st.session_state.startDate):
#         st.sidebar.warning("endDate should be later than or equal to endDate!")
#         st.session_state.startDate = st.session_state.endDate


with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
        
        stock_co = st.text_input("",max_chars=10, placeholder="AAPL", disabled=False)
       
        selection = st.selectbox('How would you like to select stock history?',('1 day', '1 week','1 month'))
        isClick = st.button("OK")
        isFollow = st.button("Follow")
        
    
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    st.title("Welcome")


    if(isFollow):
        if(stock_co != ""):
            
            # get response from FastAPI
            url = 'http://127.0.0.1:8000/api/get/following/'
            data = {"username":st.session_state["username"], "co_abbr": stock_co.upper()}
            #st.write(st.session_state["username"])
            #st.write(stock_co)
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
                    elif "not a valid company stock name!" in res_j["details"]:
                        st.sidebar.warning("There is no target stock company!")
                        st.warning("There is no target stock company!")
                    elif "You already followed!" in res_j["details"]:
                        st.sidebar.warning("You've already followed " + stock_co)
                        st.warning("You've already followed " + stock_co)
                    else:
                        st.error("New error which is not handled. Please contact us ASAP!")
                else:
                    #st.info(res_j[st.session_state["username"]])
                    #Todo return follow api response!
                    if "You already followed" in res_j[st.session_state["username"]]:
                        st.sidebar.warning("You've already followed " + stock_co)
                        st.warning("You've already followed " + stock_co)
                    elif ("Table created! Saving success!" in res_j[st.session_state["username"]]):
                        st.sidebar.success("You did it! :heart:")
                        st.success("You successfully followed " + stock_co + " :heart:")
                    elif("Table already exists! You successfully followed it!" in res_j[st.session_state["username"]]):
                        st.success("You successfully followed " + stock_co + " :heart:")
                        st.sidebar.success("You successfully followed " + stock_co + " :heart:")
                    else:
                        st.error("Something went wrong! Please contact us ASAP!")

                        
            elif(response.content[0] == 255): # image style
                st.error("Return response is in image format! Something went wrong! Please contact us for help!")
                        
            else:
                st.error("Seomthing went wrong! Please contact us for help!")
        else:
            st.warning("Do not leave commpany abbreviation name blank!")


    if(isClick == True):
        time_interval = 0
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
        # elif(selection == "1 year"):
        #     time_interval = 365
        #     startDate = datetime.today()+timedelta(-time_interval)
        #     endDate = yesterday
        else:
            st.error("Seomthign went wrong! Please contact us ASAP!")
        
        
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
            if stock_co != "":
                
                co_fullname = "Apple"
                # if we can find a way to get company full name from company abbreviation name or reverse -> That will be helpful
                # Todo    
                    
                    
                df = pd.DataFrame([stock_co.upper(),co_fullname,startDate,endDate],columns=["Your input"],index=["Company abbr name","official name","start date","end date"])
                st.table(df)

                url = 'http://127.0.0.1:8000/api/get/stockprice_search_by_date/'
                data = {"compamyabbreviation": stock_co.upper(),"startdate":startDate, "enddate":endDate}
                
                
                # Display information needed as FasrAPI request params
                # st.write(stock_co)
                # st.write(startDate)
                # st.write(endDate)
                
                response = getFastAPIResponse(url,data)
                #st.write(response) # 200 OK 404 not found 500 table error 401 need credential(JWT)
                res_dict = {}        
                if(response.content[0] == 123): # json style
                    res_j = response.json()
                    if "details" in res_j.keys():
                        if res_j["details"] == "Could not validate credentials":
                            st.warning("You should login again!")
                            st.session_state.authentication_status = None
                            time.sleep(2)
                            st.experimental_rerun()
                        elif "not a valid company stock name!" in res_j["details"]:
                            st.sidebar.warning("There is no target stock company!")
                            st.warning("There is no target stock company!")
                        else:
                            st.error("New error which is not handled. Please contact us ASAP!")
                    else:
                        st.sidebar.success("You did it! :heart:")
                        with st.expander("See results"):
                            st.table(res_j)
                        
                        #valied_days = len(list(res_j["Date"].values()))
                        #st.sidebar.info("Total valied days between " + str(startDate) + " and " + str(endDate) + " : " + str(valied_days) + " days")
                        
                        
                        #Todo display graph
                        if res_j["Date"] != {}:
                            df_history = pd.DataFrame(res_j,columns=["High","Low","Open","Close","Adj Close","Date"])
                            df_history["Date"] = df_history["Date"].replace(to_replace=r'T00:00:00', value='', regex=True)
                            df_history= df_history.rename(columns={'Date':'index'}).set_index('index')
                             
                            df_volume = pd.DataFrame(res_j,columns=['Date','Volume'])
                            df_volume= df_volume.rename(columns={'Date':'index'}).set_index('index')
                             
                            if(time_interval != 1):
                                st.line_chart(df_history)
                                st.line_chart(df_volume)
                            else:
                                df_res = pd.DataFrame(res_j)
                                df_res= df_res.rename(columns={'Date':'index'}).set_index('index')
                                st.table(df_res)
                        else:
                            st.warning("There is no data between  " + str(startDate) + "  and  " + str(endDate) + "!")

                            
                elif(response.content[0] == 255): # image style
                    st.error("Return response is in image format! Something went wrong! Please contact us for help!")
                            
                else:
                    st.error("Seomthing went wrong! Please contact us ASAP!")
            

                
                
            else:
                st.warning("Do not leave commpany abbreviation name blank!")
                
