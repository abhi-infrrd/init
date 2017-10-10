# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

import numpy
import pandas as pd
import re
import nltk


def populateRecomendations():
    data = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt", sep="\t", quoting=3)
    data = data.iloc[:, [5, 6, 14, 15]]

    #nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    for j in ['Type', 'AllFieldOfStudy', 'Topic', 'Keywords']:
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
        for j in ['AllFieldOfStudy', 'Topic', 'Keywords']:
            data['Type'][i] = numpy.append(data['Type'][i], data[j][i])

    # remove the unwanted columns
    data = data.iloc[:, 0]

    # create the correlation matrix
    import scipy.stats

    cormatrix = numpy.zeros([len(data), len(data)], tuple)
    for rows in range(len(data)):
        for cols in range(len(data)):
            cormatrix[rows][cols] = scipy.stats.pearsonr(data[rows], data[cols])

    return cormatrix


# when p value is more add it to the related items list
def getRecomendation(cormatrix, productCode, NoOfValues=5, p_value=0.0):
    itemIndex = getIndexOfProductId(str(productCode))
    data = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt", sep="\t", quoting=3)
    productIds = data.iloc[:, [0, 5, 6, 11, 12, 14, 15]]

    relatedItems = list()
    for items in range(len(cormatrix)):
        if (cormatrix[itemIndex][items][1] >= p_value):
            relatedItems.append([cormatrix[itemIndex][items][0],items,productIds.iloc[items, :], str(productCode)])

    # sort it in the highest similarity
    relatedItems.sort(reverse=True)

    return relatedItems #returning everything, not just 5 records


def getIndexOfProductId(productCode='PC-006616'):
    data = pd.read_csv("C:\\Users\\user\\Desktop\\test_panda\\Products_09202017.txt", sep="\t", quoting=3)
    productIds = data.iloc[:, [0]]
    result=''
    for item in range(len(productIds)):
        if (productIds['ProductCode'][item] == productCode):
            result = item
            break

    return result


#cormatrix = populateRecomendations()
#finaldata = getRecomendation(cormatrix, 'PC-006616', 5, 0.7)

#l = []
#print(finaldata[0][2].to_dict())
#k = len(finaldata)
#for i in range(k):
#    l.append(finaldata[i][2].to_dict())
#print(type(l[0]))
#import json
#json.dumps(l)
#print(type(l))