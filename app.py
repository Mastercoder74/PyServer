from flask import Flask

from flask_cors import CORS, cross_origin

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

app = Flask(__name__)

CORS(app, support_credentials=True)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    _formArray = _json['formArray']

    if _name and _email and _password and _formArray and request.method == 'POST':

        id = mongo.db.user.insert_one({'name':_name, 'email':_email, 'pwd':_password, 'formArray':_formArray})

        resp = jsonify("User Added Successfully!")

        resp.status_code = 200

        return resp

    else:
        return not_found()

@app.route('/users')
@cross_origin(supports_credentials=True)
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
@cross_origin(supports_credentials=True)
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User Deleted Successfully!")
    resp.status_code = 200
    return resp

@app.route('/update/<id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'PUT':

        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':_name, 'email':_email, 'pwd':_password}})

        resp = jsonify("User Updated Successfully!")

        resp.status_code = 200

        return resp

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': request.url + ' is not found.'
    }

    resp = jsonify(message)

    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True)