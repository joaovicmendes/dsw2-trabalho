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
        return jsonify({'message':'Nenhuma promoção encontrada'})

    output = []
    for promo in promos:
        hotel = Hotel.query.filter_by(cnpj=promo.hotel_cnpj).first()
        promo_data = {}
        promo_data['id'] = promo.id
        promo_data['site'] = promo.site_end
        promo_data['cnpj'] = promo.hotel_cnpj
        promo_data['hotel'] = hotel.nome
        promo_data['cidade'] = hotel.cidade
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

    hotel = Hotel.query.filter_by(cnpj=promo.hotel_cnpj).first()

    promo_data = {}
    promo_data['id'] = promo.id
    promo_data['site'] = promo.site_end
    promo_data['cnpj'] = promo.hotel_cnpj
    promo_data['hotel'] = hotel.nome
    promo_data['cidade'] = hotel.cidade
    promo_data['preco'] = promo.preco
    promo_data['inicio'] = promo.ini_promo
    promo_data['Fim'] = promo.end_promo
    return jsonify({'promo':promo_data})

@app.route('/api/promocao/hotel/<cnpj>', methods=['GET'])
def get_promo_by_hotel(cnpj):
    cnpj = int(cnpj)
    promos = Promo.query.filter_by(hotel_cnpj=cnpj)

    if not promos:    
        return jsonify({'message':'No hotel found. :('})

    hotel = Hotel.query.filter_by(cnpj=cnpj).first()

    output = []
    for promo in promos:
        promo_data = {}
        promo_data['id'] = promo.id
        promo_data['site'] = promo.site_end
        promo_data['cnpj'] = promo.hotel_cnpj
        promo_data['hotel'] = hotel.nome
        promo_data['cidade'] = hotel.cidade
        promo_data['preco'] = promo.preco
        promo_data['inicio'] = promo.ini_promo
        promo_data['fim'] = promo.end_promo
        output.append(promo_data)
    return jsonify({'promos':output})

@app.route('/api/promocao/site/<site>', methods=['GET'])
def get_promo_by_site(site):
    
    promos = Promo.query.filter_by(site_end=site)

    if not promos:    
        return jsonify({'message':'No hotel found. :('})

    output = []
    for promo in promos:
        hotel = Hotel.query.filter_by(cnpj=promo.hotel_cnpj).first()
        promo_data = {}
        promo_data['id'] = promo.id
        promo_data['site'] = promo.site_end
        promo_data['cnpj'] = promo.hotel_cnpj
        promo_data['hotel'] = hotel.nome
        promo_data['cidade'] = hotel.cidade
        promo_data['preco'] = promo.preco
        promo_data['inicio'] = promo.ini_promo
        promo_data['fim'] = promo.end_promo
        output.append(promo_data)
    return jsonify({'promos':output})

@app.route('/api/promocao', methods=['POST'])
@token_required
def create_promo(current_user):
    data = request.get_json(force=True)
    if not data or not data['nome_site'] or not data['nome_hotel'] or not data['preco']:
        return jsonify({'message':'Campos não preenchidos.'}), 401

    site = Site.query.filter_by(nome=data['nome_site']).first()
    if not site:
        return jsonify({'message':'Site não encontrado.'}), 404
    site_end = site.endereco
        
    hotel = Hotel.query.filter_by(nome=data['nome_hotel']).first()
    if not hotel:
        return jsonify({'message':'Hotel não encontrado.'}), 404
    hotel_cnpj = hotel.cnpj

    try:
        ini = datetime.strptime(data['ini'], '%m/%d/%Y')
        fim = datetime.strptime(data['fim'], '%m/%d/%Y')
    except:
        ini = datetime.now()
        fim = datetime.now()

    new_promo = Promo(site_end= site_end,
                    hotel_cnpj= hotel_cnpj,
                    preco=data['preco'],
                    ini_promo=ini,
                    end_promo=fim)
    db.session.add(new_promo)
    db.session.commit()
    return jsonify({'message' : 'Nova promoção adicionada!'}), 201

@app.route('/api/promocao/<id>', methods=['DELETE'])
@token_required
def delete_promo(current_user, id):
    promo = Promo.query.filter_by(id=id).first()
    if not promo:    
        return jsonify({'message':'No promo found. :('}), 404

    if (get_user_role(current_user) == 'hotel' and current_user.cnpj != promo.hotel_cnpj) or (get_user_role(current_user) == 'site' and current_user.endereco != promo.site_end):
        return unauthorized_access()

    db.session.delete(promo)
    db.session.commit()
    return jsonify({'message':"The promo has been deleted"})
