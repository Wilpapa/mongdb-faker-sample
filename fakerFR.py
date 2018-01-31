# sample use of faker lib / GM@Mongo 20170701

# let's import all libraries (Mongo and Faker)
import pymongo
from pymongo.errors import BulkWriteError
from faker import Factory
import time
fake = Factory.create('fr_FR') # using french names, cities, etc.

#bacth size and bulk size
batchSize=3000000
bulkSize=10000

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the database
db = connection.company
customers = db.customers

bulk = customers.initialize_unordered_bulk_op()

# let's insert xM records
for i in range(batchSize):
    if (i%bulkSize== 0): #print every bulk writes
        print('%s - records %s '% (time.strftime("%H:%M:%S"),i))

    if (i%bulkSize == (bulkSize-1)): #bulk write
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            pprint(bwe.details)
        bulk = customers.initialize_unordered_bulk_op()

    # Fake customer info
    addr=fake.address()
    addrstreet=addr.split("\n")
    addrcity=addrstreet[1]
    # Create customer record
    try:
        result=bulk.insert({
                            "name":fake.name(),
                            "ssn":fake.ssn(),
                            "job":fake.job(),
                            "phone":[
                                    {"home":fake.phone_number()},
                                    {"cell":fake.phone_number()}
                            ],
                            "address":{
                                        "street":addrstreet[0],
                                        "city":addrcity
                            }
        })
    except Exception as e:
        print "insert failed:", i, " error : ", e
