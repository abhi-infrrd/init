# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

import os
os.chdir('C:\\Users\\user\\Desktop\\test_panda')

itemIndex = 0
p_value = 0.97

import numpy
import pandas as pd

data = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt", sep="\t", quoting=3)
productIds = data.iloc[:, [0, 1, 2]]
data = data.iloc[:, [3, 4, 5, 6, 14]]

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

for j in ['Title', 'Description', 'Type', 'AllFieldOfStudy', 'Topic']:
    for i in range(len(data)):
        data[j][i] = re.sub('[^a-zA-Z]', ' ', str(data[j][i]))
        data[j][i] = str(data[j][i]).lower()
        data[j][i] = data[j][i].split()
        ps = PorterStemmer()
        data[j][i] = [ps.stem(word) for word in data[j][i] if not word in set(stopwords.words('english'))]
        data[j][i] = ' '.join(data[j][i])

    cv = CountVectorizer(max_features=100)
    x = cv.fit_transform(data[j]).toarray()

    for i in range(len(x)):
        data[j][i] = x[i]

# combine the  columns
for i in range(len(x)):
    for j in ['Description', 'Type', 'AllFieldOfStudy', 'Topic']:
        data['Title'][i] = numpy.append(data['Title'][i], data[j][i])

# remove the unwanted columns
data = data.iloc[:, 0]

# create the correlation matrix
import scipy.stats

print(scipy.stats.pearsonr(data[0], data[1]))

cormatrix = numpy.zeros([len(data), len(data)], tuple)
for rows in range(len(data)):
    for cols in range(len(data)):
        cormatrix[rows][cols] = scipy.stats.pearsonr(data[rows], data[cols])

# when p value is more add it to the related items list
relatedItems = list()
for items in range(len(cormatrix)):
    if (cormatrix[itemIndex][items][1] >= p_value):
        relatedItems.append([cormatrix[itemIndex][items][0], items])

# sort it in the highest similarity
relatedItems.sort(reverse=True)
for item in relatedItems:
    # get the index from the relatedItems and find the corresponding poductIds
    print(productIds.iloc[item[1], :])
