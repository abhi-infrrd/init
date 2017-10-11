
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


def predict_courses_for_user(user, model, d_ui, all_course_club_unique, all_products_club_unique, courses, top_N):
    user_id = d_ui[user]
    required_columns = ['CourseCode', 'Type', 'AllFieldOfStudy', 'EventEndDate', 'EventStartDate']
    courses = pd.DataFrame(courses, columns=required_columns)
    scores = model.predict(user_id, np.arange(len(all_course_club_unique)))
    d_scores = {}
    for i in range(len(scores)):
        score = scores[i]
        d_scores[all_course_club_unique[i]] = score
    top_items = all_course_club_unique[np.argsort(-scores)]
    columns_required = list(courses.columns)
    columns_required.append('Score')
    top_items_info = pd.DataFrame(columns = columns_required)
    for i in range(0, len(all_course_club_unique)):
        item = top_items[i]
        item_info = courses.loc[courses['CourseCode'] == top_items[i]]
        if len(item_info) > 0:
            top_items_info = top_items_info.append(item_info, ignore_index = True)
            item = top_items[i]
            top_items_info.at[i, 'Score'] = d_scores[item]
        else:
            row = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            top_items_info.loc[len(top_items_info)] = row
            top_items_info.at[i, 'Score'] = d_scores[item]
            top_items_info.at[i, 'CourseCode'] = top_items[i]
        if i == top_N - 1:
            break
    top_items_info_json = top_items_info.to_json(orient='index')
    return top_items_info_json


# In[3]:


def predict_products_for_user(user, model, d_ui, all_course_club_unique, all_products_club_unique, products, top_N):
    user_id = d_ui[user]
    scores = model.predict(user_id, np.arange(len(all_course_club_unique) + 1, len(all_course_club_unique) + len(all_products_club_unique)))
    d_scores = {}
    for i in range(len(scores)):
        score = scores[i]
        d_scores[all_products_club_unique[i]] = score
    top_items = all_products_club_unique[np.argsort(-scores)]
    columns_required = list(products.columns)
    columns_required.append('Score')
    top_items_info = pd.DataFrame(columns = columns_required)
    counter = 0
    for i in range(0, len(all_products_club_unique)):
        item = top_items[i]
        item_info = products.loc[products['SkuID'] == top_items[i]]
        if len(item_info) > 0:
            top_items_info = top_items_info.append(item_info, ignore_index = True)
            item = top_items[i]
            top_items_info.at[counter, 'Score'] = d_scores[item]
            counter = counter + 1
        if counter == top_N:
            break
    required_columns = ['ProductCode', 'Type', 'AllFieldOfStudy', 'EventEndDate', 'EventStartDate', 'Score']
    top_items_info = pd.DataFrame(top_items_info, columns=required_columns)
    top_items_info_json = top_items_info.to_json(orient='index')
    return top_items_info_json

