import json, requests
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash
from flaskblog import app, db
from flaskblog.models import Site, Hotel, Promo 
from .utils import *

# API de Sites
@app.route('/api/site', methods=['GET'])
def get_all_sites():
    sites = Site.query.all()

    output = []
    for site in sites:
        site_data = {}
        site_data['id'] = site.id
        site_data['nome'] = site.nome
        site_data['endereco'] = site.endereco
        site_data['senha'] = site.senha
        site_data['telefone'] = site.telefone
        output.append(site_data)
    return jsonify({'sites':output})

@app.route('/api/site/<id>', methods=['GET'])
def get_one_site(id):
    site = Site.query.filter_by(id=id).first()

    if not site:    
        return jsonify({'message':'No site found. :('})

    site_data = {}
    site_data['id'] = site.id
    site_data['nome'] = site.nome
    site_data['endereco'] = site.endereco
    site_data['senha'] = site.senha
    site_data['telefone'] = site.telefone
    return jsonify({'site':site_data})

@app.route('/api/site', methods=['POST'])
def create_site():
    data = request.get_json()
    hashed_password = generate_password_hash(data['senha'],method='sha256')

    new_site = Site(nome=data['nome'],
                    endereco=data['endereco'],
                    senha=hashed_password,
                    telefone=data['telefone'])
    db.session.add(new_site)
    db.session.commit()
    return jsonify({'message' : 'New site included.'}), 201

@app.route('/api/site/<id>', methods=['DELETE'])
@token_required
def delete_site(current_user, id):
    id = int(id)
    if get_user_role(current_user) != 'site' or current_user.id != id:
        return unauthorized_access()

    site = Site.query.filter_by(id=id).first()
    promos = Promo.query.filter_by(site_end=site.endereco).all()
    if not site:
        return jsonify({'message':'No site found. :('})
    db.session.delete(site)
    db.session.commit()
    for promo in promos:
        db.session.delete(promo)
        db.session.commit()
    return jsonify({'message':"The site and all of his promos have been deleted"})
