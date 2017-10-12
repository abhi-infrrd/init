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
from sklearn.metrics.pairwise import cosine_similarity
data = ''

d1 = ''

cos_similarity = ''
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

def tf_idf_proceessing(attribute):
    
    global d1
    
    x,v = rc.proc_an_attribute(d1,attribute)
    
    arr = v.get_feature_names()
       
    data_frame_temp  = pd.DataFrame(x.toarray(), columns = arr) 
    
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
    #global data
    
    #data = data.loc[data.ProductCode != 'ProductCode'] #changing global varibale, neagtive effects
    global cos_similarity, d1
    
    cos_similarity = cosine_similarity(d1.iloc[:,3:])
    
def cos_recommendation(product_code, data = data):
    global d1
    record = d1.loc[d1['ProductCode'] == product_code]
    if(len(record.index)==0):
        raise NoRecordFoundException('No record for the given product-code')
    data.reset_index(drop=True, inplace=True)
    df  = data.loc[data['ProductCode'] == product_code]
    df = df.iloc[:1,:]
    indc  = ((df.index).tolist())[0]

    temp = cos_similarity[indc]

    data['rating'] = temp 

    data.sort_values('rating',ascending=False, inplace=True)
    
    return data
#initialise()
#l = cos_recommendation('PC-005102',data = data)
#print(l.loc[:10,['rating']])
#print(data.iloc[:10,:4])
#del data['rating']
#for i in range(len(cos_similarity[0])):

#df  = data.loc[data['ProductCode'] == 'PC-006624']
#df = df.iloc[:1,:]
#indc  = ((df.index).tolist())[0]

#temp = cos_similarity[indc]

#data['rating'] = temp 

#print(data['rating'])

#data.sort_values(['rating'], ascending=[False])

#k = data

#del k['rating']
#print(type(((df.index).tolist())[0]))
#k = cos_similarity[0,:]
#print(type(cos_similarity[0,:]))
#print(sort(cos_similarity[0][i]))
#l = cos_recommendation('PC-005102',num = 100)
#print(l[0].iloc[:,:2])
 

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

#data.columns = data.iloc[0]
#data.drop(data.index[[0,0]], inplace=True)

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

