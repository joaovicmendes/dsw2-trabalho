import json, requests
from flask import render_template, url_for, flash, request, jsonify, make_response
from flask import session, redirect, render_template_string
from werkzeug.security import  check_password_hash
from flaskblog import app
from .models import *
from .utils import *

BASE_URL = "http://localhost:5000/"

@app.route("/")
@app.route("/home")
def home():
    context = get_session_context(session)
    
    if "role" in context:
        if context["role"] == 'hotel':
            req = requests.get(BASE_URL + 'api/promocao/hotel/' + context["username"])
        if context["role"] == "site":
            req = requests.get(BASE_URL + 'api/promocao/site/' + context["username"])
    else:
        req = requests.get(BASE_URL + 'api/promocao')

    data = json.loads(req.content)

    #cria as informações para gerar a tabela
    headers, rows = filter_table(data['promos'],'promo', ['id'])
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', data=context, headers=headers, table_data=rows, name='Promoções', script="promocoes")

## Rotas de Cadastro
# Rota inicial, que redireciona para o arquivo específico desejado
@app.route('/cadastrar', methods=['GET'])
def signup():
    context = get_session_context(session)
    return render_template('cadastro.html', title="Otelo - Cadastro",  data=context)

@app.route('/cadastrar/site', methods=['GET', 'POST'])
def signup_site():
    # Não deve ser necessário quando tiver JS no front
    if request.method == 'POST':
        site = {}
        site['nome']     = request.form['nome']
        site['endereco'] = request.form['endereco']
        site['senha']    = request.form['senha']
        site['telefone'] = request.form['telefone']
 
        req = requests.post(BASE_URL + 'api/site', json=site)
        if req.status_code != 201:
            return jsonify({'message': 'Não foi possível criar Site'}), 500

        return jsonify({'message': 'Site criado com sucesso'}), 201

    context = get_session_context(session)
    return render_template('cadastro_site.html', title="Otelo - Cadastro de site",  data=context)

@app.route('/cadastrar/hotel', methods=['GET', 'POST'])
def signup_hotel():
    # Não deve ser necessário quando tiver JS no front
    if request.method == 'POST':
        site = {}
        site['nome']   = request.form['nome']
        site['cnpj']   = request.form['cnpj']
        site['senha']  = request.form['senha']
        site['cidade'] = request.form['cidade']
 
        req = requests.post(BASE_URL + 'api/hotel', json=site)
        if req.status_code != 201:
            return jsonify({'message': 'Não foi possível criar Hotel'}), 500

        return jsonify({'message': 'Hotel criado com sucesso'}), 201

    context = get_session_context(session)
    return render_template('cadastro_hotel.html', title="Cadastro de Hotel",  data=context)

@app.route('/cadastrar/promocao', methods=['GET'])
def create_promos():
    raw_sites  = Site.query.all()
    sites = []
    for site in raw_sites:
        sites.append(site)

    raw_hoteis = Hotel.query.all()
    hoteis = []
    for hotel in raw_hoteis:
        hoteis.append(hotel)

    context = get_session_context(session)
    return render_template('cadastro_promocao.html', title="Otelo - Cadastro",  data=context, hoteis=hoteis, sites=sites)

## Rotas de Listagem
#Rota de listar sites
@app.route('/sites')
def list_sites():
    context = get_session_context(session)
    if "role" in context:
        if context["role"] == 'hotel':
            req = requests.get(BASE_URL + 'api/promocao/hotel/' + context["username"])
        if context["role"] == "site":
            req = requests.get(BASE_URL + 'api/promocao/site/' + context["username"])
    
    req = requests.get(BASE_URL + 'api/site')
    data = json.loads(req.content)
    headers, rows = filter_table(data['sites'],'site',['senha','id'])
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', title="Otelo - Sites", data=context ,headers=headers, table_data=rows, name='Sites', script="sites")

@app.route('/hoteis')
def list_hotels():
    context = get_session_context(session)
    if "role" in context:
        if context["role"] == 'hotel':
            req = requests.get(BASE_URL + 'api/promocao/hotel/' + context["username"])
        if context["role"] == "site":
            req = requests.get(BASE_URL + 'api/promocao/site/' + context["username"])
    
    req = requests.get(BASE_URL + 'api/hotel')
    data = json.loads(req.content)
    headers, rows = filter_table(data['hoteis'],'hotel',['senha','id'])
   
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', title="Otelo - Hoteis", data=context ,headers=headers, table_data=rows, name='Hoteis', script="hoteis")


# Realiza logout por limpar a sessão
@app.route('/logout')
def logout():
    session.pop('username', default=None)
    session.pop('auth', default=False)
    session.pop('temp_token', default=None)
    context = get_session_context(session)
    return render_template('logout.html', title="Otelo - Login", data=context)

## Rotas de Login
#  GET:  retorna o template de formulário para login
#  POST: tentativa de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha    = request.form['password']
        if username and senha:
            user = get_user_via_username(username)
            if user:
                if check_password_hash(user.senha, senha): 
                    session['username'] = username
                    session['logado']   = True
                    session['temp_token'] = generate_token(user)
                    session['role'] = get_user_role(user)
                    return render_template('login_sucesso.html', title="Otelo - Login", data=get_session_context(session))

        context = get_session_context(session)
        return render_template('login.html', title="Otelo - Login", data=context)
        
    context = get_session_context(session)
    return render_template('login.html', title="Otelo - Login", data=context)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    context = get_session_context(session)
    return render_template('404.html', data=context), 404

@app.errorhandler(405)
def method_not_allowed(e):
    # note that we set the 404 status explicitly
    context = get_session_context(session)
    return render_template('404.html', data=context), 405

@app.errorhandler(403)
def invalid_credentials(e):
    # note that we set the 404 status explicitly
    context = get_session_context(session)
    return render_template('403.html', data=context), 404