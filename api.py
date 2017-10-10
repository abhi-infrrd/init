# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:04:00 2017

@author: user
"""

from flask import Flask
from flask import Response
import json
import logging
import recommendationSystem as rec
import courses_courses as courses
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

cormatrix1 = ''

cormatrix2 = ''

@app.route("/recommend/<project>/user/<userId>", methods=['GET'])
def get_user_records(project, userId):
    
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
      finaldata = rec.getRecomendation(cormatrix1, itemId)
  elif(project=='courses'):
      finaldata = courses.getCourseRecomendation(cormatrix2, itemId)
  l = []
  print(finaldata[0][2].to_dict())
  k = len(finaldata)
  for i in range(k):
    l.append(finaldata[i][2].to_dict())
  return Response(json.dumps(l),  mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True,port=2273)
cormatrix1 = rec.populateRecomendations()
cormatrix2 = courses.populateCourseRecomendations()
