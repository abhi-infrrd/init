# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:04:00 2017

@author: user
"""

from flask import Flask
from flask import Response
import json
import logging
import recommendationSystem as product_product_recommendation
import courses_courses as course_course_recommendation
import course_recommendation as user_course_recommendation
import prediction_for_user as predict_user
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

cormatrix1 = ''

cormatrix2 = ''

model = d_ui = all_course_club_unique = all_products_club_unique = courses = products =''

@app.route("/recommend/<project>/user/<userId>", methods=['GET'])
def get_user_records(project, userId):
  global model, d_ui, all_course_club_unique, all_products_club_unique, courses, products
  if(project=='courses'):
      return predict_user.predict_courses_for_user(userId , model, d_ui, all_course_club_unique, all_products_club_unique, courses, products)
  elif(project=='products'):
      return predict_user.predict_products_for_user(userId , model, d_ui, all_course_club_unique, all_products_club_unique, courses, products)
  
  #global cormatrix
  #finaldata = rec.getRecomendation(cormatrix, project)
  #l = []
  #print(finaldata[0][2].to_json())
  #k = len(finaldata)
  #for i in range(k):
  #  l.append(finaldata[i][2].to_json())
  return Response([],  mimetype='application/json')

@app.route("/recommend/<project>/item/<itemId>", methods=['GET'])
def get_project_records(project, itemId):
    
  global cormatrix1
  global cormatrix2
  finaldata = ''
  if(project=='products'):
      finaldata = product_product_recommendation.getRecomendation(cormatrix1, itemId)
  elif(project=='courses'):
      finaldata = course_course_recommendation.getCourseRecomendation(cormatrix2, itemId)
  l = []
  print(finaldata[0][2].to_dict())
  k = len(finaldata)
  for i in range(k):
    l.append(finaldata[i][2].to_dict())
  return Response(json.dumps(l),  mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True,port=2273)
cormatrix1 = product_product_recommendation.populateRecomendations()
cormatrix2 = course_course_recommendation.populateCourseRecomendations()
model, d_ui, all_course_club_unique, all_products_club_unique, courses, products = user_course_recommendation.train_model('.')
