from flask import render_template, url_for, flash, request, jsonify, make_response
from flaskblog import app, db
from flaskblog.models import Site, Hotel #, Promo 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#SITE REST API
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
    return jsonify({'message' : 'New site included.'})

@app.route('/api/site/<id>', methods=['DELETE'])
def delete_site(id):
    site = Site.query.filter_by(id=id).first()
    if not site:    
        return jsonify({'message':'No site found. :('})
    db.session.delete(site)
    db.session.commit()
    return jsonify({'message':"The site has been deleted"})



#HOTEL REST API
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
    hotel = Hotel.query.filter_by(id=id).first()

    if not hotel:    
        return jsonify({'message':'No hotel found. :('})

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
    return jsonify({'message' : 'New hotel included.'})

@app.route('/api/hotel/<id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.filter_by(id=id).first()
    if not hotel:    
        return jsonify({'message':'No hotel found. :('})
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({'message':"The hotel has been deleted"})

