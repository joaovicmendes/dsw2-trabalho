from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)


_ = '''
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username() or not auth.password():
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id':})
'''