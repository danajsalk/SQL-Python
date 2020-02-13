"""
Pushes a DataFrame into a Table."TABLE_NAME" in 1000 line 
increments If you would like to record metrics and append to a table every 
single time, change the action.

INPUTS:
    Server
    Database
    dataframe

OUTPUTS:
    Table in SQL

"""
import datetime
import pandas as pd
import time
import urllib
from sqlalchemy import create_engine


# This functions kicks off load to SQL using the Write/Load Functions below
def send_dataframe_to_sql(df, name, action, index=False):
    """ Increments loads into SQL 1000 rows at a time, creating a new connection with
    each row append
    
    Args:
        df (dataFrame) 
        name (str): SQL table name
        action (str): SQL action overwrite or append
    Returns:
        None:
    """ 
    t = 1000
    current_row = 0
    while current_row < len(df):
        end_row = current_row + t
        if end_row > len(df):
            end_row = len(df)
        if current_row == 0:
            print("Writing to SQL")
            to_SQLTABLE(df.iloc[current_row:end_row, :],
                                        name, action, index)
        else:
            print("APPENDING to Scratchpad")
            to_datateamScratchpad(
                df.iloc[current_row:end_row, :], name, 'append', index)
        current_row = end_row
    print("COMPLETED SQL LOAD")
    

def to_SQLTABLE(df, name, action, index=False):
    """ Actual SQL connection link
    Args:
        df (dataFrame) 
        name (str): table name
        action (str): SQL action overwrite/append
    Returns:
        None: writes table to SQLTABLE
    """ 
    print("Starting your SQL load")
    server = 'server'
    database = 'database'
    params = urllib.parse.quote_plus(
        r'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database +
        ';Trusted_Connection=yes')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params),
                           connect_args={'connect_timeout': 45})


    tstart = time.time()
    df.to_sql(name, schema='dbo', con=engine, if_exists=action,
                      chunksize=30, index=index)
    run_time = time.time() - tstart
    print(name, "is loaded in SQL TABLE. SQL load time is:", run_time,
          "seconds")

##############################################################################################

data_dict = {'fruit': ['apple', 'orange', 'banana', 'peach']
             ,'color': ['red', 'orange', 'yellow', 'orangish']}

df = pd.DataFrame.from_dict(data_dict)
df['TimeStamp'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%d/%m %H:%M")

name_table = "table"
send_dataframe_to_sql(df, name_table, 'replace', index=False) # action = append/replace
