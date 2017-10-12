# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:36:01 2017

@author: Abhishek 
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
def read_a_file_to_dataframe(file_name,separator):
    return pd.read_csv(file_name,sep = separator, header=None)

def filter_a_list_of_columns(dataframe,list_of_columns):
    return pd.DataFrame(dataframe,columns = list_of_columns)    

def drop_null_rows(dataframe):
    return dataframe.dropna()

def proc_an_attribute(dataframe,attribute): 
    v = TfidfVectorizer(analyzer='word',stop_words = 'english')
    x = v.fit_transform(dataframe[attribute].values.astype('str'))
    return x,v
    
def write_attributes_to_a_file(file_name,array_of_feature_names):
    f = open(file_name,'w')
    for i in array_of_feature_names:
        f.write(i+'\t')
    f.write('\n')
    f.close()
    
def write_values_to_a_file(file_name,list_of_array_of_values):
    f = open(file_name,'a')
    for i in list_of_array_of_values:
        for z in i:
            f.write(str(z)+'\t')
        f.write('\n')
    f.close()
    
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
    