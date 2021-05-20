from flask import render_template, url_for, flash, request, jsonify, make_response
from flask import session,redirect,render_template_string #Usado no login (o render_template_string é só usado na resposta)
import json, requests
from flaskblog import app

BASE_URL = "http://localhost:5000/"

@app.route("/")
@app.route("/home")
def home():
    req = requests.get(BASE_URL + 'api/site')
    data = json.loads(req.content)
    #aqui tem que usar o json pra montar as tabelas e tal
    #coisa pra krl pra fazer ainda em fml pprt
    return render_template('home.html', data=data)



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