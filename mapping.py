# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:50:07 2017

@author: user
"""

import os
os.chdir('C:\\Users\\user\\Desktop\\test_panda') 
import Recommender as rc
import json
data = rc.read_a_file_to_dataframe("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt",'\t') 
data.columns = data.loc[0]

data.drop(data.index[[0,0]], inplace=True)

verify1 = data['SkuID'].as_matrix().flat

col1 = data.iloc[:,:1]
col2 = data.iloc[:,2:3]

col1 = col1.as_matrix()
col2 = col2.as_matrix()

col1 = col1.flat
col2 = col2.flat

dictionary = dict(zip(col2, col1))

json.dump(dictionary, open("mappnig.txt",'w'))

data = rc.read_a_file_to_dataframe("C:\\Users\\user\\Desktop\\test_panda\\ProdOrderSummary_09202017.txt",'\t') 

data.columns = data.iloc[0]

data.drop(data.index[[0,0]], inplace=True)

verify2 = data['SkuID'].as_matrix().flat


print(set(verify1) == set(verify2))

data['SkuID'] = data['SkuID'].map(dictionary)

print(len(data.index))

print(data.iloc[[1]])

for i in dictionary.values():
    print(i)