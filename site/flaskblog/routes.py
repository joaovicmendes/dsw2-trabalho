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
    req = requests.get(BASE_URL + 'api/site')
    data = json.loads(req.content)
    #aqui tem que usar o json pra montar as tabelas e tal
    #coisa pra krl pra fazer ainda em fml pprt
    return render_template('home.html', data=data)

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

# realiza logout por limpar a sessão
@app.route('/logout')
def logout():
    session.pop('token', default=False)
    session.pop('user_type', default=None)
    return jsonify({'message':'Logout realizado'}), 200

## Rotas de Login
#  GET:  retorna o template de formulário para login
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

#  POST: tentativa de login
@app.route('/login', methods=['POST'])
def login_post():
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
        session['token'] = token # para simular chamada rest via js
        return jsonify({'token': token}), 200

    return jsonify({'message':'Credenciais invalidas.'}), 404
