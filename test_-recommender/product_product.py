"""
Created on Tue Oct 10 17: 04:00 2017
@author : Anandu
#This script produces the product-product recommendation.
"""
import numpy
import pandas as pd
import pickle
import logging
import io
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Load data in the memory
logger.info("Loading the products_09202017 file ")
originaldata = pd.read_csv(io.open(config.product_file["file_name"], encoding=config.product_file["encoding"]),
                           sep="\t", quoting=3)
originaldata = pd.DataFrame(originaldata.drop_duplicates('ProductCode'))
originaldata = originaldata.reset_index()

dataForRecomendation = pd.DataFrame(originaldata)
dataForRecomendation = dataForRecomendation.loc[:,
                       ['ProductCode', 'SkuCode', 'Type', 'AllFieldOfStudy', 'EventStartDate',
                        'EventEndDate']]

cormatrix = None


#  The initial method which should be called only once
#  Unpickles or populates the model in memory
def init():
    logger.info("Initiating product product recomender")
    # unpickle
    try:
        logger.debug("Unpickling")
        pkl_file = open('product_pickled_data.pkl', 'rb')
        global cormatrix
        cormatrix = pickle.load(pkl_file)
        pkl_file.close()
    except Exception as e:
        logger.warn("No data found while unpickling, training new model " + str(e))
        # if no pickle present the populate and unpickle again
        populateRecomendations()
        init()


def populateRecomendations():
    logger.info("Product product recommendation model training started")
    import re
    import nltk
    # Downloading stopwords list
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    # Get only the portion of the data that is required
    global originaldata
    data = pd.DataFrame(originaldata)
    data = data.loc[:, ['Type', 'AllFieldOfStudy', 'Topic', 'Keywords']]

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
    data = data.loc[:, 'Type']

    # create the correlation matrix
    import scipy.stats

    # create the correlation matrix
    cormatrix = numpy.zeros([len(data), len(data)], tuple)
    for rows in range(len(data)):
        for cols in range(len(data)):
            cormatrix[rows][cols] = scipy.stats.pearsonr(data[rows], data[cols])

    logger.info("Product product recommendation training completed, pickling")

    output = open('product_pickled_data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(cormatrix, output)
    output.close()
    # return the correlation matrix
    return cormatrix


# Gets the recommendations for the courseCode provides from the correlation matrix created earlier.
# By default 100 courses are recommended but it can be altered by setting the NoOfValues param
# The p=value can also be set. But when p-value is set the Number of recommendations may be less than NoOFValues
def getRecomendation(product_code, no_of_rows=100, p_value=0.0):
    # Gets the original data and keeps only the required data
    logger.debug("Getting product product recommendation")

    global dataForRecomendation

    # Gets the index of the productCode
    item_index = ''
    try:
        product_codes = dataForRecomendation.loc[:, 'ProductCode']
        for item in range(len(product_codes)):
            if product_codes[item] == product_code:
                item_index = item
                break
    except:
        logger.error('Product Code does not exist', product_code)
        raise Exception("Product Code does not exist")

    global cormatrix
    # Populate the list of data from the correlation matrix
    try:
        related_items = list()
        for items in range(len(cormatrix)):
            if cormatrix[item_index][items][1] >= p_value:
                if dataForRecomendation.iloc[items, 0] != product_code:
                    related_items.append([
                        cormatrix[item_index][items][0],
                        dataForRecomendation.iloc[items, 0],
                        dataForRecomendation.iloc[items, 1],
                        dataForRecomendation.iloc[items, 2],
                        dataForRecomendation.iloc[items, 3],
                        dataForRecomendation.iloc[items, 4],
                        dataForRecomendation.iloc[items, 5]
                    ])

    except:
        logger.error('Product Code does not exist')
        raise Exception("Product Code does not exist")

    # sort it in the highest similarity
    related_items.sort(reverse=True)

    result = list()
    for iterator in range(len(related_items)):

        # split AllFieldOfStudy into a list

        FOS = related_items[iterator][4]
        FOS_array = []
        if FOS != numpy.nan or FOS != 'None':
            FOS = str(FOS).replace(';', ',')
            fields = str(FOS).split(', ')
            for j in range(0, len(fields)):
                if fields[j] != '' and fields[j] != 'None' and fields[j] != 'nan':
                    FOS_array.append(fields[j])

        # Converting into a json format
        result.append({
            "score": related_items[iterator][0],
            "ProductCode": related_items[iterator][1],
            "SkuCode": related_items[iterator][2],
            "Type": related_items[iterator][3],
            "AllFieldOfStudy": FOS_array,
            'EventStartDate': related_items[iterator][5],
            'EventEndDate': related_items[iterator][6]
        })

    # When 0 or less is passed send everything
    if no_of_rows <= 0:
        return result  # returning everything, not just 5 records
    else:
        # Else send only that many number of data
        return result[:no_of_rows]  # Sample calls

# Sample calls
# init()
# cormatrix = populateRecomendations()
# finaldata = getRecomendation('PC-005102')
# print(finaldata)
