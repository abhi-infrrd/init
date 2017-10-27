import pandas as pd
import os
import argparse
import pymongo
import tqdm
import glob


#TODO: Filename extraction
#TODO: Logging

def insertion_to_mongo(filenames):

        # Insert product master list to MongoDB
        products_master_list = pd.read_csv(filenames[1],sep = '\t', encoding="ISO-8859-1")
        collection_name = "CPA_PRODUCTS_META"
        CPA_PRODUCTS_META = db[collection_name]
        for idx, rows in tqdm.tqdm(products_master_list.iterrows()):
            CPA_PRODUCTS_META.insert(
                        {
                            "_id": rows[0],
                            "metadata": rows[1:].to_dict()
                        }
            )

        # Insert courses master list
        course_master_list = pd.read_csv(filenames[0], sep='\t', encoding="ISO-8859-1")
        collection_name = "CPA_COURSES_META"
        CPA_COURSES_META = db[collection_name]

        for idx, rows in tqdm.tqdm(course_master_list.iterrows()):
            CPA_COURSES_META.insert({
                        "_id":rows[0],
                        "metadata":rows[3:].to_dict()
                       }
            )
            if (idx+1)%100 == 0:
                print('{} Records are inserted'.format(idx+1) )

        # Insert users master list
        user_master_list = pd.read_csv(filenames[2], sep = '\t', encoding="ISO-8859-1")
        collection_name = "CPA_USERS"
        CPA_USERS = db[collection_name]
        for idx,rows in tqdm.tqdm(user_master_list.iterrows()):
            CPA_USERS.insert({
                         "_id": rows[0],
                         "metadata": rows[1:].to_dict()

            })
            if (idx+1)%100 == 0:
                print('{} Records are inserted'.format(idx+1))


if __name__ == "__main__":
    db_name = "muse"
    client = pymongo.MongoClient()
    db = client[db_name]

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', help=" Full path to where the files are stored", required=True)
    args = parser.parse_args()
    try:
        os.chdir(args.input_folder)
        file_list = glob.glob("*.csv")
        file_list.sort()
        insertion_to_mongo(file_list)
    except:
        raise OSError('Directory does not exist',args.input_folder)




