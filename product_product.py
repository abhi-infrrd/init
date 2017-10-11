import numpy
import pandas as pd
import re
import nltk

Originaldata = pd.read_csv("./Products_09202017.txt", sep="\t", quoting=3)


def populateRecomendations():
    # Get only the portion of the data that is required
    global Originaldata
    data = pd.DataFrame(Originaldata)
    data = data.iloc[:, [5, 6, 14, 15]]

    # Downloading stopwords list
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    # From all the columns take only the alphabets, lowercase it and stem it out
    for j in ['Type', 'AllFieldOfStudy', 'Topic', 'Keywords']:
        for i in range(len(data)):
            data[j][i] = re.sub('[^a-zA-Z]', ' ', str(data[j][i]))
            data[j][i] = str(data[j][i]).lower()
            data[j][i] = data[j][i].split()
            ps = PorterStemmer()
            data[j][i] = [ps.stem(word) for word in data[j][i] if not word in set(stopwords.words('english'))]
            data[j][i] = ' '.join(data[j][i])

        # Vectorize the data in each column
        cv = CountVectorizer(max_features=100)
        x = cv.fit_transform(data[j]).toarray()

        # Add it back to the dataframe
        for i in range(len(x)):
            data[j][i] = x[i]

    # combine the  columns and put it in 'AllFieldOfStudy
    for i in range(len(x)):
        for j in ['AllFieldOfStudy', 'Topic', 'Keywords']:
            data['Type'][i] = numpy.append(data['Type'][i], data[j][i])

    # remove the unwanted columns other than 'AllFieldOfStudy
    data = data.iloc[:, 0]

    # create the correlation matrix
    import scipy.stats

    cormatrix = numpy.zeros([len(data), len(data)], tuple)
    for rows in range(len(data)):
        for cols in range(len(data)):
            cormatrix[rows][cols] = scipy.stats.pearsonr(data[rows], data[cols])

    # return the correlation matrix
    return cormatrix

# Gets the Recomendations as a list of dictionaries
# input is the correlation matrix, number of values needed and the p-values
def getRecomendation(cormatrix, productCode, NoOfValues=100, p_value=0.0):

    # Gets the index of the productCode
    itemIndex = getIndexOfProductId(str(productCode))
    # Gets the original data and keeps only the required data
    global Originaldata
    data = pd.DataFrame(Originaldata)
    productIds = data.iloc[:, [0, 1, 5, 6, 11, 12, 14, 15]]

    # Populate the list of data from the correlation matrix
    try:
        relatedItems = list()
        for items in range(len(cormatrix)):
            if cormatrix[itemIndex][items][1] >= p_value:
                if productIds.iloc[items, 0] != productCode:
                    relatedItems.append([
                        cormatrix[itemIndex][items][0],
                        productIds.iloc[items, 0],
                        productIds.iloc[items, 1],
                        productIds.iloc[items, 2],
                        productIds.iloc[items, 3],
                        productIds.iloc[items, 4],
                        productIds.iloc[items, 5],
                        productIds.iloc[items, 6],
                        productIds.iloc[items, 7],
                        str(productCode)
                    ])

    except:
        raise KeyError('Product Code does not exist', productCode)

    # sort it in the highest similarity
    relatedItems.sort(reverse=True)

    result = list()
    for iterator in range(len(relatedItems)):
        result.append({
            "score": relatedItems[iterator][0],
            "ProductCode": relatedItems[iterator][1],
            "SkuCode": relatedItems[iterator][2],
            "Type": relatedItems[iterator][3],
            "AllFieldOfStudy": relatedItems[iterator][4],
            "Topic": relatedItems[iterator][5],
            "Keywords": relatedItems[iterator][6]
        })

    if NoOfValues <= 0:
        return result  # returning everything, not just 5 records
    else:
        return result[:NoOfValues]


def getIndexOfProductId(productCode):
    global Originaldata
    result = ''
    try:
        data = pd.DataFrame(Originaldata)
        productIds = data.iloc[:, 0]

        for item in range(len(productIds)):
            if productIds[item] == productCode:
                result = item
                break
    except:
        raise KeyError('Product Code does not exist', productCode)
    return result


cormatrix = populateRecomendations()
finaldata = getRecomendation(cormatrix, 'PC-006616')
print(finaldata)
