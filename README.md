# DAMG 7245 Big-Data-Systems-Intelligence-Analytics-Labs-Summer-2022

> Team 2
> 
> Cheng Wang NUID: 001280107
> 
> Meihu Qin NUID: 002190486


## 1. Intro

- Our final project is a Web APP which could track those companies stocks from Yahoo Finance API

- Our whole project contains several parts:
  1. FastAPI - Web API
  2. Streamlit - Front end prototype demo
  3. Docker - dockerfile
  4. Github CI/CD - continues integration + deploy
  5. Airflow - set up a daily task to update stock values
  6. PyTest - simple unit tests for fastaapi
  7. Logs - be stored in cloud MySQL and be displayed in Streamlit
  8. MySQL db - log, user, user_follow, company stocks tables
  9. ~~Prometheus + Grafana - display server status(metrics)~~
  10. ~~Prometheus Alert Manager - send alert when server's metrics meets requirememts~~

## 2. Setup

- ~~If S3 credential is filaed, you can create your own AWS S3 bucket and store all required info into `/credentials/` json file~~(In our final project, we ignore this credential file because of security issues)
- Under this repo, you will see a `requirements.txt` file, it contains all Python packages that we installed on our machine.  Use fllowing commands in your terminal to install all required packages
  ```python
  cd ./FinalProject
  pip install requirements.txt
  ```

- Then you will see all dependencies our peoject need will be installed!

## 3. What is in ths repo?

1. api functions
   ```markdown
   Path: ./src/api_functions/
   ```

2. main.py
   ```markdown
   Path: ./src/
   <!--start FastAPI unicorn server -->
   uvicorn main:app --reload 
   ```
3. index.html/result.html
   ```markdown
   Path: ./src/
   ```
4. log
   ```markdown
   Path: ./logs/
   ```
   - no log file inside because I used `.gitignore` to ignore it but you can generate one if you want
   - We also make an easy to generate log for you, you can create a `mysql.yaml` file under `src` folder

   ```markdown
      credentials:
         host: "your_pc_ip_address 127.0.0.1 -> localhost"
         user: "your_username"
         password: "your_userpassword"
         database: "your_db"
   ```

5.  pytest
    ```markdown
    Path: ./src/streamlit/pages/report.html
    ```

6.  requirements.txt
    ```markdown
    Path: ./src/
    You need to use Python 3+ version and user pip to install all dependencies
    pip install requirements.txt 
    ```
7. streamlit
   ```markdown
   Path: ./src/streamlit
   ```

   - You need to use `streamlit run Home.py` to start our streamlit!
   - All `*.py` files into `pages/` folder are other pages for streamlit, you don't need to worry about
8. Airflow dags(only)
   ```markdown
   Path: ./src/airflow
   ```
  
   - This is the only file we need for our daily Airflow dags task
   - You can use docker to set up a airflow server and goto `127.0.0.1:8080` to use your Airflow!
   - if you want to use our dags, you need to add a params when you use docker compose
      - In your `docker-compose.yml` file, you need to add a volume from local dag file path into docker continer `airflow/dags/` path
      

9.  MySQL database (table create SQL script only)
   ```markdown
   Path: ./src/mysql
   ```

## 4. API Functions

> Use `uvicorn main:app --reload` to start FastAPI uvicorn server
> 
> go to : `http://127.0.0.1/8000/`, this is home page
> 
> click `docs` button and you will jump to API documentation

- We create some simple api functions to test
- People who use our api could input some values and get some correct result to see

1. following
   - You need to input your username + company abbreviation name
   - We can search whether you followed this company or not
   - if this company does not exist in the database, we will search it from Yahoo API
   - if this company also DNE in Yahoo API, we will catch this exception and return messages
   - if this company exists in Yahoo API, we will download all 10 years stock history and add you as a follower into our database record

2. save stock price
   - search target company exists or not
   - if exists, we will save 10 yeas stock history
   - if not exists, we will return a exception message

3. stock price search by date
   - You can input a custom date range for searching
      - We only search it from our database if DNE, you will get a not found message
   - We will return result for you xD
  
4. predicted stock price
   - We use airflow trained our related stock company daily(00:00:00)
   - If you just follow a new company which is not in the database now, our Airflow only update it on a new day. But you can trigger it manyally and get this model you need
   - For prediction, we will return a new day's close price!

5. models
   - As point 4 shows, we only return a new day's close price!

6. update stock price
   - We also set up a Airflow dag for updating stock price for all stock company tables daily (00:00:00)
   - You also can manually trigger Airflow dag task as you want
## 5. Attestation 
- WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
- Contribution: Cheng Wang: 50% Meihu Qin: 50%
- Cheng's work: **stramlit, mysql database tables design, dockerfile, Github CI/CD,prometheus(node exporter, status exporter, alertmanager), Grafana, deploy app on cloud(VPS)**
- Meihu's work: **fastAPI, logs, Pytest, writing proposal, Airflow dags and setup, model train, stock finance data collected**
