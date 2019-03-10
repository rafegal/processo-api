__author__ = 'galleani'
import re

from models import Situacao, Responsavel, get_max_responsavel_id, get_existing_cpf_responsavel, \
    get_existing_email_responsavel, get_existing_processo_responsavel
from datetime import datetime, timedelta
from constants import VALIDATIONS_RESPONSE, VALIDATION_NAME_REQUIRED, VALIDATION_NAME_MAX_REQUIRED, \
                      VALIDATION_CPF, VALIDATION_CPF_DUPLICATED, VALIDATION_CPF_REQUIRED, VALIDATION_DATA_NASCIMENTO, \
                      VALIDATION_EMAIL, VALIDATION_EMAIL_DUPLICATED, VALIDATION_EMAIL_MAX_REQUIRED, \
                      VALIDATION_EMAIL_REQUIRED, VALIDATION_ID_EXISTS, VALIDATION_LINKED_PROCESS, URL_RESP


def valida_responsavel(nome, email, cpf, data_nascimento, responsavel_id=None):
    validated_email = lambda email_verified: \
                                re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                         email_verified)

    list_error = []
    status = True

    if not nome:
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_NAME_REQUIRED])
    elif len(nome) > 75:
            list_error.append(VALIDATIONS_RESPONSE[VALIDATION_NAME_MAX_REQUIRED])

    if not cpf:
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_CPF_REQUIRED])
    elif len(cpf) != 11 or not str(cpf).isdigit():
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_CPF])
    elif get_existing_cpf_responsavel(cpf, responsavel_id):
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_CPF_DUPLICATED])

    if not email:
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_EMAIL_REQUIRED])
    elif not validated_email(email):
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_EMAIL])
    elif len(email) > 65:
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_EMAIL_MAX_REQUIRED])
    elif get_existing_email_responsavel(email, responsavel_id):
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_EMAIL_DUPLICATED])

    if data_nascimento and data_nascimento > datetime.now() - timedelta(days=1):
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_DATA_NASCIMENTO])

    if list_error:
        status = False

    return status, list_error

def create_responsavel(nome, email, cpf, data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y') if data_nascimento else ''
    validated, response = valida_responsavel(nome, email, cpf, data_nascimento)
    if not validated:
        return validated, response

    max_id = get_max_responsavel_id() + 1

    responsavel = Responsavel(id=max_id,
                              nome=nome,
                              cpf=cpf,
                              email=email,
                              data_nascimento=data_nascimento)
    responsavel.save()
    return True, 'http://127.0.0.1:5000/responsaveis/{}'.format(max_id)

def edit_responsavel(responsavel_id, nome, email, cpf, data_nascimento):
    response = []
    data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y') if data_nascimento else ''
    responsavel = Responsavel.query.filter_by(id=responsavel_id).first()
    if not responsavel:
        response.append(VALIDATIONS_RESPONSE[VALIDATION_ID_EXISTS])
        return False, response

    validated, response = valida_responsavel(nome, email, cpf, data_nascimento, responsavel_id)
    if not validated:
        return validated, response

    max_id = get_max_responsavel_id() + 1

    responsavel.nome = nome
    responsavel.cpf = cpf
    responsavel.email = email
    responsavel.data_nascimento = data_nascimento
    responsavel.save()

    return True, URL_RESP.format(max_id)


def get_responsavel(responsavel_id):
    responsavel = Responsavel.query.filter_by(id=responsavel_id).first()
    if responsavel:
        response = {
            'id': responsavel.id,
            'cpf': responsavel.cpf,
            'data_nascimento': datetime.strftime(responsavel.data_nascimento, '%d/%m/%Y') if responsavel.data_nascimento else '',
            'email': responsavel.email,
            'nome': responsavel.nome
        }
    else:
        response = {}
    return response

def delete_responsavel(resp_id):
    list_error = []
    responsavel = Responsavel.query.filter_by(id=resp_id).first()
    if not responsavel:
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_ID_EXISTS])
    elif get_existing_processo_responsavel(resp_id):
        list_error.append(VALIDATIONS_RESPONSE[VALIDATION_LINKED_PROCESS])

    if list_error:
        return False, list_error
    else:
        responsavel.delete()
        return True, list_error


def get_responsaveis(nome, email, cpf, page, size):
    page_calc = page + 1
    end = page_calc * size if page_calc > 0 else size
    ini = end - size
    responsaveis =  Responsavel.query.filter(Responsavel.nome.ilike('%{}%'.format(nome)),
                                             Responsavel.email.ilike('%{}%'.format(email)),
                                             Responsavel.cpf.like('%{}%'.format(cpf))).all()
    total = len(responsaveis)
    responsaveis = responsaveis[ini:end]
    records = []
    for resp in responsaveis:
        records.append({
                         'cpf': resp.cpf,
                         'nome': resp.nome,
                         'email': resp.email,
                         'id': resp.id,
                         'data_nascimento': datetime.strftime(resp.data_nascimento, '%d/%m/%Y')
                                                                    if resp.data_nascimento else ''
        })
    response = {'records':records, 'records_number':total}
    return response


def get_all_situacao():
    situacao = Situacao.query.filter().all()
    list_situacao = []
    for s in situacao:
        list_situacao.append({
            'finalizado':s.finalizado,
            'id': s.id,
            'nome': s.nome
        })
    return list_situacao
