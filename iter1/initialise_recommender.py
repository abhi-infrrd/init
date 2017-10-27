import CPA_recommender as cpa
from CPA_recommender import CPA_recommender_initialise
import pickle
import logging
import time
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
def pickle_object_item_id(model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata):
   logger.info('Begin hybrid recommender\'s pickling')
   start_time = time.time()
   #filenames = []
   pickle.dump(model,open("model.pickle","wb"))
   #filenames.append("model.pickle")

   pickle.dump(d_ui,open("user_id.pickle","wb"))
   #filenames.append("user_id.pickle")

   pickle.dump(courses_with_metadata_index,open('courses_metadata_index.pickle','wb'))
   #filenames.append("courses_metadata_index.pickle")

   pickle.dump(courses_with_metadata,open('courses_metadata.pickle','wb'))
   #filenames.append("courses_metadata.pickle")

   pickle.dump(products_with_metadata_index,open('products_metadata_index.pickle','wb'))
   #filenames.append("products_metadata_index.pickle")

   pickle.dump(products_with_metadata,open('products_metadata.pickle','wb'))
   #filenames.append("products_metadata.pickle")

   pickle.dump(dictionary_courses_with_metadata,open('dictionary_courses_with_metadata.pickle','wb'))
   #filenames.append("dictionary_courses_with_metadata.pickle")

   pickle.dump(dictionary_products_with_metadata,open('dictionary_products_with_metadata.pickle','wb'))
   #filenames.append('dictionary_products_with_metadata.pickle')
   logger.info('Hybrid recommender\'s pickling finished, time taken is '+str(time.time() - start_time))
   #return filenames

def load_pickle_item_id():
    logger.info('Reading Hybrid recommender\'s pickles')
    start_time = time.time()
    model = pickle.load(open('model.pickle','rb'))
    d_ui = pickle.load(open('user_id.pickle','rb'))
    courses_with_metadata_index = pickle.load(open('courses_metadata_index.pickle','rb'))
    courses_with_metadata = pickle.load(open('courses_metadata.pickle','rb'))
    products_with_metadata_index = pickle.load(open('products_metadata_index.pickle','rb'))
    products_with_metadata = pickle.load(open('products_metadata.pickle','rb'))
    dictionary_courses_with_metadata = pickle.load(open('dictionary_courses_with_metadata.pickle','rb'))
    dictionary_products_with_metadata = pickle.load(open('dictionary_products_with_metadata.pickle','rb'))
    logger.info('Finished reading pickles, time taken is '+str(time.time() - start_time))
    
    return (model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata)
def init_hybrid():
    model= d_ui= courses_with_metadata_index= courses_with_metadata= products_with_metadata_index= products_with_metadata= dictionary_courses_with_metadata= dictionary_products_with_metadata = ''
    
    logger.info('Loading model for the hybrid recommender')

   
#if pickle doesn't exist
    (model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata) = CPA_recommender_initialise()
#pickle_object_item_id(model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata)  
     
#logger.info('Finished loading models for the recommender')
    
    return (model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata) 
def init_content_based():
    #logger.info('Populating first correlation matrix for products')
    #product_product_recommendation.init()
    #logger.info('Populating second correlation matrix for courses')
    #course_course_recommendation.init()
    pass   
