from flaskblog import db
from datetime import datetime

class Site(db.Model):
    id        = db.Column(db.Integer, primary_key = True)
    nome      = db.Column(db.String(30), nullable = False, unique = True)
    endereco  = db.Column(db.String(50), nullable = False, unique = True)
    senha     = db.Column(db.String(20), nullable = False)
    telefone  = db.Column(db.String(13), nullable = False, unique = True)
    promos    = db.relationship('Promo', backref='site')

    def __repr__(self):
        return f"{self.nome} - {self.endereco}"

class Hotel(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    nome    = db.Column(db.String(30), nullable = False, unique = True)
    cnpj    = db.Column(db.String(14), nullable = False, unique = True)
    senha   = db.Column(db.String(20), nullable = False)
    cidade  = db.Column(db.String(30), nullable = False)
    promos  = db.relationship('Promo', backref='hotel')

    def __repr__(self):
        return f"{self.nome} - {self.cnpj}"

class Promo(db.Model):
    id         = db.Column(db.Integer, primary_key = True)
    site_end   = db.Column(db.String(50), db.ForeignKey('site.endereco'))
    hotel_cnpj = db.Column(db.String(50), db.ForeignKey('hotel.cnpj'))
    preco      = db.Column(db.Float, nullable = False)
    ini_promo  = db.Column(db.DateTime, default = datetime.now())
    end_promo  = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self):
        return f"{self.site_end}, {self.hotel_cnpj}: {self.preco}"
