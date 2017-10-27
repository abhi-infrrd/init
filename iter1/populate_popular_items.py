from __future__ import division
from bson.son import SON
import pymongo

client = pymongo.MongoClient()
db = client["muse"]
pipeline = [
    {"$group": {"_id": "$itemId", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])},
    {"$project": {"count": "$count"}}
]

result = db["CPA_PRODUCTS_INTERACTIONS"].aggregate(pipeline)
toInsert = []
for item in (list(result)):
    itemId = item["_id"]
    meta = db["CPA_PRODUCTS_META"].find_one({"_id": itemId})
    if meta != None:
        record = item.copy()
        record["Type"] = meta["Type"]
        record["EventStartDate"] = meta["EventStartDate"]
        record["EventEndDate"] = meta["EventEndDate"]
        record["AllFieldOfStudy"] = meta["AllFieldOfStudy"]
        record["Keywords"] = meta["Keywords"]
        record["Topic"] = meta["Topic"]
        toInsert.append(record)

count_list = [x['count'] for x in toInsert]
max_count = max(count_list)

for record in toInsert:
    record['score'] = record['count']/max_count

db["CPA_PRODUCTS_POPULAR"].remove({})

print ("Inserting " + str(len(toInsert)) + " records")
db["CPA_PRODUCTS_POPULAR"].insert(toInsert)

result = db["CPA_COURSES_INTERACTIONS"].aggregate(pipeline)
toInsert = []
for item in list(result):
 itemId = item["_id"]
 meta = db["CPA_COURSES_META"].find_one({"_id":itemId})
 if meta != None:
  record = item.copy()
  record["Type"] = meta["Type"]
  record["EventStartDate"] = meta["EventStartDate"]
  record["EventEndDate"] = meta["EventEndDate"]
  record["AllFieldOfStudy"] = meta["AllFieldOfStudy"]
  record["Keywords"] = meta["Keywords"]
  record["Topic"] = meta["Topic"]
  toInsert.append(record)

count_list = [x['count'] for x in toInsert]
max_count = max(count_list)

for record in toInsert:
    record['score'] = record['count']/max_count
db["CPA_COURSES_POPULAR"].remove({})

print ("Inserting " + str(len(toInsert)) + " records")

db["CPA_COURSES_POPULAR"].insert(toInsert)
