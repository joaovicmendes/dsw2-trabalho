from flaskblog import db
from flaskblog.models import Site, Hotel, Promo
import os

os.system('rm flaskblog/promos.db')
db.create_all()

site1 = Site(nome    = "Site1",
            endereco = "www.site1.com",
            senha    = "senhasite1",
            telefone = "5516912345678")

site2 = Site(nome    = "Site2",
            endereco = "www.site2.com",
            senha    = "senhasite2",
            telefone = "5511955554444")

hotel = Hotel(nome = "Hotel",
            cnpj   = "00000111114444",
            senha  = "senhahotel",
            cidade = "São Paulo")

db.session.add(site1)

db.session.add(site2)

db.session.add(hotel)

promo1 = Promo(preco = 150.99, site_end=site1.endereco, hotel_cnpj=hotel.cnpj)
db.session.add(promo1)

promo2 = Promo(preco = 180.50, site_end=site2.endereco, hotel_cnpj=hotel.cnpj)
db.session.add(promo2)

promo3 = Promo(preco = 50.51, site_end=site1.endereco, hotel_cnpj=hotel.cnpj)
db.session.add(promo3)

db.session.commit()