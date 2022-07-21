import database
import pymongo

if __name__ == '__main__':
    db = database.DataBase()
    result = db.database['Book'].find().sort([('rating', pymongo.DESCENDING)])
    for i in result:
        print(i)
    print(len(list(result.clone())))
    print(list(result.clone()))
