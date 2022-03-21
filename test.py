import pandas as pd
df = pd.read_csv("./dataset/Aalborg_Gade_FebTilNu.csv",skiprows=2,sep=";")
df = df[["Recorded","NO2","NOx"    
]]
df.to_csv("./Dataset/Aalborg_Gade_Med_NO2_NOx",index=False)