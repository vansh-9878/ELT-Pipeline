from MongoDB.createDatasets import createNewRecords
from MongoDB.loadData import insert
from MongoDB.mergeDatasets import mergeIntoOne

def start():
    createNewRecords()
    mergeIntoOne()
    insert()
    
# start()