# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:55:12 2017

@author: Abhishek
"""
import Recommender as rc
import pandas as pd
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
        d1 = d1.fillna(d1[i].value_counts().index[0])

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
        
    global cos_similarity, d1
    
    cos_similarity = cosine_similarity(d1.iloc[:,3:])
    
def cos_recommendation(product_code):
    global d1
    record = d1.loc[d1['ProductCode'] == product_code]
    if(len(record.index)==0):
        raise NoRecordFoundException('No record for the given product-code')
    data.reset_index(drop=True, inplace=True)
    df  = data.loc[data['ProductCode'] == product_code]
    df = df.iloc[:1,:]
    indc  = ((df.index).tolist())[0]

    temp = cos_similarity[indc]

    data['score'] = temp 

    data.sort_values('score',ascending=False, inplace=True)
    
    finaldata = data.iloc[:,:]# slice to limit the number of rows to return as output
    
    finaldata = finaldata.loc[data.ProductCode != product_code]
    
    finaldata = finaldata.drop_duplicates('ProductCode',keep='first')
    
    finaldata = finaldata.ix[:,[0, 1, 5, 6, 11, 12, 14, 15,16]]
    
    return (list(finaldata.T.to_dict().values()))

#initialise()
#l = cos_recommendation('PC-005102')
