# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

# The Id is not unique so i am using the index  of the product
# set the index at the bottom
# Lists the items in decreasing order of similarity
# find the closest elements provide the index

import numpy
import pandas as pd

Originaldata = pd.read_csv("./Courses_09202017.txt", sep="\t", quoting=3, encoding='UTF-16')


def populateCourseRecomendations():
    global Originaldata
    data = pd.DataFrame(Originaldata)
    data = data.iloc[:, [8, 11, 18]]

    import re
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    for j in ['AllFieldOfStudy', 'Topic', 'Keywords']:
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
        for j in ['Topic', 'Keywords']:
            data['AllFieldOfStudy'][i] = numpy.append(data['AllFieldOfStudy'][i], data[j][i])

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
def getCourseRecomendation(cormatrix, courseCode, NoOfValues=100, p_value=0.0):
    itemIndex = getIndexOfCourseId(str(courseCode))
    global Originaldata
    data = pd.DataFrame(Originaldata)
    courseIds = data.iloc[:, [3, 1, 5, 6, 14, 15, 16]]

    try:
        relatedItems = list()
        for items in range(len(cormatrix)):
            if cormatrix[itemIndex][items][1] >= p_value:
                if courseIds.iloc[items, 0] != courseCode:
                    relatedItems.append([
                        cormatrix[itemIndex][items][0],
                        str(courseCode),
                        courseIds.iloc[items][0],
                        courseIds.iloc[items][1],
                        courseIds.iloc[items][2],
                        courseIds.iloc[items][3],
                        courseIds.iloc[items][4],
                        courseIds.iloc[items][5],
                        courseIds.iloc[items][6]
                    ])

    except:
        raise KeyError('Course Code does not exist', courseCode)

    # sort it in the highest similarity

    relatedItems.sort(reverse=True)

    result = list()
    for iterator in range(len(relatedItems)):
        result.append({
            "score": relatedItems[iterator][0],
            "CourseCode": relatedItems[iterator][2],
            "CourseSkuCode": relatedItems[iterator][3],
            "Title": relatedItems[iterator][4],
            "Description": relatedItems[iterator][5],
            "Image": relatedItems[iterator][6],
            "EventStartDate": relatedItems[iterator][7],
            "EventEndDate": relatedItems[iterator][8],
        })

    if NoOfValues is None:
        return result  # returning everything, not just 5 records
    else:
        return result[:100]


def getIndexOfCourseId(courseCode):
    global Originaldata
    result = ''
    try:
        data = pd.DataFrame(Originaldata)
        courseIds = data.iloc[:, 3]

        for item in range(len(courseIds)):
            if courseIds[item] == courseCode:
                result = item
                break
    except:
        raise KeyError('Course Code does not exist', courseCode)
    return result


cormatrix = populateCourseRecomendations()
finaldata = getCourseRecomendation(cormatrix, 'AAB0512', )
print(finaldata)
#print(finaldata)
#cormatrix1 = populateCourseRecomendations()
#finaldata = getCourseRecomendation(cormatrix1, 'PC-150024' )


#cormatrix1 = populateCourseRecomendations()
#finaldata = getCourseRecomendation(cormatrix1, 'PC-150024', 5, 0.7)
#l = []
#k = len(finaldata)
#for i in range(k):
#    l.append(finaldata[i][2].to_dict())
#print(l[0])
#l[0]['rItemId'] = l[0]['ProductCode']
#print(finaldata[0][2].to_dict())
#k = len(finaldata)
#for i in range(k):
#    l.append(finaldata[i][2].to_dict())
#print(type(l[0]))
#import json
#json.dumps(l)
#print(type(l))
#data = pd.read_csv("./Products_09202017.txt", sep="\t", quoting=3)
#print(data.iloc[:1,:])

#print(finaldata[4][0])
#print(finaldata[2][0])
#print(type(finaldata[2][2].to_dict()))
#Originaldata = pd.read_csv("./Courses_09202017.txt", sep="\t", quoting=3, encoding='UTF-16')
#data = pd.DataFrame(Originaldata)
#courseIds = data.iloc[:, [0, 1,3, 5, 6, 14, 15, 16]]