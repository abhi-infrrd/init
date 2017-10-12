# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:59:08 2017

@author: Abhishek
"""

#change working directory
import os
os.chdir("C:\\Users\\user\\Desktop\\recommender-infrrd-10-11-2017\\init")

import pandas as pd

#read data
data = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt",sep = '\t', header=None)

#filter concerned columns on which manipulation is to happen(along with some identifiers)
columns = [0,1,2,3,4,5,13,14,15]

#filtered data
d1 = pd.DataFrame(data,columns = [0,1,2,3,4,5,13,14,15])

#first row as columns' name and drop first row
d1.columns = d1.iloc[0]
d1.drop(d1.index[[0,0]], inplace=True)

data.columns = data.iloc[0]
data.drop(data.index[[0,0]], inplace=True)

l = ['Keywords','Topic','Title','Description','Type','PriceRange'] 

for i in l:    
    d1 = d1.fillna(d1['PriceRange'].value_counts().index[0])

#data as array
#x = d1.iloc[:,[8]].values

#d1 = d1.dropna()
tf_idf_proc_list = ['Keywords','Topic','Title','Description']

one_hot_encode_list = ['Type','PriceRange']

for i in tf_idf_proc_list:
    from nltk.corpus import stopwords
    stops = set(stopwords.words("english"))
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(analyzer='word',stop_words = 'english',max_features=400 )

    x = v.fit_transform(d1[i].values.astype('str'))

    df = pd.DataFrame(x.toarray(), columns=v.get_feature_names())

    import Recommender as rc
    d1.reset_index(drop=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    d1 = rc.concat_a_list_of_dataframes([d1,df])

    del d1[i]
for i in one_hot_encode_list:
    one_hot = pd.get_dummies(d1[i])
    d1.reset_index(drop=True, inplace=True)
    one_hot.reset_index(drop=True, inplace=True)
    d1 = pd.concat([d1,one_hot], axis=1)
    del d1[i]
print(d1.iloc[:1,:])



f = open('desc.txt','w')

arr = v.get_feature_names()
for i in arr:
    f.write(i+'\t')
f.write('\n')

arr = list(x.toarray())
print(arr)

for i in arr:
    print(i)
    for z in i:
        f.write(str(z)+'\t')
    f.write('\n')

d1['Description'] = list(x.toarray())

x = v.fit_transform(d1['Topic'])
d1['Topic'] = list(x.toarray())

x = v.fit_transform(d1['Keywords'])
d1['Keywords'] = list(x.toarray())

x = v.fit_transform(d1['Title'])
d1['Title'] = list(x.toarray())

one_hot = pd.get_dummies(d1['PriceRange'])
d1 = d1.drop('PriceRange',axis=1)
d1 = d1.join(one_hot)

one_hot = pd.get_dummies(d1['Type'])
d1 = d1.drop('Type',axis=1)
d1 = d1.join(one_hot)

d1.to_csv("test.txt", sep='\t', encoding='utf-8')

df = d1.as_matrix()

print(df[0])

t = df[0]

for i in t:
    print(i)
record_to_test = d1['ProductCode'].values[0]

d1.corr().iloc[3,:]
d1.corrwith(d1)

print(d1['Keywords'])




data_frame_to_append_1  = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\desc.txt",sep = '\t', header=None)

data_frame_to_append_1.columns = data_frame_to_append_1.iloc[0]
data_frame_to_append_1.drop(data_frame_to_append_1.index[[0,0]], inplace=True)

del d1[4]


d1.reset_index(drop=True, inplace=True)
data_frame_to_append_1.reset_index(drop=True, inplace=True)
frames = [d1,data_frame_to_append_1]

d1 = pd.concat(frames, axis=1)


print(d1['Keywords'])





















#k = 1

#master_set_8 = set()

#while True:
#    try:
#        temp = (x[k][0].split(','))
#        
#        for i in temp:    
#            i = i.split(' ')
#            for z in i:
#                master_set_8.add(z)
#        
#        k = k + 1
#    except:
#        f = open("test.txt",'a')
#        f.write(str(k)+"breaking off")
#        break
#s = pd.Series(list(master_set_8))

#df = pd.DataFrame(columns = list(master_set_8))
