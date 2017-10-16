# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:04:00 2017

@author: Abhishek Jha
"""
#This script produces the product-product and course-course recommendation. 

#To run the script execute the following commands from the same directory
#export FLASK_APP=api.py
#python -m flask run --host=0.0.0.0 -p 2273

#import os
#os.chdir("C:\\Users\\user\\Desktop\\recommender-infrrd-10-11-2017\\init")
from flask import Flask
from flask import Response
from flask import request
import numpy
import json
#import product_product as product_product_recommendation
#import courses_courses as course_course_recommendation
from datetime import datetime
import test_product_recommender as rc
app = Flask(__name__)

cormatrix1 = ''

cormatrix2 = ''

#itemId is a query parameter
#returns an array of json objects
@app.route("/recommend/<project>/item", methods=['GET'])
def get_project_records(project):
  itemId = request.args.get('itemId')
  
  global cormatrix1
  global cormatrix2
  finaldata = ''
  if(project=='CPA_PRODUCTS'):
      finaldata = rc.cos_recommendation(itemId)
  elif(project=='CPA_COURSES'):
      finaldata = course_course_recommendation.getCourseRecomendation(cormatrix2, itemId)
  else:
      return Response(status=404, mimetype='application/json')
  for temp in finaldata:
          if(project=='CPA_PRODUCTS'):
              temp['rItemId'] = temp['ProductCode']
          else:
              temp['rItemId'] = temp['CourseCode']
          try:
              temp['Topic'] = temp['Topic'].replace('||',' ')
              temp['Topic'] = temp['Topic'].replace('|',' ')
              temp['Topic'] = temp['Topic'].split()
          except:
              temp['Topic'] = []
          try:
              temp['AllFieldOfStudy'] = temp['AllFieldOfStudy'].replace(',','  ').split()
          except:
              temp['AllFieldOfStudy'] = []
          try:
            temp['EventStartDate'] = datetime.strptime(temp['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
          except:
            temp['EventStartDate'] = None
          try:
            temp['EventEndDate'] = datetime.strptime(temp['EventEndDate'], '%Y-%m-%d %H:%M').isoformat()
          except:
            temp['EventEndDate'] = None
          try:
              if(numpy.isnan(temp['Keywords'])):
                temp['Keywords'] = None
          except:
              pass
  return Response(json.dumps(finaldata),  mimetype='application/json')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=2273)
    
#Intial training on startup, delays the availability of endpoint by a few minutes
#cormatrix1 = product_product_recommendation.populateRecomendations()
#cormatrix2 = course_course_recommendation.populateCourseRecomendations()
rc.initialise()