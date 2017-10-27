
# coding: utf-8


import pandas as pd
import numpy as np
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
def predict_courses_for_user(user, model, d_ui, courses_with_metadata_index, courses_with_metadata, dictionary_courses_with_metadata, top_N = -1):
    # Get index of user from user dictionary
    try:
        user_id = d_ui[user]
        
    except Exception as e:
        logging.error('User ID does not exist')
        raise Exception("User ID does not exist")
    
    # Predict Scores for all courses for this user and store in dictionary
    scores = model.predict(user_id, np.array(courses_with_metadata_index))
    d_scores = {}
    for i in range(len(scores)):
        score = scores[i]
        d_scores[courses_with_metadata[i]] = score
        
    # Sorting scores in order
    top_items = courses_with_metadata[np.argsort(-scores)]
    
    # Iterating through all courses and populating the list of top N items and their metadata
    top_N_list = []
    counter = 0
    for item in top_items:
        item_info = dictionary_courses_with_metadata[item]
        item_info['score'] = d_scores[item]
        top_N_list.append(item_info)
        counter = counter + 1
        if (top_N != -1) and (counter == top_N):
            break
    logger.info('Fetched courses for the user')
    return top_N_list


def predict_products_for_user(user, model, d_ui, products_with_metadata_index, products_with_metadata, dictionary_products_with_metadata, top_N = -1):
    # Get index of user from user dictionary
    try:
        user_id = d_ui[user]
        
    except Exception as e:
        logging.error('User ID does not exist')
        raise Exception("User ID does not exist")
    
    # Predict Scores for all products for this user and store in dictionary
    scores = model.predict(user_id, np.array(products_with_metadata_index))
    d_scores = {}
    for i in range(len(scores)):
        score = scores[i]
        d_scores[products_with_metadata[i]] = score
    top_items = products_with_metadata[np.argsort(-scores)]
    
    # Iterating through all products and populating the list of top N items and their metadata
    top_N_list = []
    counter = 0
    for item in top_items:
        item_info = dictionary_products_with_metadata[item]
        item_info['score'] = d_scores[item]
        top_N_list.append(item_info)
        counter = counter + 1
        if (counter == top_N) and (top_N != -1):
            break
    logger.info('Fetched products for the user')
    return top_N_list

