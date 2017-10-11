# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:04:00 2017

@author: user
"""

from flask import Flask
from flask import Response
from flask import request
#from flask import abort
import json
import logging
import recommendationSystem as product_product_recommendation
import courses_courses as course_course_recommendation
import hybrid_recommender as user_course_recommendation
import prediction_for_user as predict_user_item
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

cormatrix1 = ''

cormatrix2 = ''

model = d_ui = all_course_club_unique = all_products_club_unique = courses = products =''

@app.route("/recommend/<project>/user", methods=['GET'])
def get_user_records(project, userId):
  global model, d_ui, all_course_club_unique, all_products_club_unique, courses, products

  userId = request.args.get('userId')
  
  if(project=='courses'):
      return Response(predict_user_item.predict_courses_for_user(userId , model, d_ui, all_course_club_unique, all_products_club_unique, courses, products),  mimetype='application/json')
  elif(project=='products'):
      return Response(predict_user_item.predict_products_for_user(userId , model, d_ui, all_course_club_unique, all_products_club_unique, courses, products),  mimetype='application/json')

@app.route("/recommend/<project>/item", methods=['GET'])
def get_project_records(project):
  itemId = request.args.get('itemId')
  
  global cormatrix1
  global cormatrix2
  finaldata = ''
  if(project=='CPA_PRODUCTS'):
      finaldata = product_product_recommendation.getRecomendation(cormatrix1, itemId)
  elif(project=='CPA_COURSES'):
      finaldata = course_course_recommendation.getCourseRecomendation(cormatrix2, itemId)
  else:
      return Response(status=404, mimetype='application/json')
  l = []
  #print(finaldata[0][2].to_dict())
  k = len(finaldata)
  for i in range(k):
    temp = finaldata[i][2].to_dict()
    if(project=='CPA_PRODUCTS'):
        temp['rItemId'] = temp['ProductCode']
        temp['score'] = finaldata[i][0]
    elif(project=='CPA_COURSES'):
        temp['rItemId'] = temp['CourseCode']
        temp['score'] = finaldata[i][0]
    l.append(temp)
  return Response(json.dumps(l),  mimetype='application/json')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=2273)
cormatrix1 = product_product_recommendation.populateRecomendations()
cormatrix2 = course_course_recommendation.populateCourseRecomendations()
#model, d_ui, all_course_club_unique, all_products_club_unique, courses, products = user_course_recommendation.train_model('.')
