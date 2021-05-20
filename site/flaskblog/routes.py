from flask import render_template, url_for, flash, request, jsonify, make_response
from flask import session,redirect,render_template_string #Usado no login (o render_template_string é só usado na resposta)
from flaskblog import app, db
from flaskblog.models import Site, Hotel, Promo 
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


#tentando realizar o login
app.secret_key = 'BAD_SECRET_KEY'

#@TODO Formulário de cadastro
## Já que tem o endpoint de POST de site, não mexi nisso pra n quebrar nada
@app.route('/cadastro', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """

#Verifica se está logado como algum usuário, caso não esteja pede que seja realizado o login
@app.route('/is_logged')
def is_logged():
    return render_template_string("""
            {% if session['token'] %}
                <h1>Welcome, you are logged as {{ session['user_type'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
            {% endif %}
        """)

#realiza logout por limpar a sessão
@app.route('/logout')
def logout():
    # Clear the email stored in the session object
    session.pop('token', default=False)
    session.pop('user_type', default=None)
    return '<h1>Logout realizado!</h1>'

#Rota de Login
#Caso receba um post, efetua comparação com a database e realiza o login se possível
#Caso receba um get, retorna o template de formulário para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        site = Site.query.filter_by(nome=request.form["login_name"]).first()
        if not site:    
            return jsonify({'message':'No site found. :('})
            pass

        session['token'] = True
        session['user_type'] = "site"

        return redirect(url_for('is_logged'))


    return """
        <form method="post">
            <label for="email">Nome:</label>
            <input  id="name" name="login_name" required />
            <br>
            <label for="email">Senha:</label>
            <input  id="password" name="login_password" required />
            <br>
            <button type="submit">Submit</button>
            

        </form>
        """