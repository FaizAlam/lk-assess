# import required module
import sqlite3
import pandas as pd
# connect to database
con = sqlite3.connect('C:/Users/mohdf/Desktop/projects/assignment/loop-kitchen/mine/instance/loop.sqlite')

# create cursor object
cur = con.cursor()

df = pd.read_csv('./data/store_status.csv')
df1= pd.read_csv('./data/business_hour.csv')
df2=pd.read_csv('./data/time_zone.csv')


df= df.iloc[:1000]
df1=df1.iloc[:1000]
df2= df2.iloc[:1000]


# cursor = cur.execute('select * from ')
# names = list(map(lambda x: x[0], cursor.description))
# print(names)

exec_param = """INSERT INTO poll 
                (storeId,status,timestampUtc) 
                VALUES 
                (?,?,?)"""
for i,row in df.iterrows():
    store_id, status, timestmp = row['store_id'], row['status'], row['timestamp_utc']
    data = (store_id,status,timestmp)
    cur.execute(exec_param,data)
    con.commit()


#store businessTime data
exec_param = """INSERT INTO businessHour 
                (storeId,day_of_Week,startTimeLocal, endTimeLocal) 
                VALUES 
                (?,?,?,?)"""
for i,row in df1.iterrows():
    store_id,day, startTime, endTime = row['store_id'], row['day'], row['start_time_local'], row['end_time_local']
    data = (store_id,day, startTime,endTime)
    cur.execute(exec_param,data)
    con.commit()

#store TimeZone data
exec_param = """INSERT INTO TimeZone 
                (storeId,timezoneStr) 
                VALUES 
                (?,?)"""
for i,row in df2.iterrows():
    store_id, timezn= row['store_id'], row['timezone_str']
    data = (store_id,timezn)
    cur.execute(exec_param,data)
    con.commit()


# data = cur.execute("SELECT * from TimeZone").fetchall()
# print(data)

# cursor = cur.execute('select * from businessHour')
# names = list(map(lambda x: x[0], cursor.description))
# print(names)

# commit changes
con.commit()

# terminate the connection
con.close()
