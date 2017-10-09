# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:55:12 2017

@author: Abhishek
"""
import os
os.chdir('C:\\Users\\user\\Desktop\\test_panda') #harcoded
import Recommender as rc
import pandas as pd
from scipy.spatial.distance import cosine
from collections import OrderedDict

data = ''

d1 = ''

def preprocess_data():
    
    global data
    
    data = rc.read_a_file_to_dataframe("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt",'\t') #harcoded

    columns = [0,1,2,3,4,5,13,14,15] #harcoded

    global d1

    d1 =rc.filter_a_list_of_columns(data,columns)

    d1.columns = d1.iloc[0]

    d1.drop(d1.index[[0,0]], inplace=True)

    d1 = rc.drop_null_rows(d1)
    


def tf_idf_proceessing(attribute):
    
    global d1
    
    x,v = rc.proc_an_attribute(d1,attribute)
    arr = v.get_feature_names()
    
    rc.write_attributes_to_a_file('desc.txt',arr) #harcoded
    rc.write_values_to_a_file('desc.txt',list(x.toarray())) #harcoded

    data_frame_temp  = rc.read_a_file_to_dataframe("C:\\Users\\user\\Desktop\\test_panda\\desc.txt",'\t') #harcoded
    data_frame_temp.columns = data_frame_temp.iloc[0]
    data_frame_temp.drop(data_frame_temp.index[[0,0]], inplace=True)
    
    d1.reset_index(drop=True, inplace=True)
    
    frames = [d1,data_frame_temp]

    d1 = rc.concat_a_list_of_dataframes(frames)

    del d1[attribute]
def one_hot_encode_processing(attribute):
    
    global d1
    
    d1 = rc.one_hot_encoding(d1,attribute)
    


#d1.to_csv('D:\\prod_data\prod.txt', sep='\t')
#d1.iloc[:,3:].to_csv('D:\\prod_data\k.txt', sep='\t') #filtered columns to find correlation with


def initialise():
    preprocess_data()    

    tf_idf_proc_list = ['Keywords','Topic','Title','Description'] #harcoded

    one_hot_encode_list = ['Type','PriceRange'] #harcoded

    for i in tf_idf_proc_list:
        tf_idf_proceessing(i)
    for i in one_hot_encode_list:
        one_hot_encode_processing(i)
    global d1
    d1 = d1.convert_objects(convert_numeric=True)#There's an issue of SkuCode turing into nan
    d1=d1.dropna(axis=1,how='all')
    global data
    data.columns = data.iloc[0]
    data = data.loc[data.ProductCode != 'ProductCode']
    
def recommend():
    global d1
    product_code = input("Enter a product code")
    record = d1.loc[d1['ProductCode'] == product_code]
    record = record.iloc[:1,3:]
    #d1 = d1[d1.ProductCode != product_code]
    return record
def cos_recommendation():
    global d1
    record = recommend()
    #f = open('cos.txt','w')
    l = []
    loop = len(d1.index)
    for i in range(loop+2):
        try:
            k = 1-cosine(record,d1.iloc[i:i+1,3:])
            l.append(k)
            #f.write(str(k))
            #f.write('\n')
        except:
            break
    #f.close()
    mapping  = d1.iloc[:,:1]

    df = pd.DataFrame(l,columns=['rating'])

    f = rc.concat_a_list_of_dataframes([df,mapping])

    dic = f.set_index('ProductCode').T.to_dict()
    ordered = OrderedDict(sorted(dic.items(), key=lambda i: i[1]['rating']))
    l1 =[]
    k = ordered.keys()
    for i in k:
        l1.append(i)
    
    l2 =[]
    k = ordered.values()
    for i in k:
        l2.append(i['rating'])
    f = open('a.txt','w')
    for i,j in zip(reversed(l1),reversed(l2)):
        f.write(str(i))
        f.write('\t')
        f.write(str(j))
        f.write('\n')
    f.close()

    f = open('a.txt','r')
    l =[]
    for i in f:
        l.append(i)
    num = int(input('Enter the number of similar products you want to see'))

    final_list = []

    for i in l:
        k = i.split('\t')
        final_list.append(k[0])
    global data
    for i in range(num):
        temp = data.loc[data['ProductCode'] == final_list[i]]
        print(temp.iloc[:,:1])
initialise()
cos_recommendation()