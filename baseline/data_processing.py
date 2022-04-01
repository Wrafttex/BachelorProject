# -*- coding:utf-8 -*-
from calendar import leapdays
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
import time
import re
import joblib
import requests
from torch import true_divide
from draw import *
import xlrd
from pre_train import model_predict
from unit import *
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

base_path_1 = "./dataset/"
base_path_2 = "./dataset/tmp/"
base_path_3 = "./output/"


#NOTE lng højre venstre
#NOTE lat op og ned
#DONE given load_station city as a paremeter to make it more dynamic
def load_station(city="Aalborg"):

    filename = base_path_1 + city +"_aq_station.csv" #TODO city name is not hardcoded but maybe checker to see if the file exist should be done
    fr = open(filename)                           
    aalborg_stations = {}
    flag = 0
    i = 0
    for line in fr.readlines():
        if flag == 0:
            flag = 1
            continue
        row = line.strip().split(";")#TODO what delimiter should we should
        aalborg_stations[row[0]] = {}
        aalborg_stations[row[0]]['lng'] = float(row[1]) #TODO make dynamic by check where in the head it is located at
        aalborg_stations[row[0]]['lat'] = float(row[2])
        aalborg_stations[row[0]]['type_id'] = int(row[-1])
        aalborg_stations[row[0]]['station_num_id'] = i
        i += 1
    stations = {}
    
    stations[city] = aalborg_stations #DONE isn't hardcoded to one specific city
    return stations


# 加载原始数据
#DONE csv files not merged to one, now are two because of aq paremeter not the same
def load_data(city, start_time, end_time, current_day=False):
    if current_day == False:
        if city == "Aalborg": 
            filename = base_path_1 + 'Aalborg_aq.csv'
            df = pd.read_csv(filename, sep=',')                                           
            df.rename(columns={ 'NO2': 'NO2_Concentration',
                    'Recorded': 'time', "NOx":"NOx_Concentration",}, inplace=True)  #TODO in the future make a function to sort timeformat
    elif current_day == True:
        #filename = "C:/Users/Nobody/Documents/aau/6/jacob/KDD_CUP_2018-master/dataset/tmp/beijing_17_18_aq.csv"
        filename = base_path_1 + city +"_aq_current.csv" 
        df = pd.read_csv(filename, sep=',')
        #print(df)
        df.rename(columns={ 'NO2': 'NO2_Concentration',
                    'Recorded': 'time', "NOx":"NOx_Concentration",}, inplace=True)
                
    print(df)
    df['time'] = pd.to_datetime(df['time'])
    df.index = df['time']
    df['time_week'] = df.index.map(lambda x: x.weekday)
    df['time_year'] = df.index.map(lambda x: x.year)
    df['time_month'] = df.index.map(lambda x: x.month)
    df['time_day'] = df.index.map(lambda x: x.day)
    df['time_hour'] = df.index.map(lambda x: x.hour)
    #print
    #print(df)

    df = df[["station_id", "NO2_Concentration", "NOx_Concentration",
            'time_year', 'time_month', 'time_week', 'time_day', 'time_hour']]
        
    # print df
    # df = df.dropna(axis=0)
    # print df.size
    # process_loss_data(df, city, stations, length = 24*3, pre_train_flag=pre_train_flag)
    # df.to_csv(base_path_3 + city + '.csv', index=True, sep=',')
    #print("before return",df)
    return df


# 加载处理后的数据
def load_data_process(city, current_day=False):
    if current_day == False:
        filename = base_path_2 + city+ "_airquality_processing.csv"
    else:
        filename = base_path_2 + city + "_current_day_processing.csv"
    df = pd.read_csv(filename, sep=',')
    df['time'] = pd.to_datetime(df['time'])
    df.index = df['time']
    return df


# 计算相似度
def cal_similar(df1, df2):
    # print df1.mean(), df2.mean()
    df3 = df1.sub(df2)
    return np.sqrt(df3.mul(df3).mean())


# 计算最接近的K个站点
def KNN(station_group, attr, k=6):
    tmp = {}
    for station, group in station_group.items():
        # print group.size
        tmp[station] = group[attr]
    neighborhood_k = {}
    for station1 in tmp.keys():
        dist = {}
        print (station1, tmp[station1].mean())
        for station2 in tmp.keys():
            if station1 == station2:
                continue
            distance = cal_similar(tmp[station1], tmp[station2])
            dist[station2] = distance
        dist = sorted(dist.items(), key=lambda d: d[1])
        print (dist[:k])
        neighborhood_k[station1] = [x[0] for x in dist[:k] if x[1] / tmp[station1].mean() < 0.20]
    return neighborhood_k

#There are only 1, 2, or 3 missing values
# 缺失值只有1,2,或者3个
def between_two_point(station_group, attr_need):
    num = 0
    for station, group in station_group.items():
        # print "group.values.shape: ", group.values.shape
        values1 = group[attr_need].values
        # print np.isnan(values1).sum()
        for i in range(1, values1.shape[0] - 1):
            for j in range(values1.shape[1]):
                #print(j)
                #print(values1[i,j])
                if np.isnan(values1[i, j]):
                    if not np.isnan(values1[i - 1, j]) and not np.isnan(values1[i + 1, j]): #one entry before and one after
                        values1[i, j] = (values1[i - 1, j] + values1[i + 1, j]) / 2 #takes the average of those 2 value
                        num += 1
                        continue
                    if i < 2:
                        continue
                    if not np.isnan(values1[i - 2, j]) and not np.isnan(values1[i + 1, j]): #two before and one after
                        values1[i, j] = (values1[i - 2, j] + values1[i + 1, j] * 2) / 3 #average
                        values1[i - 1, j] = (values1[i - 2, j] * 2 + values1[i + 1, j]) / 3
                        num += 2
                        continue
                    if i >= values1.shape[0] - 2:
                        continue
                    if not np.isnan(values1[i - 1, j]) and not np.isnan(values1[i + 2, j]):
                        values1[i, j] = (values1[i - 1, j] * 2 + values1[i + 2, j]) / 3
                        values1[i + 1, j] = (values1[i - 1, j] + values1[i + 2, j] * 2) / 3
                        num += 2
                        continue
                    if not np.isnan(values1[i - 2, j]) and not np.isnan(values1[i + 2, j]):
                        values1[i - 1, j] = (values1[i - 2, j] * 3 + values1[i + 2, j]) / 4
                        values1[i, j] = (values1[i - 2, j] * 2 + values1[i + 2, j] * 2) / 4
                        values1[i + 1, j] = (values1[i - 2, j] + values1[i + 2, j] * 3) / 4
                        num += 3
                        continue
                        # print np.isnan(values1).sum()
                        # group[["PM25_Concentration", "PM10_Concentration", "O3_Concentration"]].values = values1
        group.loc[:, attr_need] = values1
        # print "group.values.shape: ", group.values.shape
    print ("num: ", num)

#Fill missing values with a pretrained model
# 利用预训练的模型 填补缺失值
#TODO need to change to be able to open our air quality model
def pre_train(station_group, city, stations, attr_need, length, day=None):
    model_file = base_path_2 + city + "_NO2_best.model"
    reg_NO2 = joblib.load(model_file)
    model_file = base_path_2 + city + "_NOx_best.model"
    reg_NOx = joblib.load(model_file)
    nan_num = 0
    total_error = 0.0
    total_num = 0

    for station, group in station_group.items():
        print(station)
        if day is None:
            values1 = group[attr_need].values
        else:
            values1 = group[day:][attr_need].values
        print(values1.shape[0]- length)
        for i in range(0, values1.shape[0] - length):
            #print(i)
            # print i
            #print(values1)
            #input("values1")
            #print(values1[i + length, -2:])
            #input("values1[i + length, -2:]")
            tmp = [stations[city][station]["type_id"], stations[city][station]["station_num_id"]]
            tmp += list(values1[i + length, -2:])
            values2 = values1[i: i + length, :2]
            values2 = list(values2.T.flatten())
            tmp += values2
            values2 = values1[i + length, :2]
                # values2 = list(values2.flatten())
                # tmp += values2
                # values2 = list(values2.flatten())
                # tmp += values2
            # print tmp
            tmp = np.array(tmp)
            if np.isnan(tmp).sum() > 0:
                continue
            ans_NO2 = model_predict(tmp, reg_NO2, city,stations, attribution="NO2") #TODO can be done as a for in loop
            ans_NOx = model_predict(tmp, reg_NOx, city,stations, attribution="NOx") 
            # print ans_PM25, ans_PM10
            #TODO check what these if statement are checking for 
            if np.isnan(values2[0]) or values2[0] < 0:
                values1[i + length, 0] = ans_NO2
                nan_num += 1
            else:
                total_num += 1
                total_error += np.abs(values1[i + length, 0] - ans_NO2) / (values1[i + length, 0] + ans_NO2) * 2
            
            if np.isnan(values2[1]) or values2[1] < 0:
                values1[i + length, 1] = ans_NOx
                nan_num += 1
            else:
                total_num += 1
                total_error += np.abs(values1[i + length, 1] - ans_NOx) / (values1[i + length, 1] + ans_NOx) * 2

        if day is None:
            group.loc[:, attr_need] = values1
        else:
            group[day:].loc[:, attr_need] = values1
    if total_num == 0:
        total_error = 0.0
        total_num = 1
    print (nan_num, total_error / total_num)


# 加载预训练的数据
#TODO in if statement check what the differes is between them, depending on it, might need to change it
def pre_train_data(station_group, stations, city, attr_need, length):
    ans = []
    #print(pos_station)
    for station, group in station_group.items():
        values1 = group[attr_need].values
        #print(group[attr_need])
        #input("values1")
        #print(values1[i + length, -2:])
        #input("values1[i + length, -2:]")
        # print "length: ", length
        # print "values1.shape", values1.shape
        for i in range(0, values1.shape[0] - length):
            tmp = [stations[city][station]["type_id"], stations[city][station]["station_num_id"]]
            tmp += list(values1[i + length, -2:])
            #print(tmp)
            #input("tmp")
            values2 = values1[i: i + length, :2]
            values2 = list(values2.T.flatten())
            tmp += values2
            values2 = values1[i + length, :2]
            values2 = list(values2.flatten())
            tmp += values2
               
            # print tmp
            #print("before",tmp)
            tmp = np.array(tmp)
            #print("after",tmp)
            #print(np.isnan(tmp).sum())
            #print(len(tmp))
            #if i == 2:
            #    time.sleep(1000000000000000000000000)
            
            if np.isnan(tmp).sum() > 0:
                #print("continue",tmp)
                continue
            #print("tmp",tmp)
            ans.append(tmp)
    ans = np.array(ans)
    print ("ans.shape", ans.shape)
    np.savetxt(base_path_2 + city+ '_training_pre.csv', ans, delimiter=',')
    return ans


# 加载最终训练的数据
def train_data(station_group, stations, city, attr_need, length):
    ans = []
    for station, group in station_group.items():
        values1 = group[attr_need].values
        for i in range(0, values1.shape[0] - length + 1, 24):
            # print i
            tmp = [stations[city][station]["type_id"], stations[city][station]["station_num_id"]]
            tmp += list(values1[i + length - 24, -4: -1])
            tmp += list(values1[i + length - 48, -4: -1])
            values2 = values1[i: i + length - 48, :2]
            values2 = list(values2.T.flatten())
            tmp += values2
            values2 = values1[i + length - 48:i + length, :2]
            values2 = list(values2.T.flatten())
            tmp += values2
            tmp += values2
            # print tmp
            #print(tmp)
            tmp = np.array(tmp)
            #print(tmp)
            if np.isnan(tmp).sum() > 0:
                #print(tmp)
                continue
                
            ans.append(tmp)
    ans = np.array(ans)
    np.savetxt(base_path_2 + city+ '_training.csv', ans, delimiter=',')
    return ans



# 前四天用整体的平均值填补
#TODO if statements are hardcoded to only work with bj and ld, same with date_start variable 
def four_days(df, station_group, city, attr_need):
    
    date_start = "2020-01-14"
    group_ = df[date_start:].groupby(["station_id", 'time_week', 'time_hour'])
    for station, group in station_group.items():
        # print group["2017-01-01"]
        values1 = group["2020-01-14":"2020-01-17"][attr_need].values
        # print "1 ", values1
        for i in range(values1.shape[0]):
            values = group_.get_group((station, values1[i, -2], values1[i, -1]))[
                ["NO2_Concentration", "NOx_Concentration"]].mean().values
                # if np.isnan(values).sum() > 0:
                #     print "station:", station
            if np.isnan(values1[i, 0]) or values1[i, 0] < 0:
                values1[i, 0] = values[0]
            if np.isnan(values1[i, 1]) or values1[i, 1] < 0:
                values1[i, 1] = values[1]
        # print group["2017-01-01"]
        # print "2 ", values1
        group["2020-01-14":"2020-01-17"].loc[:, attr_need] = values1




# 处理丢失数据
#DONE added if statement for aalborg
#TODO if statement should be itself able to see what it needed 
def process_loss_data(df, city, stations, length=24 * 3, pre_train_flag=True):
    ans_df = df.sort_index()
    group = ans_df.groupby("station_id")
    station_group = {}
    for name, g in group:
        station_group[name] = g.sort_index()
        # print station_group[name] #header: time,time_week,time_year,time_month,time_day,time_hour,station_id,PM25_Concentration,NO2_Concentration,SO2_Concentration,CO_Concentration,NOx_Concentration,O3_Concentration 
    attr_need = ["NO2_Concentration", "NOx_Concentration",'time_year',
                'time_month', 'time_day', 'time_week', 'time_hour']  
    #print("station___:",station_group)
    between_two_point(station_group, attr_need)#we have more than 3 missing data point at the same time
    # neighborhood_k = KNN(station_group, attr="PM10_Concentration")
    # print neighborhood_k
    # for station in neighborhood_k.keys():
    #     neighborhood = neighborhood_k[station]
    #     if len(neighborhood)==0:
    #         continue
    if pre_train_flag == True:
        #print("test",station_group)
        ans = pre_train_data(station_group, stations, city, attr_need, length)
    else:
        #print("before four days")
        four_days(ans_df, station_group, city, attr_need)
        #print("else in process_loss_data",station_group)
        pre_train(station_group, city, stations, attr_need, length)
        print("before train_data")
        ans = train_data(station_group, stations, city,  attr_need, length=24 * 5)
    import pickle
    f1 = open(base_path_3 + city+ '_data_processing.pkl', 'wb')
    pickle.dump(station_group, f1, True)
    return ans


# # 画图分析
def analysis(df, stations, city):
    day = "2020-01-14"
    num = 800
    # draw_single_station_day(df, city, stations, start_day=day, num=num)
    draw_single_station(df, city, stations, start_day=day)


# 从处理好的历史数据中获取对应时间的数据
def history_data(city, stations, start_day="2022-01-05", end_day="2018-04-10"):
    f1 = open(base_path_3 + city + '_data_processing.pkl', 'rb')
    # f1 = file(base_path_3 + city + '_data_history_KNN.pkl', 'rb'
    station_group = pd.read_pickle(f1)
    city_station = stations[city]
    ans = {}
    for station, group in station_group.items():
        
        group = group[start_day: end_day]
        #print(start_day,end_day)
       
        # print group["station_id"]
        # group["station_id"] = np.array([station]*group.values.shape[0])
      
        values = group[["station_id","NO2_Concentration","NOx_Concentration","time", 'time_year',
                        'time_month', 'time_day', 'time_week', 'time_hour'] ] 
        #print(group)
        ans[station] = values
        # print values
        #print(ans)
        
    return ans



'''
处理好的数据保存在本地
最近的数据
base_path_3 + city + '_data_post.pkl'
历史数据
base_path_3 + city + '_data_history.pkl'
最新的数据
base_path_2 + city + "_current_day_processing.csv"
'''


def post_data(city="Aalborg"):
    stations = load_station()
    ans_post = history_data(city=city, stations=stations, start_day="2022-01-05", end_day="2022-01-14")
    import pickle
    #print("ans_post",ans_post)
    f1 = open(base_path_3 + city + '_data_post.pkl', 'wb')
    # print ans_post
    pickle.dump(ans_post, f1, True)
    ans_history = history_data(city=city, stations=stations, start_day="2021-12-04", end_day="2022-01-04")
    f2 = open(base_path_3 + city+ '_data_history.pkl', 'wb')
    pickle.dump(ans_history, f2, True)

    #NOTE Based on what they have done 
    current_start_time = "2022-01-15-0"
    current_end_time = "2022-01-19-23"
    # get_data(start_time=start_time, end_time=end_time, city=city, current_day=True)
    df = load_data(city=city, start_time=current_start_time, end_time=current_end_time, current_day=True)
    filename = base_path_2 + city + "_current_day_processing.csv"
    current_start_time_1 = "2022-01-15" + " 00:00:00"
    current_end_time_1 = "2022-01-19" + " 23:00:00"
    write_to_process(df, start_time=current_start_time_1, end_time=current_end_time_1, filename=filename)


# 获取所有的数据进行预测                         2022-03-03 2022-03-11
def get_all_processing_data(city, start_day, end_day, down_load=False):
    stations = load_station()
    import pickle
    f1 = open(base_path_3 + city+ '_data_post.pkl', 'rb')
    data_post = pd.read_pickle(f1)
    #data_post = pickle.load(f1)
    list_data_post = list(data_post.keys())
    #print(data_post.keys())
    #print(data_post.keys()[1])
    print("data_post",data_post[list_data_post[0]])
    max_post_day = datetime_toString(data_post[list_data_post[0]]['time'].max() - timedelta(hours=23))
    # print df2
    one_day_after_max_post_day = datetime_toString(string_toDatetime(max_post_day) + timedelta(days=1))
    # data_post = data_post
    start_time = start_day + "-0"
    end_time = end_day + "-23"
    three_day_before_start_day = datetime_toString(string_toDatetime(start_day) - timedelta(days=3))
    one_day_before_end_day = datetime_toString(string_toDatetime(end_day) - timedelta(days=1))
    # one_day_before_start_day = datetime_toString(string_toDatetime(start_day)-timedelta(days=1))
    df = load_data(city=city, start_time=start_time, end_time=end_time, current_day=True)
    filename = base_path_2 + city+ "_current_day_processing.csv"
    start_time_1 = start_day + " 00:00:00"
    end_time_1 = datetime_toString(string_toDatetime(end_day) + timedelta(days=2)) + " 23:00:00"
    write_to_process(df, start_time=start_time_1, end_time=end_time_1, filename=filename)

    data_current = load_data_process(city=city, current_day=True)
    current_group = data_current.groupby("station_id")
    data_current = {}
    for station, group in current_group:
        data_current[station] = group
    # print data_post, data_history, data_current
    station_group = {}
    for station in data_post.keys():
        station_group[station] = pd.concat(
            [data_post[station][: max_post_day], data_current[station][one_day_after_max_post_day:]],
            axis=0).sort_index()  # data_history[station],
        # print data_post[station][:max_post_day]
        # print station_group[station].values.shape,
        # print max_post_day, one_day_after_max_post_day
        # print station_group[station]
    #if city == 'bj':
    #     attr_need = ["PM25_Concentration", "PM10_Concentration", "O3_Concentration", 'time_year',
    #                  'time_month', 'time_day', 'time_week', 'time_hour']
    # else:
    #     attr_need = ["PM25_Concentration", "PM10_Concentration", 'time_year', 'time_month',
    #                  'time_day', 'time_week', 'time_hour']
    attr_need = ["NO2_Concentration","NOx_Concentration",'time_year',
                    'time_month', 'time_day', 'time_week', 'time_hour']  
    between_two_point(station_group, attr_need)
    if string_toDatetime(max_post_day) >= string_toDatetime(end_day):
        pass
    else:
        pre_train(station_group, city, stations, attr_need, length=24 * 3, day=three_day_before_start_day)
    ans_post_1 = {}
    for station, group in station_group.items():
        if string_toDatetime(max_post_day) <= string_toDatetime(one_day_before_end_day):
            ans_post_1[station] = group[:one_day_before_end_day].drop_duplicates()
        else:
            ans_post_1[station] = group[:max_post_day].drop_duplicates()
    f1 = open(base_path_3 + city+ '_data_post.pkl', 'wb')
    pickle.dump(ans_post_1, f1, True)
    ans_post_2 = {}
    for station, group in station_group.items():
        ans_post_2[station] = group[
                              :datetime_toString(string_toDatetime(end_day) + timedelta(days=2))].drop_duplicates()
    return ans_post_2


def model_1(city):
    stations = load_station()
    import pickle
    f1 = open(base_path_3 + city + '_data_post.pkl', 'rb')
    data_post = pickle.load(f1)
    f2 = open(base_path_3 + city + '_data_history.pkl', 'rb')
    data_history = pickle.load(f2)
    # filename3 = base_path_2 + city + "_current_day_processing.csv"
    data_current = load_data_process(city=city, current_day=True)
    current_group = data_current.groupby("station_id")
    data_current = {}
    for station, group in current_group:
        data_current[station] = group
    # print data_post, data_history, data_current
    station_group = {}
    for station in data_history.keys():
        if city == "ld":
            if stations[city][station]["predict"] == False:
                continue
        # print data_current[station]
        station_group[station] = pd.concat([data_post[station], data_current[station]],
                                           axis=0).sort_index()  # data_history[station],
        print (station_group[station])

    if city == 'bj':
        attr_need = ["PM25_Concentration", "PM10_Concentration", "O3_Concentration", 'time_year',
                     'time_month', 'time_day', 'time_week', 'time_hour']
        attr_need2 = ["PM25_Concentration", "PM10_Concentration", "O3_Concentration",
                      "CO_Concentration", "NO2_Concentration", "SO2_Concentration", 'time_year', 'time_month',
                      'time_day', 'time_week', 'time_hour']
    else:
        attr_need = ["PM25_Concentration", "PM10_Concentration", 'time_year', 'time_month',
                     'time_day', 'time_week', 'time_hour']
        attr_need2 = ["PM25_Concentration", "PM10_Concentration",
                      "NO2_Concentration", 'time_year', 'time_month',
                      'time_day', 'time_week', 'time_hour']
    between_two_point(station_group, attr_need)
    pre_train(station_group, city, stations, attr_need, length=24 * 3)
    # print station_group
    tmp = ""
    for station, group in station_group.items():
        if station_id_change.has_key(station):
            station = station_id_change[station]
        values = group[attr_need].values
        if city == 'bj':
            values = values[-48:, :3]
            for i in range(values.shape[0]):
                tmp += station + "#" + str(i) + "," + str(values[i, 0]) + "," + str(values[i, 1]) + "," + str(
                    values[i, 2]) + "\n"
        else:
            values = values[-48:, :2]
            for i in range(values.shape[0]):
                tmp += station + "#" + str(i) + "," + str(values[i, 0]) + "," + str(values[i, 1]) + ",0.0\n"
    return tmp


#  缺失值填充入口
#TODO denne skal gøres mere dynmamik
def loss_data_process_main(pre_train_flag=True):
    stations = load_station()
    city = "Aalborg"
    #TODO pre_precessing/write_to_process skal gøre før denne function da den skal bruge filen som bliver gjørt
    df = load_data_process(city=city, current_day=False)

    process_loss_data(df, city, stations, length=24 * 3, pre_train_flag=pre_train_flag)
    analysis(df, stations, city)


'''
存储处理后的结果
filename = base_path_2 + city + "_airquality_processing.csv"
filename = base_path_2 + city + "_current_day_processing.csv"
'''

#TODO check why they both of time and splitting of time, might be it should be the same as line 160
#TODO change parameter to fit our time and cities as standard
def write_to_process(df, start_time="2020-01-14 00:00:00", end_time="2022-01-14 23:00:00",
                     filename=base_path_2 + "Aalborg_Gade_airquality_processing.csv"):
    
    df = df.drop_duplicates(["station_id", 'time_year', "time_month", "time_day", "time_hour"])
    start_day = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_day = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    dates = pd.date_range(start_day, end_day, freq='60min')
    df1 = pd.DataFrame(index=dates)
    df1['time'] = df1.index.map(lambda x: str(x))
    df1['time_week'] = df1.index.map(lambda x: x.weekday)
    df1['time_year'] = df1.index.map(lambda x: x.year)
    df1['time_month'] = df1.index.map(lambda x: x.month)
    df1['time_day'] = df1.index.map(lambda x: x.day)
    df1['time_hour'] = df1.index.map(lambda x: x.hour)
    stations_group = df.groupby("station_id")
    ans = None
    for station_id, group in stations_group:
        # if station_id == "KF1":
        #     print "test"
        # print df1.values.shape[0]
        df1['station_id'] = np.array([station_id] * df1.values.shape[0])
        # print df1
        # print "group1", group.values.shape[0]
        group_ = pd.merge(df1, group, how='left')
        # print "group2", group_.values.shape[0]
        # print group
        if ans is None:
            ans = group_
        else:
            ans = pd.concat([ans, group_], axis=0)
            # print df1.values.shape
    # print ans
    ans.to_csv(filename, index=False, sep=',')


# 预处理，去除重复的项，同时将不连续的时间修正
#TODO parameter to fit our data
#DONE changed start_day and end_day to fit our timeframe'
#DONE has parameter pos_station to separate the stations
def pre_precessing(city='Aalborg'):
    # 处理4月10号之前的数据
    start_day = "2020-01-14"
    start_time = start_day + "-0" #2017-01-01-0
    end_day = "2022-01-14"
    end_time = end_day + "-0" #2018-04-10-23
    start_time_1 = start_day + " 00:00:00"
    end_time_1 = end_day + " 23:00:00"
    
    # get_data(city, start_time, end_time)
    df = load_data(city, start_time, end_time)
    filename = base_path_2 + city + "_airquality_processing.csv"
    #TODO some days are missing a ton of timeframe data (not our mistake)
    write_to_process(df, start_time=start_time_1, end_time=end_time_1, filename=filename)

    # # 处理当天和前天的数据
    # time_now = datetime.now()
    # time_now = time_now - timedelta(hours=32)
    # time_now = time_now.strftime('%Y-%m-%d')
    # start_time = str(time_now) + "-0"
    # start_time_1 = str(time_now) + " 00:00:00"
    # time_now = datetime.now()
    # time_now = time_now - timedelta(hours=8)
    # time_now = time_now.strftime('%Y-%m-%d')
    # end_time = str(time_now) + "-23"
    # end_time_1 = str(time_now) + " 23:00:00"
    # # get_data(start_time=start_time, end_time=end_time, city=city, current_day=True)
    # df = load_data(city=city, start_time=start_time, end_time=end_time, current_day=True)
    # filename = base_path_2 + city + "_current_day_processing.csv"
    # write_to_process(df, start_time=start_time_1, end_time=end_time_1, filename=filename)


from pre_train import main as pre_main

def concatingaq():
    dfGade = pd.read_csv(base_path_1 + "Aalborg_Gade_FebTilNu.csv",sep=";",skiprows=2)
    dfTag = pd.read_csv(base_path_1 + "Aalborg_Tag_FebTilNu.csv",sep=";",skiprows=2)
    dfGade["station_id"] = "Vesterbro"
    dfTag["station_id"] = "Oesterbro"
    dfGade = dfGade[["station_id","Recorded","NO2","NOx"   
    ]]
    dfTag = dfTag[["station_id","Recorded","NO2","NOx"   
    ]]
    
    
    dfconcat = pd.concat([dfGade,dfTag],axis=0)
    dfconcat['Recorded'] = pd.to_datetime(dfconcat['Recorded'], format='%d-%m-%Y %H:%M:%S')
    dfconcat = dfconcat.sort_values(by="Recorded")
    dfconcat.to_csv(base_path_1 + "Aalborg_aq_current.csv",index=False)

#TODO pre_main is hardcoded 
#NOTE loss_data_process_main only takes aalborg atm, but it and the following function inside of it should be made more dynamic
#DONE pre_precessing and loss_data_process_main function work with aalborg data
#NOTE remember to run pre_precessing and loss_data_process_main to get the files needed
if __name__ == '__main__':
    # analysis_station()
    #concatingaq()
    '''
    预处理，去除重复的项，同时将不连续的时间修正
    '''
    #pre_precessing(city="Aalborg")

    '''
    缺失数据处理
    训练模型 前三天预测后一个值
    利用模型预测对缺失数据进行填充
    '''
    #loss_data_process_main(pre_train_flag=True)
    #pre_main("Aalborg")
    loss_data_process_main(pre_train_flag=False)

    '''
    获取全部的数据
    利用前三预测后一个值来提交结果，迭代预测
    '''
    #post_data(city="Aalborg")
    #post_data(city="Aalborg",pos_station="Tag")
    # post_data(city="bj")
    #     model_1(city='bj')
    # post_data(city="ld")
    #     model_1(city='ld')

    # ans = "test_id,PM2.5,PM10,O3\n"
    # ans1 = model_1(city="bj")
    # ans2 = model_1(city="ld")
    # ans_file = base_path_3 + "ans.csv"
    # f_to = open(ans_file, 'wb')
    # f_to.write(ans + ans1 + ans2)
    # f_to.close()
    # city = 'bj'
    # df = load_data_process(city=city)
    # for station, group in df.groupby("station_id"):
    #     print station, group.values.shape
    # # print df.values.shape
    
    # city = 'ld'
    # df = load_data_process(city=city)
    # for station, group in df.groupby("station_id"):
    #     print station, group.values.shape
    # print df.values.shape
