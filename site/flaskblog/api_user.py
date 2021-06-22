import json, requests
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash
from flaskblog import app, db
from flaskblog.models import Site, Hotel, Promo 
from .utils import *

@app.route('/api/user', methods=['GET'])
@token_required
def get_current_user(current_user):
    role = get_user_role(current_user)
    user = {}
    if role == 'site':
        user = site_to_dict(current_user)
    elif role == 'hotel':
        user = hotel_to_dict(current_user)
    user['role'] = role;
    return jsonify(user), 200

@app.route('/api/token', methods=['POST'])
def get_token():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'Credenciais inválidas',
            403,
            {'WWW-Authenticate' : 'Basic realm="Precisa estar logado"'})

    user = get_user_via_username(auth.username)
    if not user:
        return jsonify({'message':'Credenciais invalidas.'}), 403

    # Geração de token para validar requisições para a API
    if check_password_hash(user.senha, auth.password): 
        token = generate_token(user)
        return jsonify({'token': token, 'role': get_user_role(user), 'username': auth.username}), 200

    return jsonify({'message':'Credenciais invalidas.'}), 403