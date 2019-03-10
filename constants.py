__author__ = 'rafeg'

URL_RESP = '/responsaveis/{}'

VALIDATION_NAME_REQUIRED = 'name_required'
VALIDATION_NAME_MAX_REQUIRED = 'max_name'
VALIDATION_CPF_REQUIRED = 'cpf_required'
VALIDATION_CPF = 'cpf_validated'
VALIDATION_CPF_DUPLICATED = 'cpf_duplicated'
VALIDATION_EMAIL_REQUIRED = 'email_required'
VALIDATION_EMAIL = 'email_validated'
VALIDATION_EMAIL_MAX_REQUIRED = 'max_email'
VALIDATION_EMAIL_DUPLICATED = 'email_duplicated'
VALIDATION_DATA_NASCIMENTO = 'data_nascimento_validated'
VALIDATION_ID_EXISTS = 'responsavel_noneexistent'
VALIDATION_LINKED_PROCESS = 'linked_process'

VALIDATIONS_RESPONSE = {
    VALIDATION_NAME_REQUIRED:{
        'local_erro': 'responsavel.nome', 
        'erro' :'obrigatorio', 
        'mensagem': 'O nome é obrigatório', 
        'args': [] 
    },
    VALIDATION_NAME_MAX_REQUIRED:{
        'local_erro': 'responsavel.nome',
        'erro' :'tamanhoMaximo',
        'mensagem': 'O nome deve possuir no máximo {} caracteres',
        'args': [75]
    },
    VALIDATION_CPF_REQUIRED:{
        'local_erro': 'responsavel.cpf',
        'erro' :'obrigatorio',
        'mensagem': 'O CPF é obrigatório',
        'args': []
    },
    VALIDATION_CPF:{
        'local_erro': 'responsavel.cpf',
        'erro' :'invalido',
        'mensagem': 'O CPF é inválido, o CPF deve possuir exatamente {} caracteres numéricos',
        'args': [11]
    },
    VALIDATION_CPF_DUPLICATED:{
        'local_erro': 'responsavel.cpf',
        'erro' :'duplicado',
        'mensagem': 'O CPF é duplicado, já existe outro responsável com o CPF informado	',
        'args': []
    },
    VALIDATION_EMAIL_REQUIRED:{
        'local_erro': 'responsavel.email',
        'erro' :'obrigatorio',
        'mensagem': 'O e-mail é obrigatório',
        'args': []
    },
    VALIDATION_EMAIL:{
        'local_erro': 'responsavel.email',
        'erro' :'invalido',
        'mensagem': 'O e-mail informado é inválido',
        'args': []
    },
    VALIDATION_EMAIL_MAX_REQUIRED:{
        'local_erro': 'responsavel.email',
        'erro' :'tamanhoMaximo',
        'mensagem': 'O e-mail deve possuir no máximo {} caracteres',
        'args': [65]
    },
    VALIDATION_EMAIL_DUPLICATED:{
        'local_erro': 'responsavel.email',
        'erro' :'duplicado',
        'mensagem': 'O e-mail é duplicado, já existe outro responsável com o e-mail informado',
        'args': []
    },
    VALIDATION_DATA_NASCIMENTO:{
        'local_erro': 'responsavel.dataNascimento',
        'erro' :'menorDataAtual',
        'mensagem': 'A data de nascimento deve ser menor que a data atual',
        'args': []
    },
    VALIDATION_ID_EXISTS:{
        'local_erro': 'responsavel.id',
        'erro' :'inexistente',
        'mensagem': 'O responsável é inexistente',
        'args': []
    },
    VALIDATION_LINKED_PROCESS:{
        'local_erro': 'responsavel.processo',
        'erro' :'vinculadoProcesso',
        'mensagem': 'O responsável está vinculado a um processo, não é possivel remover',
        'args': []
    }
}
