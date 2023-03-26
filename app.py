from flask import Flask, jsonify, request

app = Flask(__name__)

storages = [
    {
        'name': 'Sattarkhan',
        'cargos': [
            {
                'name': '10kg rice bag',
                'quantity': 5
            },
            {
                'name': '200g tea box',
                'quantity': 11
            }
        ]
    },
    {
        'name': 'Koshtargah',
        'cargos': [
            {
                'name': 'Gucci Bag',
                'quantity': 55
            }
        ]
    }
]


@app.route('/storages', methods=['POST'])
def create_storage():
    request_data = request.get_json()
    new_storage = {
        'name': request_data['name'],
        'cargos': []
    }
    storages.append(new_storage)
    return jsonify(new_storage)


@app.route('/storages/<string:storage_name>')
def retrieve_storage(storage_name):
    for storage in storages:
        if storage['name'] == storage_name:
            return jsonify(storage)
    return jsonify({'message': 'not found'})


@app.route('/storages')
def get_storage_list():
    return jsonify({'storages': storages})


@app.route('/storages/<storage_name>/cargos', methods=['POST'])
def create_cargo(storage_name):
    request_data = request.get_json()
    for storage in storages:
        if storage['name'] == storage_name:
            new_cargo = {
                'name': request_data['name'],
                'quantity': request_data['quantity']
            }
            storage['cargos'].append(new_cargo)
            return jsonify(new_cargo)
    return jsonify({'message': 'not found'})


@app.route('/storages/<storage_name>/cargos')
def get_cargo_list(storage_name):
    pass


app.run(port=5001)
