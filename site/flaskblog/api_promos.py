import json, requests
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash
from flaskblog import app, db
from flaskblog.models import Site, Hotel, Promo 
from .utils import *

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
