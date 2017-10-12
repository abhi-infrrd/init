# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:55:12 2017

@author: Abhishek
"""
import os
os.chdir("C:\\Users\\user\\Desktop\\recommender-infrrd-10-11-2017\\init")
import Recommender as rc
import pandas as pd
from scipy.spatial.distance import cosine
from collections import OrderedDict
data = ''

d1 = ''
class NoRecordFoundException(Exception):
    pass
def preprocess_data():
    
    global data
    
    data = rc.read_a_file_to_dataframe("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt",'\t') 
    
    columns = [0,1,2,3,4,5,13,14,15]

    global d1

    d1 =rc.filter_a_list_of_columns(data,columns)

    d1.columns = d1.iloc[0]

    d1.drop(d1.index[[0,0]], inplace=True)
    
    data.columns = data.iloc[0]
    
    data.drop(data.index[[0,0]], inplace=True)
    
    l = ['Keywords','Topic','Title','Description','Type','PriceRange'] 

    for i in l:    
        d1 = d1.fillna(d1['PriceRange'].value_counts().index[0])
        
    #d1 = rc.drop_null_rows(d1)
    
    


def tf_idf_proceessing(attribute):
    
    global d1
    
    x,v = rc.proc_an_attribute(d1,attribute)
    arr = v.get_feature_names()
       
    data_frame_temp  = pd.DataFrame(x.toarray(), columns = arr) 
    #data_frame_temp.columns = data_frame_temp.iloc[0]
    #data_frame_temp.drop(data_frame_temp.index[[0,0]], inplace=True)
    
    del d1[attribute]
    
    frames = [d1,data_frame_temp]

    d1 = rc.concat_a_list_of_dataframes(frames)
    
def one_hot_encode_processing(attribute):
    
    global d1
    
    d1 = rc.one_hot_encoding(d1,attribute)

def initialise():
    preprocess_data()    

    tf_idf_proc_list = ['Keywords','Topic','Title','Description']

    one_hot_encode_list = ['Type','PriceRange'] 

    for i in tf_idf_proc_list:
        tf_idf_proceessing(i)
    for i in one_hot_encode_list:
        one_hot_encode_processing(i)
    #global d1
    #d1 = d1.convert_objects(convert_numeric=True)#There's an issue of SkuCode turing into nan
    #d1=d1.dropna(axis=1,how='all')
    global data
    #data.columns = data.iloc[0]
    data = data.loc[data.ProductCode != 'ProductCode'] #chnaging global varibale, neagtive effects
    
def recommend(product_code):
    global d1
    #product_code = input("Enter a product code")
    record = d1.loc[d1['ProductCode'] == product_code]
    if(len(record.index)==0):
        raise NoRecordFoundException('No record for the given product-code')
    record = record.iloc[:1,3:]
    return record
def cos_recommendation(product_code,num = 5):
    global d1
    record = recommend(product_code)
    l = []
    loop = len(d1.index)
    for i in range(loop+2):
        try:
            k = 1-cosine(record,d1.iloc[i:i+1,3:])
            l.append(k)
        except:
            break
    mapping  = d1.iloc[:,:1]

    df = pd.DataFrame(l,columns=['rating'])

    f = rc.concat_a_list_of_dataframes([df,mapping])

    dic = f.set_index('ProductCode').T.to_dict()
    ordered = OrderedDict(sorted(dic.items(), key=lambda i: i[1]['rating']))
    l1 =[]
    k = ordered.keys()
    for i in k:
        l1.append(i)
    l1.reverse()
    #num = int(input('Enter the number of similar products you want to see'))
    global data
    l=[]
    for i in range(num):
        temp = data.loc[data['ProductCode'] == l1[i]]
        l.append(temp.iloc[:,:])
        print(temp.iloc[:,:1]) #CHANGE SECOND SLICE TO GET MORE COLUMNS
    return l
initialise()
l = cos_recommendation('PC-006617')
print(l[0].iloc[:,:2])

preprocess_data()  

#def f(x):
#    if x.count()<=0:
#        return 
#    return x.value_counts().index[0]

#d1['Keywords'] = d1.groupby('Keywords')['Keywords'].transform(f)

#d1['Keywords'] = d1['Keywords'].fillna(d1['Keywords'].value_counts().idxmax())  

#print(d1[d1.isnull().any(axis=1)])

#d1.reset_index(drop=True, inplace=True)
#x = d1.groupby(['ProductCode']).agg(lambda x:x.value_counts())
#print(x.loc['ProductCode'])

data.columns = data.iloc[0]
data.drop(data.index[[0,0]], inplace=True)

#d1 = data.iloc[:,15:]

#x = d1.mode(axis=1)

#import numpy as np
#data = data.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('', np.NaN)

#data = data.apply(lambda x: x.str.strip()).replace('', np.nan)

#print(data.iloc[:1,15:])

#data.fillna('', inplace=True)

#k= data.iloc[:1,15:]

#k = k.iloc[::].as_matrix()
#print(typek[0])

#print(data.isnan())
#data['Keywords'].apply(lambda x:float(x))
#from sklearn.preprocessing import Imputer
#imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)
#imp.fit_transform(d1)

#d1 = d1.max(axis=1, skipna=True)
#d1 = d1.dropna()

#tf_idf_proc_list = ['Keywords','Topic','Title','Description']

#one_hot_encode_list = ['Type','PriceRange'] 

#print(d1['Keywords'])

#for i in tf_idf_proc_list:
#        tf_idf_proceessing(i)
#k =pd.get_dummies(data['Type'])

#print(d1.iloc[:1,:])

