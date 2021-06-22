import json, requests
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash
from flaskblog import app, db
from flaskblog.models import Site, Hotel, Promo 
from .utils import *

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
