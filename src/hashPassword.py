import streamlit_authenticator as stauth

name_list = ['meihu','cheng','prof','ta','team1','team3','team4','airflow']
username_list = ['meihu','lemon','prof','ta','team1','team3','team4','airflow']
passwords = ['meihu','cheng','prof','ta','team1','team3','team4','airflow']

hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)

