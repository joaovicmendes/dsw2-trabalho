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
    #print("---------------------------------\n\n\n")
    #print(req.content)
    #print("---------------------------------\n\n\n")
    data = json.loads(req.content)
    #aqui tem que usar o json pra montar as tabelas e tal
    #coisa pra krl pra fazer ainda em fml pprt
    
    #cria as informações para gerar a tabela
    table_headers = [] #as chaves no header da tabela
    table_data = [] #as informaçes para mostrar na tabela
    for d in data['promos']:
        _ = d.pop('id')
    if data["promos"]:
        table_headers = data["promos"][0].keys()
        table_data = []
    for promo in data["promos"]:
        table_data.append(promo.values())
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', data=context,table_headers=table_headers,table_data=table_data,table_name='Promoções')

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
    for d in data['sites']:
        _ = d.pop('senha')
        _ = d.pop('id')
    #cria as informações para gerar a tabela
    table_headers = list() #as chaves no header da tabela
    table_data = list() #as informaçes para mostrar na tabela
    if data["sites"]:
        table_headers = list(data["sites"][0].keys())
    for promo in data["sites"]:
        table_data.append(promo.values())
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', title= "Otelo - Sites", data=context ,table_headers=table_headers, table_data=table_data, table_name='Sites')

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
    for d in data['hoteis']:
        _ = d.pop('senha')
        _ = d.pop('id')
    #cria as informações para gerar a tabela
    table_headers = list() #as chaves no header da tabela
    table_data = list() #as informaçes para mostrar na tabela
    if data["hoteis"]:
        table_headers = list(data["hoteis"][0].keys())
    for promo in data["hoteis"]:
        table_data.append(promo.values())
    
    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', title="Otelo - Hoteis", data=context ,table_headers=table_headers, table_data=table_data, table_name='Hoteis')


# Realiza logout por limpar a sessão
@app.route('/logout')
def logout():
    session.pop('username', default=None)
    session.pop('auth', default=False)
    session.pop('temp_token', default=None)
    # return jsonify({'message':'Logout realizado'}), 200
    return '''
            Deslogado com sucesso
            <script>window.localStorage.removeItem('token');</script>
            <a href="/">Inicio</a>
        '''

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
                # @TODO: Precisa começar a salvar a senha hasheada no banco para fazer essa verificação
                if check_password_hash(user.senha, senha): 
                #if user.senha == senha:
                    session['username'] = username
                    session['logado']   = True
                    session['temp_token'] = generate_token(user)
                    session['role'] = get_user_role(user)
                    return 'Login bem sucedido, usuário ' + username

        # @TODO colocar mensagem de erro no template
        context = get_session_context(session)
        return render_template('login.html', title="Otelo - Login", data=context)
        
    context = get_session_context(session)
    return render_template('login.html', title="Otelo - Login", data=context)


@app.route('/api/token', methods=['POST'])
def get_token():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'Credenciais inválidas',
            401,
            {'WWW-Authenticate' : 'Basic realm="Precisa estar logado"'})

    user = get_user_via_username(auth.username)
    if not user:
        return jsonify({'message':'Credenciais invalidas.'}), 404

    # Geração de token para validar requisições para a API
    # @TODO: Precisa começar a salvar a senha hasheada no banco para fazer essa verificação
    if check_password_hash(user.senha, auth.password): 
    #if user.senha == auth.password:
        token = generate_token(user)
        return jsonify({'token': token}), 200

    return jsonify({'message':'Credenciais invalidas.'}), 404
