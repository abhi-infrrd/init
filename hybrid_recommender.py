import pandas as pd
import numpy as np
import re
import scipy.sparse as sps
import codecs
from scipy.sparse import identity,coo_matrix, hstack
from collections import Counter
import pickle as pkl


def train_model(local_path):

    #read_user_files_from_local_and_merge(local_path)

    # Reading all relevant files from csv / txt
    doc = codecs.open(local_path + '/Courses_09202017.txt', 'rU', 'UTF-16')
    courses = pd.read_csv(doc, sep = '\t')

    doc = codecs.open(local_path + '/Products_09202017.txt', 'rU', 'UTF-8')#16-->8
    products = pd.read_csv(doc, sep = '\t')

    doc = codecs.open(local_path + '/ProdOrderSummary_09202017.txt', 'rU', 'UTF-8')
    products_order_summary = pd.read_csv(doc, sep = '\t')

    doc = codecs.open(local_path + '/UserEnrollmentsCompletions_09222017.txt', 'rU', 'UTF-8')
    course_completion = pd.read_csv(doc, sep = '\t')

    doc = codecs.open(local_path + '/UserSubscriptions_09202017.txt', 'rU', 'UTF-8')
    user_subscription = pd.read_csv(doc, sep = '\t')

    demographics = pd.read_csv(local_path + '/user__masterlist.csv',  sep = '\t', encoding='ISO-8859-1')


    courses_club = courses['CourseCode']
    courses_club_unique = courses_club.unique()

    courses_enrolments_club = course_completion['CourseCode']
    courses_enrolments_club_unique = courses_enrolments_club.unique()

    all_course_club = np.concatenate((courses_club_unique,courses_enrolments_club_unique))
    all_course_club_unique = np.unique(all_course_club)

    products_club = products['SkuID']
    products_club_unique = products_club.unique()

    products_order_club = products_order_summary['SkuID']
    products_order_club_unique = products_order_club.unique()

    all_products_club = np.concatenate((products_club_unique, products_order_club_unique))
    all_products_club_unique = np.unique(all_products_club)

    course_products_club = np.concatenate((courses_club_unique,courses_enrolments_club_unique, products_club_unique, products_order_club_unique))
    course_products_club_unique = np.unique(course_products_club)

    users_from_demographics = demographics['EncryptedRecordID']
    users_from_demographics_unique = users_from_demographics.unique()

    users_from_subscription = user_subscription['EncryptedUserID']
    users_from_subscription_unique = users_from_subscription.unique()

    users_from_course_completion = course_completion['EncryptedRecordID']
    users_from_course_completion_unique = users_from_course_completion.unique()

    users_from_products_order_summary = products_order_summary['EncryptedRecordID']
    users_from_products_order_summary_unique = users_from_products_order_summary.unique()

    users_club = np.concatenate((users_from_demographics_unique,users_from_subscription_unique,users_from_course_completion_unique,users_from_products_order_summary_unique))
    users_club_unique = np.unique(users_club)



    # Build a dict with the user index in ulist
    d_ui = {}
    for i in range(len(users_club_unique)):
        user = users_club_unique[i]
        d_ui[user] = i


    # Build a dict with the course/product index in ulist
    d_ci = {}
    for i in range(len(all_course_club_unique)):
        course = all_course_club_unique[i]
        d_ci[course] = i

    course_number = i + 1
    for i in range(len(all_products_club_unique)):
        course = all_products_club_unique[i]
        d_ci[course] = i + course_number

    # Build the user x item matrices using scipy lil_matrix
    Mui_tr = sps.lil_matrix((len(users_club_unique), (len(all_course_club_unique) + len(all_products_club_unique))), dtype=np.int8)

    # Now fill Mui_tr with the info from cpdtr
    for i in range(len(course_completion)):
        user = course_completion["EncryptedRecordID"].values[i]
        course = course_completion["CourseCode"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0


    # Now fill Mui_tr with the info from cpdtr
    for i in range(len(products_order_summary)):
        user = products_order_summary["EncryptedRecordID"].values[i]
        course = products_order_summary["SkuID"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0

    for i in range(len(user_subscription)):
        user = user_subscription["EncryptedUserID"].values[i]
        course = user_subscription["SkuID"].values[i]
        ui, ci = d_ui[user], d_ci[course]
        Mui_tr[ui, ci] = 1.0


    user_cred = demographics['Credential'].unique()
    user_unique_cred = []
    for i in range(0, len(user_cred)):
        user_cred[i] = str(user_cred[i]).replace(' ', '')
        fields = str(user_cred[i]).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                user_unique_cred.append(fields[j])

    user_unique_cred = list(set(user_unique_cred))

    user_expert = demographics['Expertise'].unique()
    user_unique_expert = []
    for i in range(0, len(user_expert)):
        user_expert[i] = str(user_expert[i]).replace(' ', '')
        fields = str(user_expert[i]).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                user_unique_expert.append(fields[j])

    user_unique_expert = list(set(user_unique_expert))

    user_interst = demographics['Interest'].unique()
    user_unique_interest = []
    for i in range(0, len(user_interst)):
        user_interst[i] = str(user_interst[i]).replace(' ', '')
        user_interst[i] = str(user_interst[i]).replace('\\', ',')
        fields = str(user_interst[i]).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                user_unique_interest.append(fields[j])

    user_unique_interest = list(set(user_unique_interest))

    user_judi = demographics['Jurisdiction'].unique()
    user_unique_judi = []
    for i in range(0, len(user_judi)):
        user_judi[i] = str(user_judi[i]).replace(' ', '')
        fields = str(user_judi[i]).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                user_unique_judi.append(fields[j])

    user_unique_judi = list(set(user_unique_judi))

    user_state = demographics['State'].unique()
    user_unique_state = []
    for i in range(0, len(user_state)):
        user_state[i] = str(user_state[i]).replace(' ', '')
        fields = str(user_state[i]).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan' and (not ('.' in fields[j])):
                user_unique_state.append(fields[j])

    user_unique_state = list(set(user_unique_state))



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

    #d_ui has list of users

    from scipy.sparse import identity,coo_matrix, hstack
    # Build the user x item matrices using scipy lil_matrix
    Mui_uf = sps.lil_matrix((len(users_club_unique), len(d_uf)), dtype=np.int8)

    # Now fill Mui_tr with the info from course features
    for i in range(len(demographics)):
        if demographics["EncryptedRecordID"].values[i] == '#Name?':
            i = i+1
        user = demographics["EncryptedRecordID"].values[i]
        ui = d_ui[user]
        credential = demographics['Credential'].values[i]
        credential = str(credential).replace(' ', '')
        fields = str(credential).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j] + '_credential']
                Mui_uf[ui, uf] = 1.0


        state = demographics['State'].values[i]
        state = str(state).replace(' ', '')
        fields = str(state).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan' and (not ('.' in fields[j])):
                uf = d_uf[fields[j] + '_state']
                Mui_uf[ui, uf] = 1.0

        expert = demographics['Expertise'].values[i]
        expert = str(expert).replace(' ', '')
        fields = str(expert).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j] + '_expert']
                Mui_uf[ui, uf] = 1.0

        interest = demographics['Interest'].values[i]
        interest = str(interest).replace(' ', '')
        interest = str(interest).replace('\\', ',')
        fields = str(interest).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j] + '_interest']
                Mui_uf[ui, uf] = 1.0

        jurisdiction = demographics['Jurisdiction'].values[i]
        jurisdiction = str(jurisdiction).replace(' ', '')
        fields = str(jurisdiction).split(',')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                uf = d_uf[fields[j] + '_jurisdiction']
                Mui_uf[ui, uf] = 1.0

    Mui_uf = hstack([Mui_uf, identity(len(users_club_unique))])



    required_columns = ['CourseCode', 'AllFieldOfStudy', 'TotalCreditHours', 'Topic', 'Type', 'PriceRange', 'Keywords']
    courses = pd.DataFrame(courses, columns=required_columns)

    course_FOS = courses['AllFieldOfStudy'].unique()
    course_unique_FOS = []
    for i in range(0, len(course_FOS)):
        course_FOS[i] = str(course_FOS[i]).replace(';', ',')
        fields = str(course_FOS[i]).split(', ')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                course_unique_FOS.append(fields[j])

    course_unique_FOS = list(set(course_unique_FOS))

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

    product_unique_type = list(products['Type'].unique())
    product_unique_type = [x for x in product_unique_type if str(x) != 'nan']

    product_FOS = products['AllFieldOfStudy'].unique()
    product_unique_FOS = []
    for i in range(0, len(product_FOS)):
        product_FOS[i] = str(product_FOS[i]).replace(';', ',')
        fields = str(product_FOS[i]).split(', ')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                product_unique_FOS.append(fields[j])

    product_unique_FOS = list(set(product_unique_FOS))

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



    # Build a dict with the item features in ulist
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
        d_if['price Range %s' %i] = i + feature_count
    feature_count = feature_count + i + 1
    #d_ci has list of courses/products



    # Build the user x item matrices using scipy lil_matrix
    Mui_if = sps.lil_matrix((len(course_products_club_unique), len(d_if)), dtype=np.int8)

    # Now fill Mui_tr with the info from course features
    for i in range(len(courses)):
        course = courses["CourseCode"].values[i]
        ci = d_ci[course]
        FOS = courses['AllFieldOfStudy'].values[i]
        FOS = str(FOS).replace(';', ',')
        fields = str(FOS).split(', ')
        for j in range(0, len(fields)):
            if fields[j] !='' and fields[j] !='None'and fields[j] !='nan':
                fi = d_if[fields[j] + '_FOS']
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

        topic = str(products['Topic'].values[0]).split('|')
        for top in topic:
            if top != '' and top !='None' and top !='nan':
                fi = d_if[str(top) + '_topic']
                Mui_if[ci, fi] = 1.0


    Mui_if = hstack([Mui_if, identity(len(course_products_club_unique))])



    doc = codecs.open(local_path + '/Courses_09202017.txt', 'rU', 'UTF-16')
    courses = pd.read_csv(doc, sep = '\t')
    doc = codecs.open(local_path + '/Products_09202017.txt', 'rU', 'UTF-16')
    products = pd.read_csv(doc, sep = '\t')



    from lightfm import LightFM
    from lightfm.evaluation import auc_score, precision_at_k


    model = LightFM(no_components=30, loss='warp')
    model.fit_partial(
            Mui_tr, item_features = Mui_if, user_features=Mui_uf,
            epochs=30,
            verbose=True)
    
    return(model, d_ui, all_course_club_unique, all_products_club_unique, courses, products)

