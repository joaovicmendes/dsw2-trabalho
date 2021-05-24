import json, requests
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
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

# API de Hoteis
@app.route('/api/hotel', methods=['GET'])
def get_all_hotels():
    hoteis = Hotel.query.all()

    output = []
    for hotel in hoteis:
        hotel_data = {}
        hotel_data['id'] = hotel.id
        hotel_data['nome'] = hotel.nome
        hotel_data['cnpj'] = hotel.cnpj
        hotel_data['senha'] = hotel.senha
        hotel_data['cidade'] = hotel.cidade
        output.append(hotel_data)
    return jsonify({'hoteis':output})

@app.route('/api/hotel/<id>', methods=['GET'])
def get_one_hotel(id):
    id = int(id)
    hotel = Hotel.query.filter_by(id=id).first()

    if not hotel:    
        return jsonify({'message':'No hotel found. :('}), 401

    hotel_data = {}
    hotel_data['id'] = hotel.id
    hotel_data['nome'] = hotel.nome
    hotel_data['cnpj'] = hotel.cnpj
    hotel_data['senha'] = hotel.senha
    hotel_data['cidade'] = hotel.cidade
    return jsonify({'hotel':hotel_data})

@app.route('/api/hotel', methods=['POST'])
def create_hotel():
    data = request.get_json()
    hashed_password = generate_password_hash(data['senha'],method='sha256')

    new_hotel = Hotel(nome=data['nome'],
                    cnpj=data['cnpj'],
                    senha=hashed_password,
                    cidade=data['cidade'])
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify({'message' : 'New hotel included.'}), 201

@app.route('/api/hotel/<id>', methods=['DELETE'])
@token_required
def delete_hotel(current_user, id):
    id = int(id)
    if get_user_role(current_user) != 'hotel' or \
     current_user.id != id:
        return unauthorized_access()

    hotel = Hotel.query.filter_by(id=id).first()
    promos = Promo.query.filter_by(hotel_cnpj=hotel.cnpj).all()
    if not hotel:    
        return jsonify({'message':'No hotel found. :('})
    db.session.delete(hotel)
    db.session.commit()
    for promo in promos:
        db.session.delete(promo)
        db.session.commit()
    return jsonify({'message':"The hotel has been deleted"})

# API de Promoções
@app.route('/api/promocao', methods=['GET'])
def get_all_promos():
    promos = Promo.query.all()

    if not promos:    
        return jsonify({'message':'No hotel found. :('})

    output = []
    for promo in promos:
        promo_data = {}
        promo_data['id'] = promo.id
        promo_data['site'] = promo.site_end
        promo_data['cnpj'] = promo.hotel_cnpj
        promo_data['preco'] = promo.preco
        promo_data['inicio'] = promo.ini_promo
        promo_data['fim'] = promo.end_promo
        output.append(promo_data)
    return jsonify({'promos':output})

@app.route('/api/promocao/<id>', methods=['GET'])
def get_one_promo(id):
    id = int(id)
    promo = Promo.query.filter_by(id=id).first()

    if not promo:    
        return jsonify({'message':'No hotel found. :('})

    promo_data = {}
    promo_data['id'] = promo.id
    promo_data['site'] = promo.site_end
    promo_data['cnpj'] = promo.hotel_cnpj
    promo_data['preco'] = promo.preco
    promo_data['inicio'] = promo.ini_promo
    promo_data['Fim'] = promo.end_promo
    return jsonify({'promo':promo_data})

@app.route('/api/promocao', methods=['POST'])
@token_required
def create_promo(current_user):
    data = request.get_json()
    site = Site.query.filter_by(endereco=data['endereco']).first()
    if not site:
        return jsonify({'message':'No site found. :('}), 404
    site_end = site.endereco
        
    hotel = Hotel.query.filter_by(cnpj=data['hotel_cnpj']).first()
    if not hotel:
        return jsonify({'message':'No hotel found. :('}), 404
    hotel_cnpj = hotel.cnpj

    new_promo = Promo(site_end= site_end,
                    hotel_cnpj= hotel_cnpj,
                    preco=data['preco'])
    db.session.add(new_promo)
    db.session.commit()
    return jsonify({'message' : 'New promo included.'}), 201

@app.route('/api/promocao/<id>', methods=['DELETE'])
@token_required
def delete_promo(current_user, id):
    promo = Promo.query.filter_by(id=id).first()
    if not promo:    
        return jsonify({'message':'No promo found. :('}), 404

    if (get_user_role(current_user) == 'hotel' and current_user.cnpj != promo.hotel_cnpj) or\
       (get_user_role(current_user) == 'site' and current_user.endereco != promo.site_end):
        return unauthorized_access()

    db.session.delete(promo)
    db.session.commit()
    return jsonify({'message':"The promo has been deleted"})
