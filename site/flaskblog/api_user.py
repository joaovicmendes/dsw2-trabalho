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
