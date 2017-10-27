"""
Created on Tue Oct 10 17: 04:00 2017
@author : Anandu
#This script produces the course-course recommendation.
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

# Load data in the memory.
logger.info("Loading the courses_09202017 file ")
originaldata = pd.read_csv(io.open(config.courses_file["file_name"], 'r', encoding=config.courses_file["encoding"]), sep="\t", quoting=3)
originaldata = pd.DataFrame(originaldata.drop_duplicates('CourseCode'))
originaldata = originaldata.reset_index()  # This method populates the course correlation matrix


dataForRecomendation = pd.DataFrame(originaldata)
dataForRecomendation = dataForRecomendation.loc[:,
                       ['CourseCode', 'SkuCode', 'EventStartDate', 'EventEndDate']]

cormatrix = None


#  The initial method which should be called only once
#  Unpickles or populates the model in memory
def init():
    # unpickle
    try:
        pkl_file = open('course_pickled_data.pkl', 'rb')
        global cormatrix
        cormatrix = pickle.load(pkl_file)
        pkl_file.close()
    except:
        logger.warn("Pickled file not found, training new model")
        populateCourseRecomendations()
        init()


def populateCourseRecomendations():
    logger.info("Course course recommendation model training started")
    import re
    import nltk
    # Downloading stopwords list
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    # Get only the required data from the original data
    global originaldata
    data = pd.DataFrame(originaldata)
    data = data.loc[:, ['AllFieldOfStudy', 'Topic', 'Keywords']]

    # For all the fields take only the alphabets , to lowercase and stem it out
    for j in ['AllFieldOfStudy', 'Topic', 'Keywords']:
        for i in range(len(data)):
            data[j][i] = re.sub('[^a-zA-Z]', ' ', str(data[j][i]))
            data[j][i] = str(data[j][i]).lower()
            data[j][i] = data[j][i].split()
            ps = PorterStemmer()
            data[j][i] = [ps.stem(word) for word in data[j][i] if not word in set(stopwords.words('english'))]
            data[j][i] = ' '.join(data[j][i])

        # Vectorize the data of each column
        cv = CountVectorizer(max_features=100)
        x = cv.fit_transform(data[j]).toarray()

        # Add it back to the dataframe
        for i in range(len(x)):
            data[j][i] = x[i]

    # combine the all the columns and store in 'AllFieldOfstudy' column
    for i in range(len(x)):
        for j in ['Topic', 'Keywords']:
            data['AllFieldOfStudy'][i] = numpy.append(data['AllFieldOfStudy'][i], data[j][i])

    # remove the unwanted columns ie. other thatn 'ALlFieldOfStudy'
    data = data.loc[:, 'AllFieldOfStudy']

    # create the correlation matrix
    import scipy.stats

    # create the correlation matrix
    cormatrix = numpy.zeros([len(data), len(data)], tuple)
    for rows in range(len(data)):
        for cols in range(len(data)):
            cormatrix[rows][cols] = scipy.stats.pearsonr(data[rows], data[cols])

    logger.info("Course course recommendation training completed, pickling")

    output = open('course_pickled_data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(cormatrix, output)
    output.close()
    # return the correlation matrix
    return cormatrix


# Gets the recommendations for the courseCode provides from the correlation matrix created earlier.
# By default 100 courses are recommended but it can be altered by setting the NoOfValues param
# The p=value can also be set. But when p-value is set the Number of recommendations may be less than NoOFValues
def getCourseRecomendation(courseCode, NoOfValues=100, p_value=0.0):
    # Get the entire data file
    logger.debug("Getting course course recommendation")
    global dataForRecomendation
    global cormatrix

    # Find the index of the productcode
    item_index = ''
    try:
        # Get only the course code
        course_codes = dataForRecomendation.loc[:, 'CourseCode']
        # Get the index of the course code
        for item in range(len(course_codes)):
            if course_codes[item] == courseCode:
                item_index = item
                break
    except Exception as e:
        logging.error('Course Code does not exist', courseCode)
        raise Exception("Course code does not exist")

    # When course code is not present in the data catch it
    # Populate the data from the correlation matrix
    try:
        related_items = list()
        for items in range(len(cormatrix)):
            if cormatrix[item_index][items][1] >= p_value:
                if dataForRecomendation.loc[items, 'CourseCode'] != courseCode:
                    related_items.append([
                        cormatrix[item_index][items][0],
                        dataForRecomendation.iloc[items][0],
                        dataForRecomendation.iloc[items][1],
                        dataForRecomendation.iloc[items][2],
                        dataForRecomendation.iloc[items][3],
                        str(courseCode)
                    ])

    except Exception as e:
        logging.error('Course Code does not exist')
        raise Exception("Course code does not exist")

    # sort it in the highest similarity
    related_items.sort(reverse=True)

    # Prepare the result in the json format
    result = list()
    for iterator in range(len(related_items)):
        result.append({
            "score": related_items[iterator][0],
            "CourseCode": related_items[iterator][1],
            "CourseSkuCode": related_items[iterator][2],
            "EventStartDate": related_items[iterator][3],
            "EventEndDate": related_items[iterator][4],
        })

    if NoOfValues <= 0:
        return result  # returning everything, not just 5 records
    else:
        return result[:NoOfValues]

# Sample calls
# init()
# cormatrix = populateCourseRecomendations()
# finaldata = getCourseRecomendation('AAB03ED8E790489E894FBAC94DBA2512')
# print(finaldata)
