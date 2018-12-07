# sample use of faker lib / GM@Mongo 20170701
#https://faker.readthedocs.io/en/master/
#https://faker.readthedocs.io/en/master/providers/faker.providers.address.html -

# let's import all libraries (Mongo and Faker)
import pymongo
from pymongo.errors import BulkWriteError
from faker import Factory
from multiprocessing import Process
import time
import random

#Number of processes to launch
processesNumber = 8
processesList = []

#Settings for Faker, change locale to create other language data
fake = Factory.create('fr_FR') # using french names, cities, etc. // fr_FR is almost 10 times faster than en_US

#batch size and bulk size
batchSize=125001
bulkSize=1000

def run(processId):
    # establish a connection to the database
    connection = pymongo.MongoClient("mongodb://localhost")

    # get a handle to the database, and start a bulk op
    db = connection.world
    customers = db.people
    bulk = customers.initialize_unordered_bulk_op()

    # let's insert batchSize records
    for i in range(batchSize):
        if (i%bulkSize== 0): #print every bulkSize writes
            print('%s - process %s - records %s \n'% (time.strftime("%H:%M:%S"),processId,i))

        if (i%bulkSize == (bulkSize-1)): #bulk write
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                pprint(bwe.details)
            bulk = customers.initialize_unordered_bulk_op() #and reinit the bulk op

        # Fake person info - this is where you build your people document
        # Create customer record
        try:
            result=bulk.insert({
                                "process":processId,
                                "index":i,
                                "lastName":fake.last_name(),
                                "firstName":fake.first_name(),
                                "ssn":fake.ssn(),
                                "job":fake.job(),
                                "phone":[
                                        {"type":"home","number":fake.phone_number()},
                                        {"type":"cell","number":fake.phone_number()}
                                ],
                                "address":{
                                            "street":fake.street_address(),
                                            "city":fake.city()
                                },
                                "revenue": random.randint(50000,250000),
                                "age": random.randint(20,60),
            })
        except Exception as e:
            print "insert failed:", i, " error : ", e

if __name__ == '__main__':
    # Creation of processesNumber processes
    for i in range(processesNumber):
        process = Process(target=run, args=(i,))
        processesList.append(process)

    # launch processes
    for process in processesList:
        process.start()


    # wait for processes to complete
    for process in processesList:
        process.join()
