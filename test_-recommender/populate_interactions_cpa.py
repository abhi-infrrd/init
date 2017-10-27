import pandas as pd
import pymongo
from datetime import datetime
import logging
import argparse
import os
import config

def insertToDB(records, coll):
    print ("Inserting " + str(len(records)) + " items to DB")
    coll.insert(records)

def readAndInsert():
    mpm = {}
    pRecords = []
    cRecords = []
    num = 0
    failnum = 0
    client = pymongo.MongoClient()
    db = client["muse2"]

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

    print("Parsing files")
    for idx, row in products_master_list.iterrows():
        pc = row["ProductCode"]
        skuId = row["SkuID"]
        mpm[skuId] = pc

    for idx, row in products_int_list.iterrows():
        skuId = row["SkuID"]
        userId = row["EncryptedRecordID"]
        try:
            Dt = datetime.strptime(row['OrderDate'], '%m/%d/%y %H:%M')
            print("Got a proper date products_int_list")
        except Exception as e:
            print e
            Dt = None

        pc = ""
        if skuId in mpm:
            pc = mpm[skuId]
            num = num + 1
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
            Dt = datetime.strptime(row['SubsStartDate'], '%m/%d/%y %H:%M')
            print("Got a proper date sub_products_int_list")
        except Exception as e:
            print e
            Dt = None

        pc = ""
        if skuId in mpm:
            num = num + 1
            pc = mpm[skuId]
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
            Dt = datetime.strptime(row['EnrollDate'], '%m/%d/%y %H:%M')
            print("Got a proper date courses_int_list")
        except Exception as e:
            print e
            Dt = None

        num = num + 1
        cRecords.append({
            "userId": userId,
            "itemId": cc,
            "Dt": Dt
        }
        )

    print("Found " + str(num) + " records from course enrollments")
    print("Found " + str(failnum) + " bad records from course enrollments")

    insertToDB(pRecords, db["CPA_PRODUCTS_INTERACTIONS"])
    insertToDB(cRecords, db["CPA_COURSES_INTERACTIONS"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', help=" Full path to where the files are stored", required=True)
    args = parser.parse_args()
    try:
        os.chdir(args.input_folder)
    except Exception as e:
        print e
        raise OSError('Directory does not exist',args.input_folder)
    readAndInsert()



"""
    TODO:
    2. Add Log statements after appropriate steps( import logging)
    3. Add a main module statement( if __name__ == "__main__") and create mongo client there if there is no dependency in other modules.
    4. Reuse code ( like reading  file)
    5. follow PEP 8 coding practice.

"""
