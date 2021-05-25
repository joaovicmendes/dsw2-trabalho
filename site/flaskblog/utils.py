import datetime as dt
import jwt
from flask import jsonify, request
from functools import wraps
from . import app
from .models import *
from collections import OrderedDict

def generate_token(user):
    ''' 
        Geração de token para verificação na API. Utiliza 'jwt.encode()'
    '''
    return jwt.encode(
        {
            'id'  : user.id,
            'usr' : get_user_username(user),
            'exp' : dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256")

def get_user_via_username(username):
    ''' 
        Tenta recuperar um usuário do banco de dados na seguinte ordem:
        1) Admin
        2) Hotel
        3) Site
    '''
    user = None
    # user = User.query.filter_by(username=username).first()
    if not user:
        user = Hotel.query.filter_by(cnpj=username).first()
    if not user:
        user = Site.query.filter_by(endereco=username).first()
    return user

def get_user_username(user):
    ''' 
        Retorna o username baseado no tipo do usuário:
        1) Admin > username
        2) Hotel > cnpj
        3) Site  > endereco
    '''
    username = None
    # if type(user) == User:
    #     username = user.username
    if type(user) == Hotel:
        username = user.cnpj
    if type(user) == Site:
        username = user.endereco
    return username

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify({'message': 'Token inexistente.'}), 400
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            user = get_user_via_username(data['usr'])
        except:
            return jsonify({'message': 'Token inválido.'}), 400

        return f(user, *args, **kwargs)
    return decorated

def get_user_role(user):
    # if type(user) == User:
    #     return "user"
    if type(user) == Hotel:
        return "hotel"
    elif type(user) == Site:
        return "site"

    return None

def unauthorized_access():
    return jsonify({'message': 'Acesso não autorizado.'}), 401

def get_session_context(session):
    context = {}
    if session:
        try:
            context['username'] = session['username']
            context['logado'] = session['logado']
            context['token'] = session['temp_token']
            context['role'] = session['role']
        except KeyError:
            pass
    return context

def site_to_dict(site):
    site_dict = {}
    site_dict['id'] = site.id
    site_dict['nome'] = site.nome
    site_dict['endereco'] = site.endereco
    # site_dict['senha'] = site.senha
    site_dict['telefone'] = site.telefone
    return site_dict

def hotel_to_dict(hotel):
    hotel_dict = {}
    hotel_dict['id'] = hotel.id
    hotel_dict['nome'] = hotel.nome
    hotel_dict['cnpj'] = hotel.cnpj
    # hotel_dict['senha'] = hotel.senha
    hotel_dict['cidade'] = hotel.cidade
    return hotel_dict

#Tratamento, reordenação e formatação da tabela,
def filter_table(data, type, forbidden_fields=[]):
    #Retira campos secretos (id e senha)
    for d in data:
        if forbidden_fields:
            for f in forbidden_fields:
                _ = d.pop(f)
    

    #Define a ordem das colunas de cada tabela
    if type == 'hotel':
        order = ['nome', 'cidade','cnpj']
    elif type == 'site':
        order = ['nome', 'endereco','telefone']
    elif type =='promo':
        order = ['site', 'cnpj','preco','inicio','fim']
        

    #Reordena as colunas das tabelas
    _data = list()
    for d in data:
        ordered = OrderedDict()
        for k in order:
             ordered[k] = d[k]
        _data.append(dict(ordered))
    data = _data

    table_headers = list() #as chaves no header da tabela
    table_data = list() #as informaçes para mostrar na tabela
    
    #Formata o nome dos campos 
    if data:
        table_headers = list(data[0].keys())
        table_headers = [t.capitalize() for t in table_headers]
    for i,el in enumerate(table_headers):
        if el == "Cnpj":
            table_headers[i] = "CNPJ"
        if el == "Preco":
            table_headers[i] = "Preço"
        if el=='Inicio':
            table_headers[i] = "Início"
    
    #Recebe o conteúdo da tabela
    for promo in data:
        table_data.append(list(promo.values()))
    
    #Formata cada campo da tabela
    new_data = []
    for row_data in table_data:
        new_row = []
        for data,hdr in zip(row_data, table_headers):
            new_row.append(format_data(data,hdr))
        new_data.append((new_row))
    
    return table_headers, new_data


#Funcção auxiliar para formatação dos campos da tabela
def format_data(data, header):
    if header == 'CNPJ':
        return (data[:2] + '.' + data[2:5] + '.' + data[5:8] + '/' 
                + data[8:12] + '-' + data[12:])
    if header == 'Preço':
        return 'R$ ' + str(data)
    if header == 'Telefone':
        return '('+ data[:2] + ')'+data[2:4]+' '+data[4:9] + '-' + data[9:]
    if header == 'Início' or header == 'Fim':
        return data[:16]

    
    return data
