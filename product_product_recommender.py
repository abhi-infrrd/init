# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:36:01 2017

@author: Abhishek 
"""
import os
os.chdir("C:\\Users\\user\\Desktop\\recommender-infrrd-10-11-2017\\init")

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
def read_a_file_to_dataframe(file_name,separator):
    return pd.read_csv(file_name,sep = separator, header=None)

def filter_a_list_of_columns(dataframe,list_of_columns):
    return pd.DataFrame(dataframe,columns = list_of_columns)    

def proc_an_attribute(dataframe,attribute): 
    v = TfidfVectorizer(analyzer='word',stop_words = 'english')
    x = v.fit_transform(dataframe[attribute].values.astype('str'))
    return x,v
    
def one_hot_encoding(dataframe,attribute):
    one_hot = pd.get_dummies(dataframe[attribute])
    del dataframe[attribute]
    dataframe.reset_index(drop=True, inplace=True)
    one_hot.reset_index(drop=True, inplace=True)
    dataframe = pd.concat([dataframe,one_hot], axis=1)
    return dataframe

def concat_a_list_of_dataframes(list_of_dataframes):
    for i in list_of_dataframes:
        i.reset_index(drop=True, inplace=True)
    return pd.concat(list_of_dataframes, axis=1)
    