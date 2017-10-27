
# coding: utf-8

# In[14]:

import sys
#fsock = open('output','w')
#sys.stdout = sys.stderr = fsock


import pandas as pd
import numpy as np
import re
import scipy.sparse as sps
import codecs
from scipy.sparse import identity,coo_matrix, hstack
from collections import Counter
from hybrid_recommender import train_hybrid_recommender
import config


# In[15]:


# Finds unique fields in a column of pandas dataframe
def process_and_find_unique_fields(dataframe, column):
    column_uniques = dataframe[column].unique()
    unique_fields = []
    for i in range(0, len(column_uniques)):
        unique_candidate = column_uniques[i]
        if unique_candidate != np.nan and unique_candidate != 'None':
            unique_candidate = str(unique_candidate).replace(' ', '')
            unique_candidate = str(unique_candidate).replace('\\', ',')
            unique_candidate = str(unique_candidate).replace(';', ',')
            fields = str(unique_candidate).split(',')
            for j in range(0, len(fields)):
                if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                    unique_fields.append(fields[j].lower())
    unique_fields = list(set(unique_fields))
    return unique_fields

# Finds unique fields in CPA_state column of pandas dataframe
def process_and_find_unique_states(dataframe, column):
    column_uniques = dataframe[column].unique()
    unique_fields = []
    for i in range(0, len(column_uniques)):
        unique_candidate = column_uniques[i]
        if unique_candidate != np.nan and unique_candidate != 'None':
            unique_candidate = str(unique_candidate).replace(' ', '')
            unique_candidate = str(unique_candidate).replace('\\', ',')
            fields = str(unique_candidate).split(',')
            for j in range(0, len(fields)):
                if fields[j] !='' and fields[j] !='None'and fields[j] !='nan' and (not ('.' in fields[j])):
                    unique_fields.append(fields[j].lower())
    unique_fields = list(set(unique_fields))
    return unique_fields

# Finds top N keywords in column of pandas dataframe
def get_top_Keywords(keyword_unique, N):
    keyword_set = []
    for topics in keyword_unique:
        topic = str(topics).split(', ')
        for top in topic:
            if top != '':
                keyword_set.append(str(top))
    count = Counter(keyword_set)
    common_list = count.most_common(N)
    keyword_list = [ seq[0] for seq in common_list ]
    return keyword_list


# In[16]:


def CPA_preprocessing():
    # Reading all relevant files from csv / txt
    doc = codecs.open( config.courses_file["file_name"], 'rU', config.courses_file["encoding"])
    courses = pd.read_csv(doc, sep = '\t')

    doc = codecs.open(  config.product_file["file_name"], 'rU', config.product_file["encoding"])
    products = pd.read_csv(doc, sep = '\t')

    doc = codecs.open( config.product_order_summary_file["file_name"], 'rU', config.product_order_summary_file["encoding"])
    products_order_summary = pd.read_csv(doc, sep = '\t')
    products_order_summary = products_order_summary[pd.notnull(products_order_summary['SkuID'])]
    products_order_summary = products_order_summary[pd.notnull(products_order_summary['EncryptedRecordID'])]

    doc = codecs.open( config.user_enrollments_completions_file["file_name"], 'rU', config.user_enrollments_completions_file['encoding'])
    course_completion = pd.read_csv(doc, sep = '\t')
    course_completion = course_completion[pd.notnull(course_completion['CourseCode'])]
    course_completion = course_completion[pd.notnull(course_completion['EncryptedRecordID'])]

    doc = codecs.open( config.user_subscriptions_file["file_name"], 'rU', config.user_subscriptions_file["encoding"])
    user_subscription = pd.read_csv(doc, sep = '\t')
    user_subscription = user_subscription[pd.notnull(user_subscription['SkuID'])]
    user_subscription = user_subscription[pd.notnull(user_subscription['EncryptedUserID'])]

    demographics = pd.read_csv( config.user__masterlist_file["file_name"], sep = '\t')

    # Finding all unique Courses
    courses_club_unique = courses['CourseCode'].unique()

    courses_enrolments_club_unique = course_completion['CourseCode'].unique()

    all_course_club_unique = np.concatenate((courses_club_unique,courses_enrolments_club_unique))
    all_course_club_unique = np.unique(all_course_club_unique)


    # Finding all unique Products
    products_club_unique = products['SkuID'].unique()

    products_order_club_unique = products_order_summary['SkuID'].unique()

    all_products_club_unique = np.concatenate((products_club_unique, products_order_club_unique))
    all_products_club_unique = np.unique(all_products_club_unique)

    #Finding all unique Subscriptions
    subscriptions_unique = user_subscription['SkuID'].unique()

    # Finding all unique Products and products
    course_products_club_unique = np.concatenate((all_course_club_unique, all_products_club_unique, subscriptions_unique))
    course_products_club_unique = np.unique(course_products_club_unique)


    # Finding all unique Users
    users_from_demographics_unique = demographics['EncryptedRecordID'].unique()

    users_from_subscription_unique = user_subscription['EncryptedUserID'].unique()

    users_from_course_completion_unique = course_completion['EncryptedRecordID'].unique()

    users_from_products_order_summary_unique = products_order_summary['EncryptedRecordID'].unique()

    users_club = np.concatenate((users_from_demographics_unique,users_from_subscription_unique,users_from_course_completion_unique,users_from_products_order_summary_unique))
    users_club_unique = np.unique(users_club)


    # Build a dictionary with the user index for all users
    d_ui = {}
    for i in range(len(users_club_unique)):
        user = users_club_unique[i]
        d_ui[user] = i


    # Build a dictionary with the course/product index for all course/product
    d_ci = {}
    for i in range(len(course_products_club_unique)):
        course = course_products_club_unique[i]
        d_ci[course] = i

    # Build a sparse matrix for user-item interaction
    Mui_tr = sps.lil_matrix((len(users_club_unique), (len(all_course_club_unique) + len(all_products_club_unique))), dtype=np.int8)

    # Now fill Mui_tr with the info from course_completion file
    for i in range(len(course_completion)):
        user = course_completion["EncryptedRecordID"].values[i]
        course = course_completion["CourseCode"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0

    # Now fill Mui_tr with the info from products_order_summary file
    for i in range(len(products_order_summary)):
        user = products_order_summary["EncryptedRecordID"].values[i]
        course = products_order_summary["SkuID"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0

    # Now fill Mui_tr with the info from user_subscription file
    for i in range(len(user_subscription)):
        user = user_subscription["EncryptedUserID"].values[i]
        course = user_subscription["SkuID"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0

    # Process and find unique fields in user demographics
    user_unique_cred = process_and_find_unique_fields(demographics, 'Credential')
    user_unique_expert = process_and_find_unique_fields(demographics, 'Expertise')
    user_unique_interest = process_and_find_unique_fields(demographics, 'Interest')
    user_unique_judi = process_and_find_unique_fields(demographics, 'Jurisdiction')
    user_unique_state = process_and_find_unique_states(demographics, 'State')

    # d_ui has list of users
    # Build a dict with the user features in ulist
    d_uf = {}
    feature_count = 0
    for i in range(len(user_unique_cred)):
        feature = user_unique_cred[i]
        d_uf['%s_credential' %feature] = i

    feature_count = feature_count + i + 1
    for i in range(len(user_unique_state)):
        feature = user_unique_state[i]
        d_uf['%s_state' %feature] = i + feature_count

    feature_count = feature_count + i + 1
    for i in range(len(user_unique_expert)):
        feature = user_unique_expert[i]
        d_uf['%s_expert' %feature] = i + feature_count

    feature_count = feature_count + i + 1
    for i in range(len(user_unique_interest)):
        feature = user_unique_interest[i]
        d_uf['%s_interest' %feature] = i + feature_count

    feature_count = feature_count + i + 1
    for i in range(len(user_unique_judi)):
        feature = user_unique_judi[i]
        d_uf['%s_jurisdiction' %feature] = i + feature_count

    # d_ui has list of users
    # Build a sparse matrix for user-metadata
    Mui_uf = sps.lil_matrix((len(users_club_unique), len(d_uf)), dtype=np.int8)

    # Now fill Mui_uf with the info from user features
    for i in range(len(demographics)):
        if demographics["EncryptedRecordID"].values[i] == '#Name?':
            i = i+1
        user = demographics["EncryptedRecordID"].values[i]
        ui = d_ui[user]
        credential = demographics['Credential'].values[i]
        credential = str(credential).replace(' ', '')
        credential = str(credential).replace('\\', ',')
        fields = str(credential).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j].lower() + '_credential']
                Mui_uf[ui, uf] = 1.0


        state = demographics['State'].values[i]
        state = str(state).replace(' ', '')
        state = str(state).replace('\\', ',')
        fields = str(state).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan' and (not ('.' in fields[j])):
                uf = d_uf[fields[j].lower() + '_state']
                Mui_uf[ui, uf] = 1.0

        expert = demographics['Expertise'].values[i]
        expert = str(expert).replace(' ', '')
        expert = str(expert).replace('\\', ',')
        fields = str(expert).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j].lower() + '_expert']
                Mui_uf[ui, uf] = 1.0

        interest = demographics['Interest'].values[i]
        interest = str(interest).replace(' ', '')
        interest = str(interest).replace('\\', ',')
        fields = str(interest).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j].lower() + '_interest']
                Mui_uf[ui, uf] = 1.0

        jurisdiction = demographics['Jurisdiction'].values[i]
        jurisdiction = str(jurisdiction).replace(' ', '')
        jurisdiction = str(jurisdiction).replace('\\', ',')
        fields = str(jurisdiction).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j].lower() + '_jurisdiction']
                Mui_uf[ui, uf] = 1.0

    Mui_uf = hstack([Mui_uf, identity(len(users_club_unique))])

    required_columns = ['CourseCode', 'AllFieldOfStudy', 'TotalCreditHours', 'Topic', 'Type', 'PriceRange', 'Keywords', 'EventEndDate', 'EventStartDate']
    courses = pd.DataFrame(courses, columns=required_columns)

    # Process and find unique fields in Courses
    course_unique_FOS = process_and_find_unique_fields(courses, 'AllFieldOfStudy')

    set_topics = []
    course_topic = courses['Topic'].unique()
    for i in range(0, len(course_topic)):
        set_topics.append([x.strip() for x in (str((course_topic[i]))).split('|')])
    course_unique_topics = []
    for topics in course_topic:
        topic = str(topics).split('|')
        for top in topic:
            if top != '' and top !='None' and top !='nan':
                course_unique_topics.append(str(top))

    course_unique_topics = list(set(course_unique_topics))

    course_unique_type = list(courses['Type'].unique())
    course_unique_type = [x for x in course_unique_type if str(x) != 'nan']

    course_unique_keywords = get_top_Keywords(courses['Keywords'].unique(), 100)

    course_price = courses['PriceRange'].unique()
    average_course_price_unique =[]
    for i in range(0, len(course_price)):
        if not (pd.isnull(course_price[i])):
            priceends = course_price[i].split(' - ')
            for j in range(0, len(priceends)):
                priceends[j] = float(priceends[j].replace('$', '').replace(',',''))
            average_course_price_unique.append(int(np.mean(priceends)))

    course_bins = np.linspace(0, max(average_course_price_unique), 10)

    required_columns = ['ProductCode', 'SkuID', 'Type', 'AllFieldOfStudy', 'TotalCreditHours', 'PriceRange', 'Topic', 'Keywords']
    products = pd.DataFrame(products, columns=required_columns)

    # Process and find unique fields in Products
    product_unique_type = list(products['Type'].unique())
    product_unique_type = [x for x in product_unique_type if str(x) != 'nan']

    product_unique_FOS = process_and_find_unique_fields(products, 'AllFieldOfStudy')
    len(product_unique_FOS)#36

    set_topics = []
    product_topic = products['Topic'].unique()
    for i in range(0, len(product_topic)):
        set_topics.append([x.strip() for x in (str((product_topic[i]))).split('|')])
    product_unique_topics = []
    for topics in product_topic:
        topic = str(topics).split('|')
        for top in topic:
            if top != '' and top !='None' and top !='nan':
                product_unique_topics.append(str(top))

    product_unique_topics = list(set(product_unique_topics))

    product_unique_keywords = get_top_Keywords(products['Keywords'].unique(), 100)

    product_price = products['PriceRange'].unique()
    average_product_price_unique =[]
    for i in range(0, len(product_price)):
        if not (pd.isnull(product_price[i])):
            priceends = product_price[i].split(' - ')
            for j in range(0, len(priceends)):
                priceends[j] = float(priceends[j].replace('$', '').replace(',',''))
            average_product_price_unique.append(int(np.mean(priceends)))

    product_bins = np.linspace(0, max(average_product_price_unique), 10)

    #d_ci has list of courses/products
    # Build a dictionary with the item features
    d_if = {}
    unique_type = list(set().union(product_unique_type,course_unique_type))
    feature_count = 0
    for i in range(len(unique_type)):
        feature = unique_type[i]
        d_if['%s_type' %feature] = i

    unique_FOS = list(set().union(product_unique_FOS,course_unique_FOS))
    feature_count = feature_count + i + 1
    for i in range(len(unique_FOS)):
        feature = unique_FOS[i]
        d_if['%s_FOS' %feature] = i + feature_count

    feature_count = feature_count + i + 1
    d_if['TotalCreditHours'] = feature_count

    feature_count = feature_count + 1
    unique_topic = list(set().union(product_unique_topics,course_unique_topics))
    for i in range(len(unique_topic)):
        feature = unique_topic[i]
        d_if['%s_topic' %feature] = i + feature_count

    unique_keywords = list(set().union(product_unique_keywords,course_unique_keywords))
    feature_count = feature_count + i + 1

    for i in range(len(unique_keywords)):
        feature = unique_keywords[i]
        d_if['%s_keyword' %feature] = i + feature_count

    price_range = max(max(average_product_price_unique), max(average_course_price_unique))
    price_bins = np.linspace(0, price_range, 10)
    feature_count = feature_count + i + 1

    for i in range(len(product_bins)):
        d_if['price Range %s' %str(i+1)] = i + feature_count
    feature_count = feature_count + i + 1

    # Build the user x item matrices using scipy lil_matrix
    Mui_if = sps.lil_matrix((len(course_products_club_unique), len(d_if)), dtype=np.int8)

    # Now fill Mui_tr with the info from course features
    for i in range(len(courses)):
        course = courses["CourseCode"].values[i]
        ci = d_ci[course]
        FOS = courses['AllFieldOfStudy'].values[i]
        FOS = str(FOS).replace(' ', '')
        FOS = str(FOS).replace('\\', ',')
        FOS = str(FOS).replace(';', ',')
        fields = str(FOS).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                fi = d_if[fields[j].lower() + '_FOS']
                Mui_if[ci, fi] = 1.0

        credit_hours = courses["TotalCreditHours"].values[i]
        if not np.isnan(credit_hours):
            fi = d_if['TotalCreditHours']
            Mui_if[ci, fi] = credit_hours

        typec = courses['Type'].values[i] + '_type'
        fi = d_if[typec]
        Mui_if[ci, fi] = 1.0

        pricerange = courses['PriceRange'].values[i]
        if (not (pd.isnull(pricerange))):
            priceends = str(pricerange).split(' - ')
            for j in range(0, len(priceends)):
                priceends[j] = float(priceends[j].replace('$', '').replace(',',''))
            price_avg = int(np.mean(priceends))
            course_price_bin = int(np.digitize(price_avg, price_bins))
            pricerange = 'price Range %s' %course_price_bin
            fi = d_if[pricerange]
            Mui_if[ci, fi] = 1.0

        topic = str(courses['Topic'].values[0]).split('|')
        for top in topic:
            if top != '' and top !='None' and top !='nan':
                fi = d_if[str(top) + '_topic']
                Mui_if[ci, fi] = 1.0

    # Now fill Mui_tr with the info from product features
    for i in range(len(products)):
        product = products["SkuID"].values[i]
        ci = d_ci[product]
        FOS = products['AllFieldOfStudy'].values[i]
        FOS = str(FOS).replace(' ', '')
        FOS = str(FOS).replace('\\', ',')
        FOS = str(FOS).replace(';', ',')
        fields = str(FOS).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                fi = d_if[fields[j].lower() + '_FOS']
                Mui_if[ci, fi] = 1.0

        credit_hours = products["TotalCreditHours"].values[i]
        if not np.isnan(credit_hours):
            fi = d_if['TotalCreditHours']
            Mui_if[ci, fi] = credit_hours

        typec = products['Type'].values[i]
        if str(typec) != 'nan':
            typec = typec + '_type'
            fi = d_if[typec]
            Mui_if[ci, fi] = 1.0

        pricerange = products['PriceRange'].values[i]
        if (not (pd.isnull(pricerange))):
            priceends = str(pricerange).split(' - ')
            for j in range(0, len(priceends)):
                priceends[j] = float(priceends[j].replace('$', '').replace(',',''))
            price_avg = int(np.mean(priceends))
            product_price_bin = int(np.digitize(price_avg, price_bins))
            pricerange = 'price Range %s' %product_price_bin
            fi = d_if[pricerange]
            Mui_if[ci, fi] = 1.0

        topic = str(products['Topic'].values[0]).split('|')
        for top in topic:
            if top != '' and top !='None' and top !='nan':
                fi = d_if[str(top) + '_topic']
                Mui_if[ci, fi] = 1.0

    Mui_if = hstack([Mui_if, identity(len(course_products_club_unique))])

    # Filtering out courses with metadata, since only they can be recommended
    courses_with_metadata_index = []
    courses_with_metadata = []
    for i in range(len(all_course_club_unique)):
        if any(courses.CourseCode == all_course_club_unique[i]):
            courses_with_metadata.append(all_course_club_unique[i])
            courses_with_metadata_index.append(d_ci[all_course_club_unique[i]])

    courses_with_metadata = np.array(courses_with_metadata)

    # Filtering out products with metadata, since only they can be recommended
    products_with_metadata_index = []
    products_with_metadata = []
    for i in range(len(all_products_club_unique)):
        if any(products.SkuID == all_products_club_unique[i]):
            products_with_metadata.append(all_products_club_unique[i])
            products_with_metadata_index.append(d_ci[all_products_club_unique[i]])

    products_with_metadata = np.array(products_with_metadata)

    dictionary_courses_with_metadata = {}
    for item in courses_with_metadata:
            item_info = courses.loc[courses['CourseCode'] == item]
            if len(item_info) > 0:
                FOS = item_info.iloc[-1]['AllFieldOfStudy']
                FOS_array = []
                if FOS != np.nan and FOS != 'None':    
                    FOS = str(FOS).replace(';', ',')
                    fields = str(FOS).split(', ')
                    for j in range(0, len(fields)):
                        if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                            FOS_array.append(fields[j])
                try:
                    start_date = datetime.strptime(item_info.iloc[-1]['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
                except:
                    start_date = None
                try:
                    end_date = datetime.strptime(item_info.iloc[-1]['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
                except:
                    end_date = None
                dictionary_courses_with_metadata[item] = {'itemId' : item,
                                                       'Type' : item_info.iloc[-1]['Type'],
                                                       'AllFieldOfStudy' : FOS_array,
                                                       'EventEndDate' : end_date,
                                                       'EventStartDate' : start_date}


    dictionary_products_with_metadata = {}
    for item in products_with_metadata:
            item_info = products.loc[products['SkuID'] == item]
            len_item_info = len(item_info)
            if len_item_info > 0:
                FOS = item_info.iloc[-1]['AllFieldOfStudy']
                FOS_array = []
                if FOS != np.nan and FOS != 'None':    
                    FOS = str(FOS).replace(';', ',')
                    fields = str(FOS).split(', ')
                    for j in range(0, len(fields)):
                        if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                            FOS_array.append(fields[j])
                try:
                    start_date = datetime.strptime(item_info.iloc[-1]['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
                except:
                    start_date = None
                try:
                    end_date = datetime.strptime(item_info.iloc[-1]['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
                except:
                    end_date = None
                dictionary_products_with_metadata[item] ={'itemId' : item_info.iloc[-1]['ProductCode'],
                                                           'Type' : item_info.iloc[-1]['Type'],
                                                           'AllFieldOfStudy' : FOS_array,
                                                           'EventEndDate' : end_date,
                                                           'EventStartDate' : start_date}
    return(Mui_tr, Mui_if, Mui_uf, d_ui, courses_with_metadata_index, 
           courses_with_metadata, products_with_metadata_index, 
           products_with_metadata, dictionary_courses_with_metadata, 
           dictionary_products_with_metadata)



# In[24]:


(Mui_tr, Mui_if, Mui_uf, d_ui, courses_with_metadata_index, 
           courses_with_metadata, products_with_metadata_index, 
           products_with_metadata, dictionary_courses_with_metadata, 
           dictionary_products_with_metadata) = CPA_preprocessing()


# In[25]:


from skopt import forest_minimize
from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k
import lightfm


# In[30]:


def objective_wsideinfo(params):
    # unpack
    epochs, learning_rate,    no_components, item_alpha,    scale = params
    
    print 'epochs:', epochs
    print 'learning_rate:', learning_rate
    print 'no_components:', no_components
    print 'item_alpha:', item_alpha
    print 'scale:', scale
    sys.stdout.flush()
    user_alpha = item_alpha * scale
    model = LightFM(loss='warp',
                    random_state=2016,
                    learning_rate=learning_rate,
                    no_components=no_components,
                    user_alpha=user_alpha,
                    item_alpha=item_alpha)
    model.fit( Mui_tr, item_features = Mui_if, user_features=Mui_uf,
              epochs=epochs,
              num_threads=4, verbose=True)
    
    patks = precision_at_k(model,  Mui_tr, 
                           item_features = Mui_if, 
                           user_features=Mui_uf,
                           train_interactions=None, 
                           k=5, num_threads=4)
    mapatk = np.mean(patks)
    # Make negative because we want to _minimize_ objective
    out = -mapatk
    # Weird shit going on
    if np.abs(out + 1) < 0.01 or out < -1.0:
        return 0.0
    else:
        return out


# In[ ]:


space = [(10, 150), # epochs
         (10**-3, 1.0, 'log-uniform'), # learning_rate
         (20, 200), # no_components
         (10**-5, 10**-3, 'log-uniform'), # item_alpha
         (0.001, 1., 'log-uniform') # user_scaling
        ]
#x0 = res_fm.x.append(1.)
# This typecast is required
item_features = Mui_if.astype(np.float32)
res_fm_itemfeat = forest_minimize(objective_wsideinfo, space, n_calls=10,
                                  random_state=0,
                                  verbose=True)


# In[28]:


print('Maximimum p@k found: {:6.5f}'.format(-res_fm_itemfeat.fun))
print('Optimal parameters:')
sys.stdout.flush()
params = ['epochs', 'learning_rate', 'no_components', 'item_alpha', 'scaling']
for (p, x_) in zip(params, res_fm_itemfeat.x):
    print('{}: {}'.format(p, x_))
    sys.stdout.flush()


# Maximimum p@k found: 0.19531
# Optimal parameters:
# epochs: 68
# learning_rate: 0.0271016262622
# no_components: 59
# item_alpha: 0.000114232541556
# scaling: 0.0505980387466
