from flask_restful import Resource #import library
from models.store import StoreModel # import from models folder

# will extend the resource class
class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        # creating a new store :
        store = StoreModel(name)
        try:
            store.save_to_db() #saving it to database
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201 #return Json &  201, it has been created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
