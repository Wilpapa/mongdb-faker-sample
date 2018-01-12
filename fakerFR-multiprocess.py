# sample use of faker lib / GM@Mongo 20170701

# let's import all libraries (Mongo and Faker)
import pymongo
from pymongo.errors import BulkWriteError
from faker import Factory
from multiprocessing import Process
import time
#Number of processes to launch
processesNumber = 16
processesList = []

#Settings pour Faker
fake = Factory.create('fr_FR') # using french names, cities, etc.

#batch size and bulk size
batchSize=1000000
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
            print('%s - process %s - records %s '% (time.strftime("%H:%M:%S"),processId,i))

        if (i%bulkSize == (bulkSize-1)): #bulk write
            try:
                bulk.execute()
            except BulkWriteError as bwe:
                pprint(bwe.details)
            bulk = customers.initialize_unordered_bulk_op() #and reinit the bulk op

        # Fake customer info - this is where you build your people document
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
