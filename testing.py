# testing = "ILONDON1124,51.47687912,0.068984,London"
# row = testing.strip().split(",")
import pandas as pd
# print(int(row[-1]))
filename = "C:/Users/Nobody/Documents/aau/6/BachelorProject/dataset/Aalborg_Gade.csv"
df = pd.read_csv(filename,low_memory=False, sep=';',skiprows=2)
df["station_id"] = "gade"
df['Recorded'] = pd.to_datetime(df['Recorded'], format='%d-%m-%Y %H:%M:%S')
print(df)