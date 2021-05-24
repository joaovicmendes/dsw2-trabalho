import datetime as dt
import jwt
from flask import jsonify, request
from functools import wraps
from . import app
from .models import *

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
