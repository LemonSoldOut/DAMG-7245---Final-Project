import streamlit.components.v1 as components
import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
import pandas as pd
import numpy as np
import time
import base64
from PIL import Image
import os
import requests
import pymysql
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns




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



con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
c = con.cursor()

with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
        
        options = st.multiselect(
            'What log info you want to get?',
            ['logId','requestUrl','userId', 'response', 'logTime', 'code_', 'username','level_','processTime'],
            ['logId','username','requestUrl','code_','level_'],key="log_output_selection")

        num_logs = st.number_input(label="Choose number of logs you want to see", min_value=0, max_value=40, step=5)
        isNumLogsButtonClick = st.button("OK")
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")

if(st.session_state.authentication_status == True):
    st.markdown("# Log Analysis")
    #st.markdown("## Try it :smile:")
    if(isNumLogsButtonClick == True):
        if(num_logs != 0):
            sql = "SELECT "
            # sql_lmit = "LIMIT 10"
            for item in options:
                if(item == options[-1]):
                    sql = sql + "lt." + str(item)
                else:
                    if(item == "username"):
                        sql = sql + "ut."+str(item) + ", "
                    else:
                        sql = sql + "lt." + str(item) + ", "
                
            sql = sql + " FROM log_table lt INNER JOIN user_table ut ON lt.userId = ut.userId WHERE ut.username = '" + st.session_state.username + "' LIMIT " + str(num_logs)
            #st.write(sql)
            c.execute(sql)
            result = c.fetchall()
            #st.write(result)
            df = pd.DataFrame(result, columns = options)
            st.table(df)
        else:
            list_keys = [],
            list_values = []
            df = pd.DataFrame(list_values,columns=list_keys)
            st.warning("You should give a number which is greater than 0!")
            st.table(df)
        
        
        # if("logTime" in options):
        #     log_start = st.sidebar.date_input("Log Sart from",datetime.date(2022, 6, 29),key="log_start",on_change=modify_start_date_to_default)
        #     log_end = st.sidebar.date_input("Log End",datetime.date(2022, 6, 29),key="log_end",on_change=modify_end_date_to_default)
            
            # Todo: start time -> end time log query (if have time)
            # time_start = st.time_input('Set an alarm for', datetime.time(0, 0),key="time_start")
            # time_end = st.time_input('Set an alarm for', datetime.time(0, 0),key="time_end")
    
            # st.write('Start time', time_start)
            # st.write('End time', time_end)
            
            # st.write('Log start from:', log_start)
            # st.write('Log start from:', log_end)
        
    
    if(st.session_state["username"] != "cheng" and st.session_state["username"] != "meihu" and st.session_state["username"] != "prof" and st.session_state["username"] != "ta"):
        
    
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "'")
        count_current_user_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.code_= 200")
        count_success_user_log = c.fetchall()[0][0]
        #st.write(count_success_user_log)
        #Creating the dataset
        keys = ["success","fail","all"]
        #keys.append(st.session_state.username)
        values = [count_success_user_log,count_current_user_log-count_success_user_log,count_current_user_log]
        #values.append(count_current_user_log)

        fig = plt.figure(figsize = (6, 3))

        plt.bar(keys, values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of API functions calling")
        plt.title(st.session_state.username + "'s API Functions Call Bar Chart")
        st.pyplot(fig)
        
        ###########################################
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'pass', 'fail'
        sizes = [count_success_user_log, count_current_user_log-count_success_user_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(st.session_state.username + "'s API functions Call Pie Chart")
        st.pyplot(fig1)
        
        
        #####################################################
        c.execute("SELECT requestUrl FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "'")
        function_name_1 = "predicted_stock_price"
        count_func1 = 0
        function_name_2 = "following"
        count_func2 = 0
        function_name_3 = "imgSizeRange"
        count_func3 = 0
        function_name_4 = "save_stock_price"
        count_func4 = 0
        function_name_5 = "stockprice_search_by_date"
        count_func5 = 0
        
        
        #Todo 改名字
        result = c.fetchall()
        for item in result:
            if(function_name_1 in item[0]):
               count_func1 += 1
            if(function_name_2 in item[0]):
                count_func2 += 1
            if(function_name_3 in item[0]):
                count_func3 += 1
            if(function_name_4 in item[0]):
                count_func4 += 1
            if(function_name_5 in item[0]):
                count_func5 += 1
        
        
        df10 = pd.DataFrame({
            'function': [function_name_1, function_name_2, function_name_3, function_name_4,function_name_5],
            st.session_state.username: [count_func1,count_func2,count_func3,count_func4,count_func5]
        })

        df10 = df10.rename(columns={'function':'index'}).set_index('index')

        #st.line_chart(df2)
        st.bar_chart(df10)
        

        
        ####################################################
        
        
        
    else:
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "'")
        count_current_user_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.code_= 200")
        count_success_user_log = c.fetchall()[0][0]
        #st.write(count_success_user_log)
        #Creating the dataset
        keys = ["success","fail","all"]
        #keys.append(st.session_state.username)
        values = [count_success_user_log,count_current_user_log-count_success_user_log,count_current_user_log]
        #values.append(count_current_user_log)

        fig = plt.figure(figsize = (6, 3))

        plt.bar(keys, values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of API functions calling")
        plt.title(st.session_state.username + "'s API Functions Call Bar Chart")
        st.pyplot(fig)
        
        ###########################################
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'pass', 'fail'
        sizes = [count_success_user_log, count_current_user_log-count_success_user_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(st.session_state.username + "'s API functions Call Pie Chart")
        st.pyplot(fig1)
        
        
        ########################################
        
        
        c.execute("SELECT ut.username, COUNT(*) FROM log_table lt INNER JOIN user_table ut ON lt.userId = ut.userId GROUP BY ut.userId")   
        admin_result = c.fetchall()
        admin_keys = []
        admin_values = []
        for item in admin_result:
            admin_values.append(item[1])
            admin_keys.append(item[0])

        fig = plt.figure(figsize = (6, 3))

        plt.bar(admin_keys, admin_values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of API functions calling")
        plt.title("API Functions Call Bar Chart Record")
        st.pyplot(fig)
        

        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId")
        count_current_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId" + " WHERE lt.code_= 200")
        count_success_log = c.fetchall()[0][0]
        labels = 'pass', 'fail'
        sizes = [count_success_log, count_current_log-count_success_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("API functions Call Pie Chart")
        st.pyplot(fig1)
        
        
        
        
        #===================================================================================================
        
        c.execute("SELECT requestUrl FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId")
        function_name_1 = "predicted_stock_price"
        count_func1 = 0
        function_name_2 = "following"
        count_func2 = 0
        function_name_3 = "imgSizeRange"
        count_func3 = 0
        function_name_4 = "save_stock_price"
        count_func4 = 0
        function_name_5 = "stockprice_search_by_date"
        count_func5 = 0
        
        
        #Todo 改名字
        result = c.fetchall()
        for item in result:
            if(function_name_1 in item[0]):
               count_func1 += 1
            if(function_name_2 in item[0]):
                count_func2 += 1
            if(function_name_3 in item[0]):
                count_func3 += 1
            if(function_name_4 in item[0]):
                count_func4 += 1
            if(function_name_5 in item[0]):
                count_func5 += 1
        
        
        df2 = pd.DataFrame({
            'function': [function_name_1, function_name_2, function_name_3, function_name_4,function_name_5],
            st.session_state.username: [count_func1,count_func2,count_func3,count_func4,count_func5]
        })

        df2 = df2.rename(columns={'function':'index'}).set_index('index')

        #st.line_chart(df2)
        st.bar_chart(df2)
        
        
        sql5 = """
            SELECT
	            count( sft.stockAbbrName ),
	            sft.userId,
	            ut.username
	        FROM
	            `stock_follow_table` sft 
	
	        INNER JOIN user_table ut ON ut.userId = sft.userId 

            GROUP BY userId;
        
        """
        
        c.execute(sql5)
        getFollowData = c.fetchall()
        #st.write(getFollowData)
        user_list = []
        user_follow = []
        for i in getFollowData:
            user_list.append(i[2])
            user_follow.append(i[0])

        #st.write(user_list)
        #st.write(user_follow)
        df9 = pd.DataFrame({'followed number': user_follow,'username':user_list})
        df9 = df9.rename(columns={'username':'index'}).set_index('index')
        st.bar_chart(df9)
        
        