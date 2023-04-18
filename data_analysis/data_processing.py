import toml
import pandas as pd
import mysql.connector

def preprocess_data(df: pd.DataFrame):
    df_ = df.copy()
    df_['subtitle_neighborhood'] = df_['subtitle_neighborhood'].str.strip()
    return df_

def load_data():
    toml_data = toml.load("./configs/secrets.toml")
    # saving each credential into a variable
    HOST_NAME = toml_data['mysql']['host']
    DATABASE = toml_data['mysql']['database']
    PASSWORD = toml_data['mysql']['password']
    USER = toml_data['mysql']['user']
    PORT = toml_data['mysql']['port']

    mydb = mysql.connector.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True, port=PORT)
    
    df = pd.read_sql('SELECT * FROM crawler_divar_post_info ORDER BY crawl_timestamp DESC LIMIT 300;' , mydb)

    return preprocess_data(df)
