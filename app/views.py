from flask import Flask, request, jsonify, abort
from app import app


# static url
@app.route('/')
def index():
    return "Hello Karan!"


data = [
    {
        'id' : 1,
        'name' : u'cat1',
        'type' : u'cats'
        
    },
    {
        'id' : 2,
        'name' : u'cat2',
        'type' : u'cats'
        
    },
    {
        'id' : 1,
        'name' : u'dog1',
        'type' : u'dogs'
    },
    {
        'id' : 2,
        'name' : u'dog2',
        'type' : u'dogs'
        
    },
    {
        'id' : 1,
        'name' : u'human1',
        'type' : u'humans'
        
    },
    {
        'id' : 2,
        'name' : u'human2',
        'type': u'humans'
    }
]

# api with endpoint
@app.route('/getdata', methods=['GET'])
def getdata():
    return jsonify({'data' : data})
@app.route('/getdata/<data_type>', methods=['GET'])
def get_data_type(data_type):
    data_return = [data for data in data if data['type'] == data_type]
    if len(data_return) == 0:
        abort(400, description = "There is no data type " + data_type + " in our database")
    else:
        return jsonify({'data' : data_return[:]})
@app.route('/getdata/<data_type>/<data_id>', methods=['GET'])
def get_data_type_id(data_id, data_type):
    data_return = [data for data in data if data['type'] == data_type]
    if len(data_return) == 0:
        abort(400, description = "There is no data type " + data_type + " in our database")
    data_id_return = [did for did in data_return if did['id'] == int(data_id)]
    if len(data_id_return) == 0:
        abort(400, description = "There is no " + data_type + " with the id " + data_id + " in our database would you like to add it" + " <a href=\"/postdata/\"> add data </a>" + data_type)
    else:
        return jsonify({'data' : data_id_return[:]})

@app.route('/postdata/<data_type>', methods=['POST'])
def create_data(data_type):
    if request.json is None or 'name' not in request.json.keys():
        abort(400, description = "Please specify a name for the " + data_type)

    data_return = [data for data in data if data['type'] == data_type]
    if len(data_return) == 0:
        abort(400, description = "There is no data type " + data_type + " in our database")
    data_return = {
        'id': data_return[-1]['id'] + 1,
        'name': request.json['name'],
        'type': data_type
    }
    data.append(data_return)
    return jsonify({'data': data})

@app.route('/modifydata/<data_type>', methods=['PUT'])
def modify_data(data_type):
    if data_type == 'cats' or data_type == 'dogs':
        if request.json is None or 'id' not in request.json.keys():
            abort(400, description = "Please specify an id for the " + data_type)
        data_return = [data for data in data if data['type'] == data_type]
        if len(data_return) == 0:
            abort(400, description = "There is no data type " + data_type + " in our database")
        data_id_return = [did for did in data_return if did['id'] == int(request.json['id'])]
        data_id_return[0]['name'] = request.json['name']
        return jsonify({'data': data})
    else:
        abort(400, description = data_type + " is not modifiable")

@app.route('/deletedata/<data_type>', methods=['DELETE'])
def delete_data(data_type):
    if data_type == 'humans' or data_type == 'dogs':
        abort(400, description = data_type+" is not deletable")
    data_return = [data for data in data if data['type'] == data_type]
    if len(data_return) == 0:
        abort(400, description = "There is no data type " + data_type + " in our database")
    if request.json is None or 'id' not in request.json.keys():
        abort(400, description = "Please specify an id for the " + data_type)
    id_to_delete = int(request.json['id'])
    data.remove(data_return[:][id_to_delete])
    return jsonify({'result': True})
