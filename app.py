from flask import Flask

app = Flask(__name__)


@app.route('/storage', methods=['POST'])
def create_storage():
    pass


@app.route('/storage/<string:storage_name>')
def retrieve_storage(storage_name):
    pass


@app.route('/storage')
def get_storage_list():
    pass


@app.route('/storage/<storage_name>/cargos', methods=['POST'])
def create_cargo(storage_name):
    pass


@app.route('/storage/<storage_name>/cargos')
def get_cargo_list(storage_name):
    pass


app.run(port=5001)
