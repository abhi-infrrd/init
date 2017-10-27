import pandas as pd
import pymongo
import datetime
import logging
import argparse
import config
client = pymongo.MongoClient()
db = client["muse"]

print("Reading files")
products_master_list = pd.read_csv(config.product_file["file_name"],
                                   sep='\t', encoding=config.product_file["encoding"])
products_int_list = pd.read_csv(config.product_order_summary_file["file_name"],
                                sep='\t', encoding=config.product_order_summary_file["encoding"])
sub_products_int_list = pd.read_csv(
    config.user_subscriptions_file["file_name"], sep='\t', encoding=config.user_subscriptions_file["encoding"])
courses_int_list = pd.read_csv(
    config.user_enrollments_completions_file["file_name"], sep='\t',
    encoding=config.user_enrollments_completions_file["encoding"])

mpm = {}
pRecords = []
cRecords = []
num = 0
failnum = 0


def insertToDB(records, collectionName):
    coll = db[collectionName]
    print ("Inserting " + str(len(records)) + " items to DB")
    coll.insert(records)


print("Parsing files")
for idx, row in products_master_list.iterrows():
    pc = row["ProductCode"]
    skuId = row["SkuID"]
    try:
        Dt = datetime.strptime(row['EventStartDate'], '%Y-%m-%d %H:%M').isoformat()
    except:
        Dt = None
    global mpm
    mpm[skuId] = pc

for idx, row in products_int_list.iterrows():
    skuId = row["SkuID"]
    userId = row["EncryptedRecordID"]
    try:
        Dt = datetime.strptime(row['OrderDate'], '%Y-%m-%d %H:%M').isoformat()
    except:
        Dt = None
    global mpm, num, failnum

    pc = ""
    if skuId in mpm:
        pc = mpm[skuId]
        num = num + 1
        global pRecords
        pRecords.append({
            "userId": userId,
            "itemId": pc,
            "Dt": Dt
        }
        )
    else:
        failnum = failnum + 1

print("Found " + str(num) + " records from order summary")
print("Found " + str(failnum) + " bad records from order summary")

num = 0
failnum = 0

for idx, row in sub_products_int_list.iterrows():
    skuId = row["SkuID"]
    userId = row["EncryptedUserID"]
    try:
        Dt = datetime.strptime(row['SubsStartDate'], '%Y-%m-%d %H:%M').isoformat()
    except:
        Dt = None
    global mpm, num, failnum
    pc = ""
    if skuId in mpm:
        num = num + 1
        pc = mpm[skuId]
        global pRecords
        pRecords.append({
            "userId": userId,
            "itemId": pc,
            "Dt": Dt
        }
        )
    else:
        failnum = failnum + 1

print("Found " + str(num) + " records from subscriptions")
print("Found " + str(failnum) + " bad records from subscriptions")

num = 0
failnum = 0

for idx, row in courses_int_list.iterrows():
    cc = row["CourseCode"]
    userId = row["EncryptedRecordID"]
    try:
        Dt = datetime.strptime(row['EnrollDate'], '%Y-%m-%d %H:%M').isoformat()
    except:
        Dt = None
    global num, failnum
    num = num + 1
    global cRecords
    cRecords.append({
        "userId": userId,
        "itemId": cc,
        "Dt": Dt
    }
    )

print("Found " + str(num) + " records from course enrollments")
print("Found " + str(failnum) + " bad records from course enrollments")

insertToDB(pRecords, "CPA_PRODUCTS_INTERACTIONS")
insertToDB(cRecords, "CPA_COURSES_INTERACTIONS")



"""
    TODO:
    2. Add Log statements after appropriate steps( import logging)
    3. Add a main module statement( if __name__ == "__main__") and create mongo client there if there is no dependency in other modules.
    4. Reuse code ( like reading  file)
    5. follow PEP 8 coding practice.

"""