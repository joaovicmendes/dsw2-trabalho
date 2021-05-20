from flaskblog import db
from flaskblog.models import Site, Hotel, Promo
import os

os.system('rm flaskblog/banco.db')
db.create_all()

site1 = Site(nome    = "Ofertão",
            endereco = "www.ofertao.com.br",
            senha    = "senhasite1",
            telefone = "5516912345678")

site2 = Site(nome    = "Desconto Legal",
            endereco = "www.descontolegal.com",
            senha    = "senhasite2",
            telefone = "5511961382167")

site3 = Site(nome    = "Central do Preço",
            endereco = "www.centraldopreco.com",
            senha    = "senhasite2",
            telefone = "5511964052079")

site4 = Site(nome    = "Preço Baixo",
            endereco = "www.precobaixo.com.br",
            senha    = "senhasite3",
            telefone = "5519933427065")

site5 = Site(nome    = "Cupom Store",
            endereco = "www.cupomstore.com",
            senha    = "senhasite4",
            telefone = "5517954076430")


hotel1 = Hotel(nome = "Lakeview Hotel",
            cnpj    = "62278848997305",
            senha   = "senhahotel1",
            cidade  = "São Paulo")

hotel2 = Hotel(nome = "Oceanview Motel",
            cnpj    = "74154433501666",
            senha   = "senhahotel2",
            cidade  = "São Paulo")

hotel3 = Hotel(nome = "The Great Northern Hotel",
            cnpj    = "33373145729006",
            senha   = "senhahotel3",
            cidade  = "São Paulo")

hotel4 = Hotel(nome = "Giant's Deep Hotel",
            cnpj    = "33146749007486",
            senha   = "senhahotel4",
            cidade  = "Blumenau")

hotel5 = Hotel(nome = "Brittle Hollow Hotel",
            cnpj    = "48057327771821",
            senha   = "senhahotel4",
            cidade  = "Blumenau")

hotel6 = Hotel(nome = "Timber Hearth Hotel",
            cnpj    = "94743633222202",
            senha   = "senhahotel5",
            cidade  = "Salvador")

            
db.session.add(site1)
db.session.add(site2)
db.session.add(site3)
db.session.add(site4)
db.session.add(site5)
db.session.add(hotel1)
db.session.add(hotel2)
db.session.add(hotel3)
db.session.add(hotel4)
db.session.add(hotel5)
db.session.add(hotel6)


promo1  = Promo(preco = 100.19, site_end=site1.endereco, hotel_cnpj=hotel1.cnpj)
promo2  = Promo(preco = 110.29, site_end=site2.endereco, hotel_cnpj=hotel1.cnpj)
promo3  = Promo(preco = 200.39, site_end=site3.endereco, hotel_cnpj=hotel2.cnpj)
promo4  = Promo(preco = 220.49, site_end=site4.endereco, hotel_cnpj=hotel2.cnpj)
promo5  = Promo(preco = 300.59, site_end=site5.endereco, hotel_cnpj=hotel3.cnpj)
promo6  = Promo(preco = 330.69, site_end=site1.endereco, hotel_cnpj=hotel3.cnpj)
promo7  = Promo(preco = 400.79, site_end=site2.endereco, hotel_cnpj=hotel4.cnpj)
promo8  = Promo(preco = 440.89, site_end=site3.endereco, hotel_cnpj=hotel4.cnpj)
promo9  = Promo(preco = 550.99, site_end=site4.endereco, hotel_cnpj=hotel5.cnpj)
promo10 = Promo(preco = 550.09, site_end=site5.endereco, hotel_cnpj=hotel5.cnpj)


db.session.add(promo1)
db.session.add(promo2)
db.session.add(promo3)
db.session.add(promo4)
db.session.add(promo5)
db.session.add(promo6)
db.session.add(promo7)
db.session.add(promo8)
db.session.add(promo9)
db.session.add(promo10)

db.session.commit()