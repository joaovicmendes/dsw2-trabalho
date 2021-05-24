import json, requests
from flask import render_template, url_for, flash, request, jsonify, make_response
from flask import session, redirect, render_template_string
from flaskblog import app
from .models import *
from .utils import *

BASE_URL = "http://localhost:5000/"

@app.route("/")
@app.route("/home")
def home():
    req = requests.get(BASE_URL + 'api/promocao')
    #print("---------------------------------\n\n\n")
    #print(req.content)
    #print("---------------------------------\n\n\n")
    data = json.loads(req.content)
    #aqui tem que usar o json pra montar as tabelas e tal
    #coisa pra krl pra fazer ainda em fml pprt
    
    #cria as informações para gerar a tabela
    table_headers = data["promos"][0].keys()#as chaves no header da tabela
    table_data = []#as informaçes para mostrar na tabela
    for promo in data["promos"]:
        table_data.append(promo.values())
    
    #aqui coloquei pra poder comparar os tokens da sessão
    context = {}
    if session:
        try:
            context['username'] = session['username']
            context['logado'] = session['logado']
            context['token'] = session['temp_token']
        except KeyError:
            pass

    #caso não precise de tabela, só tirar o table_header e table_data que nem renderiza a tabela
    return render_template('home.html', data=context ,table_headers=table_headers,table_data=table_data)

## Rotas de Cadastro
# Rota inicial, que redireciona para o arquivo específico desejado
@app.route('/cadastrar', methods=['GET'])
def signup():
    return render_template('cadastro.html')

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

    return render_template('cadastro_site.html')

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

    return render_template('cadastro_hotel.html')


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
                # if check_password_hash(user.senha, auth.password): 
                if user.senha == senha:
                    session['username'] = username
                    session['logado']   = True
                    session['temp_token'] = generate_token(user)
                    return 'Login bem sucedido, usuário ' + username

        # @TODO colocar mensagem de erro no template
        return render_template('login.html')

    return render_template('login.html')


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
    # if check_password_hash(user.senha, auth.password): 
    if user.senha == auth.password:
        token = generate_token(user)
        return jsonify({'token': token}), 200

    return jsonify({'message':'Credenciais invalidas.'}), 404
