# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:04:00 2017
@author: Abhishek Jha
"""
# This script produces the product-product and course-course recommendation.

# To run the script execute the following commands from the same directory
# export FLASK_APP=api.py
# python -m flask run --host=0.0.0.0 -p 2273

import numpy
import json
import product_product as product_product_recommendation
import courses_courses as course_course_recommendation
import hybrid_recommender as user_course_recommendation
import prediction_for_user as predict_user_item
import logging
import time
from flask import Flask
from flask import Response
from flask import request
from datetime import datetime
from CPA_recommender import CPA_recommender_initialise
import initialise_recommender
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Flask(__name__)

(model, d_ui, courses_with_metadata_index, courses_with_metadata, products_with_metadata_index, products_with_metadata, dictionary_courses_with_metadata, dictionary_products_with_metadata) = initialise_recommender.init_hybrid()

logger.info('Populating first correlation matrix for products')
#product_product_recommendation.init()
logger.info('Populating second correlation matrix for courses')
#course_course_recommendation.init()


@app.route("/recommend/<project>/user", methods=['GET'])
def get_user_records(project):
    userId = (request.args.get('userId'))
    userId.replace(" ", "+")
    global model, d_ui, all_course_club_unique, all_products_club_unique, courses, products
    try:
        if (project == 'CPA_COURSES'):
            logger.info('Fetching hybrid recommendation for courses for the user ' + userId)
            start_time = time.time()
            tempResponse = Response(json.dumps(
                predict_user_item.predict_courses_for_user(userId, model, d_ui, courses_with_metadata_index,
                                                           courses_with_metadata, dictionary_courses_with_metadata)),
                                    mimetype='application/json')
            logger.info('Fetched hybrid recommendation for courses for the user ' + userId + ', time taken ' + str(
                time.time() - start_time))
            return tempResponse
        
        elif (project == 'CPA_PRODUCTS'):
            logger.info('Fetching hybrid recommendation for products for the user ' + userId)
            start_time = time.time()
            tempResponse = Response(
                json.dumps(predict_user_item.predict_products_for_user(userId, model, d_ui, products_with_metadata_index,
                                                                       products_with_metadata,
                                                                       dictionary_products_with_metadata)),
                mimetype='application/json')
            logger.info('Fetched hybrid recommendation for products for the user ' + userId + ', time taken ' + str(
                time.time() - start_time))
            return tempResponse
    except Exception as e:
        logger.info('Cannot recommend to User ID')
        return Response(status=404, mimetype='application/json')


# itemId is a query parameter
# Method returns an array of json objects

@app.route("/recommend/<project>/item", methods=['GET'])
def get_project_records(project):
    itemId = request.args.get('itemId')


    finaldata = ''
    try:
        if (project == 'CPA_PRODUCTS'):
            logger.info('Content recommendation for the product ' + itemId)
            finaldata = product_product_recommendation.getRecomendation(itemId)
        elif (project == 'CPA_COURSES'):
            logger.info('Content recommendation for the course ' + itemId)
            finaldata = course_course_recommendation.getCourseRecomendation(itemId)
        else:
            logger.info('Inavlid itemId, no recommendation to return')
            return Response(status=404, mimetype='application/json')
    except Exception as e:
        logger.info('Inavlid itemId, Item not found')
        return Response(status=404, mimetype='application/json')

    for temp in finaldata:
        try:
            if (numpy.isnan(temp['Keywords'])):
                temp['Keywords'] = None
        except:
            pass
        try:
            temp['EventStartDate'] = datetime.strptime(temp['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
        except:
            temp['EventStartDate'] = None
        try:
            temp['EventEndDate'] = datetime.strptime(temp['EventEndDate'], '%Y-%m-%d %H:%M').isoformat()
        except:
            temp['EventEndDate'] = None
        try:
            if (numpy.isnan(temp['Topic'])):
                temp['Topic'] = None
        except:
            pass
        if (project == 'CPA_PRODUCTS'):
            temp['rItemId'] = temp['ProductCode']
        elif (project == 'CPA_COURSES'):
            temp['rItemId'] = temp['CourseCode']
    if (len(finaldata) == 0):
        return Response(json.dumps(None), mimetype='application/json')
    return Response(json.dumps(finaldata), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=2273)

