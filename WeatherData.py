import requests
import pandas as pd
from datetime import datetime, timedelta


# startDay = '20191206'
# #startDay = '20200113'
# datetimeStartDay = datetime.strptime(startDay, '%Y%m%d')
# #print(datetimeStartDay)
# ##nextDay = datetimeStartDay + timedelta(days=1)
# #onlyDay = nextDay.strftime('%Y%m%d')
# #print(onlyDay)
# small_df = []
# # response = requests.get('https://api.weather.com/v1/location/EKYT:9:DK/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=m&startDate=20200113')
# # jsonData = response.json()
# # df = pd.json_normalize(jsonData['observations'])
# # print(df.columns)
# for i in range(0,823):
#     nextDay = datetimeStartDay + timedelta(days=i)
#     onlyDay = nextDay.strftime('%Y%m%d')
#     response = requests.get('https://api.weather.com/v1/location/EKYT:9:DK/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=m&startDate='+onlyDay)
#     jsonData = response.json()
#     df = pd.json_normalize(jsonData['observations'])
#     print(df.columns)
#     df = df[['valid_time_gmt', 'heat_index', 'rh', 'pressure', 'wdir', 'wdir_cardinal', 'wspd']]
#     small_df.append(df)
#     response.close()

# largeDF = pd.concat(small_df, ignore_index=True)
# largeDF.to_csv('WeatherData19des-22mar.csv', index=False, sep=',')

# timeTest = 1578963000
# convertTime = datetime.utcfromtimestamp(timeTest)
# convertTime = convertTime + timedelta(hours=2)

# df = pd.read_csv('WeatherData19des-22mar.csv')
# cleanList = []
# for i in range(0, df.shape[0]-1):
#     now = df.loc[i, 'valid_time_gmt']
#     next = df.loc[i+1, 'valid_time_gmt']
#     difference = next - now
#     if difference < 940:
#         if now % 1800 > next % 1800:
#             cleanList.append(i)
#         else:
#             cleanList.append(i+1)
# df = df.drop(cleanList)
# df = df.reset_index(drop=True)

# for i in range(0, df.shape[0]):
#     timeChange = df.loc[i,'valid_time_gmt']
#     convertTime = datetime.utcfromtimestamp(timeChange)
#     convertTime = convertTime + timedelta(hours=2)
#     df.loc[i, 'valid_time_gmt'] = convertTime
# df.to_csv('RemoveBadTimes.csv', index=False)


# df = pd.read_csv('NewWeatherData.csv')
# df['valid_time_gmt'] = pd.to_datetime(df['valid_time_gmt'])
# print(type(df.loc[1, 'valid_time_gmt']))
# if df.loc[1, 'valid_time_gmt'] < df.loc[2, 'valid_time_gmt']:
#     print('<')
# if df.loc[1, 'valid_time_gmt'] > df.loc[2, 'valid_time_gmt']:
#     print('>')

# for i in range(0, df.shape[0]):
#     now = df.loc[i, 'valid_time_gmt']
#     next = df.loc[i+1, 'valid_time_gmt']
#     difference = (next - now).astype
#     print(type(difference))
    # print (difference)

# df = df[['valid_time_gmt', 'heat_index', 'rh', 'pressure', 'wdir', 'wdir_cardinal', 'wspd']]
# df.to_csv('NewWeatherData.csv', index=False)

df = pd.read_csv('RemoveBadTimes.csv')
df['valid_time_gmt'] = pd.to_datetime(df['valid_time_gmt'])

ts = pd.date_range("2019-12-06 00:00:00", "2022-03-09 00:00:00", freq='10min')
print(df.columns)
df =df.set_index('valid_time_gmt').reindex(ts).fillna(method="ffill").rename_axis('valid_time').reset_index()

#df[(df.groupby(["valid_time_gmt"], as_index=False)["valid_time_gmt"].diff().fillna(pd.Timedelta(seconds=0)).dt.seconds <= 1000).reset_index(drop=True)]
print(df.shape)
df.to_csv("teswtaaaaing.csv",index=False)

df1 = pd.read_csv("teswtaaaaing.csv")

ts = pd.date_range("2019-12-06 00:00:00", "2022-03-09 00:00:00", freq='30min')
df1['valid_time_gmt'] = pd.to_datetime(df1['valid_time_gmt'])
df1.index = df1["valid_time_gmt"]
df2 = pd.DataFrame(index=ts)
print(df2.index)
df3 =df2.join(df1)
#df3 = pd.concat([df,df2],axis=1)
df3.to_csv("zz.csv",index=False)





# df = pd.read_csv("WeatherData19des-22marNotUnix.csv")
# print(df)
# df['valid_time_gmt'] = pd.to_datetime(df['valid_time_gmt'])
# df.index = df["valid_time_gmt"]
# df1 = pd.read_csv("AAl_t_19des-22mar_Skew.csv")
# df1['Recorded'] = pd.to_datetime(df1['Recorded'])
# df1.index = df1["Recorded"]
# df2 = df1.join(df)
# df2 = df2.drop(columns="valid_time_gmt")
# df2["station_id"]="Tag"
# df2 = df2[["Recorded","NO2","NOx","O3","heat_index","rh","pressure","wdir","wdir_cardinal","wspd","station_id"]]
# df2.to_csv("AAl_T_Weather_SkewFix_19des-22mar.csv",index=False)

# df = pd.read_csv("Aal_T_19des-22mar.csv",sep=";")
# df = df[["Recorded","CO","NO2","SO2","NOx","PM_2.5_Lvs","comment"]]
# df = df[["Recorded","NO2","NOx","O3"]]
# df.to_csv("fixedorder.csv",index=False,sep=";")
# 07-03-2022 12:30:00
# current_start_time_1 = "2022-03-07" + " 12:30:00"
# current_end_time_1 = "2019-12-06" + " 10:00:00"
# start_day = datetime.strptime(current_start_time_1, '%Y-%m-%d %H:%M:%S')
# end_day = datetime.strptime(current_end_time_1, '%Y-%m-%d %H:%M:%S')
# dates = pd.date_range(end_day, start_day, freq='30min')
# print(dates)
# df1 = pd.DataFrame(index=dates)
# df1["Recorded"]=dates
# #df1["station"] = "Gade"
# #df1['Recorded'] = df1.index.map(lambda x: str(x))
# print(df1)
# df  = pd.read_csv("Aalborg_Tag.csv",sep=";")
# df['Recorded'] = pd.to_datetime(df['Recorded'], format='%d-%m-%Y %H:%M:%S')
# df = df.sort_values(by=["Recorded"],ascending=True)
# df.index = df["Recorded"]
# #df["station"]="Gade"

# df2 = pd.concat([df1,df],axis=1)
# # # # #df2 = pd.merge(df1,df,how="left")
# df2.to_csv("AAL_T_19des-22mar.csv",index=False,sep=";")

# df2 = pd.read_csv("AAl_T_19des-22mar.csv",sep=";")
# print(df2.columns)
# df2 = df2.drop(columns=["Recorded1"])

# df2.to_csv("AAl_T_19des-22mar.csv",index=False,sep=";")


# df = pd.read_csv("AAl_G_Weather_SkewFix_19des-22mar.csv")
# df["Recorded"] = pd.to_datetime(df['Recorded'])
# df.index = df["Recorded"]

# df[["NO2","NOx","CO","SO2"]] =df[["NO2","NOx","CO","SO2"]].interpolate(method="linear").round(2)

# df.to_csv("interpolatelinear.csv",index=False)





# df = pd.read_csv("Aalborg_Tag.csv",sep=";")

# #df = df.drop(columns="PM_2.5_Lvs")
# df = df[["Recorded","NO2","NOx","O3"]]

# df.to_csv("Aalborg_Tag.csv",index=False,sep=";")

# df = pd.read_csv("AAl_T_Weather_SkewFix_Int_19des-22mar.csv")


# df = df[["Recorded","NO2","NOx","heat_index","rh","pressure","wdir","wdir_cardinal","wspd","station_id"]]
# df.to_csv("T.csv",index=False)