__author__ = 'galleani'
from flask import Flask, request, jsonify, make_response
from utils import get_responsaveis, get_responsavel, create_responsavel, edit_responsavel, delete_responsavel, \
    get_all_situacao

app = Flask(__name__)


@app.route('/responsaveis/find-all', methods=['POST'])
def find_all():
    input_data = dict(request.json) if request.data else {}
    name = input_data.get('nome') if input_data.get('nome')  else ''
    email = input_data.get('email') if input_data.get('email')  else ''
    cpf = input_data.get('cpf') if input_data.get('cpf')  else ''
    page = int(request.args.get('page')) if request.args.get('page') else 0
    size = int(request.args.get('size')) if request.args.get('size') else 10

    response = get_responsaveis(nome=name,email=email, cpf=cpf, page=page, size=size)
    return jsonify(response)


@app.route('/responsaveis/<int:responsavel_id>', methods=['GET', 'PUT', 'DELETE'])
def responsavel(responsavel_id):
    if request.method == 'GET':
        response = get_responsavel(responsavel_id)
        return jsonify(response)
    elif request.method == 'PUT':
        input_data = dict(request.json) if request.data else {}
        nome = input_data.get('nome') if input_data.get('nome')  else ''
        email = input_data.get('email') if input_data.get('email')  else ''
        cpf = input_data.get('cpf') if input_data.get('cpf')  else ''
        data_nascimento = input_data.get('data_nascimento') if input_data.get('data_nascimento')  else ''

        edited, response = edit_responsavel(responsavel_id=responsavel_id,
                                             nome=nome, email=email, cpf=cpf, data_nascimento=data_nascimento)
        if edited:
            return 'OK'
        else:
            return jsonify(response), 400
    elif request.method == 'DELETE':
        deleted, response = delete_responsavel(responsavel_id)
        if deleted:
            return 'OK'
        else:
            return jsonify(response), 400


@app.route('/responsaveis/', methods=['POST'])
def set_responsavel():
    input_data = dict(request.json) if request.data else {}
    nome = input_data.get('nome') if input_data.get('nome')  else ''
    email = input_data.get('email') if input_data.get('email')  else ''
    cpf = input_data.get('cpf') if input_data.get('cpf')  else ''
    data_nascimento = input_data.get('data_nascimento') if input_data.get('data_nascimento')  else ''
    created, response = create_responsavel(nome=nome, email=email, cpf=cpf, data_nascimento=data_nascimento)
    if created:
        resp = make_response('Created')
        resp.headers['Location'] = response
        return resp, 201
    else:
        return jsonify(response), 400


@app.route('/situacoes', methods=['GET'])
def find_all_situaao():
    response = get_all_situacao()
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
