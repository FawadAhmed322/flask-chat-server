from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from utils.utils import load_environment_variables
from models.user import User
from functools import wraps

app = Flask(__name__)

env_variables = load_environment_variables()

try:
    app.secret_key = env_variables['SECRET_KEY']
except:
    app.secret_key = '42'
    print(f'Warning, using default secret key: {app.secret_key}')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            current_user = User.get_by_email(data['email'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def hello_world():
    res = make_response('Hello World!')
    return res

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            return jsonify({'error': 'Passwords do not match'})

        user = User.get_by_email(email)
        if user:
            return jsonify({'error': 'User with that email already exists'})

        # create hash of password
        password_hash = generate_password_hash(password1, method='sha256')
    
        user = User(username=username, email=email, password_hash=password_hash)
        return jsonify({'success': 'User registered: ' + user.user['email']})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # create hash of password
        user = User.get_by_email(email)

        if not user:
            return jsonify({'error': 'User with that email does not exist'})
        else:
            if check_password_hash(user['password_hash'], password):
                token = jwt.encode({'email': user['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.secret_key)
                return jsonify({'success': 'User logged in: ' + user['email'], 'token': token})

@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    return jsonify({'users': User.users})

@app.route('/hello')
@token_required
def hello(current_user):
    return jsonify({'message': f'Hello {current_user["username"]}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)