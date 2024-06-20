from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
            #return jsonify({'token': token})
            return redirect(url_for('index'))
        return 'Неправильное имя пользователя или пароль', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password, mail=data['mail'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return 'Токен отсутствует', 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return 'Неправильный токен', 403
        return f(current_user, *args, **kwargs)
    return wrap

@app.route('/livingroom/curtains', endpoint='livingroom_curtains')
@token_required
def livingroom_curtains(current_user):
    return redirect(url_for('index'))

@app.route('/livingroom/light', endpoint='livingroom_light')
@token_required
def livingroom_light(current_user):
    return redirect(url_for('index'))

@app.route('/livingroom/radiator', endpoint='livingroom_radiator')
@token_required
def livingroom_radiator(current_user):
    return redirect(url_for('index'))

@app.route('/greenhouse/watering', endpoint='greenhouse_watering')
@token_required
def greenhouse_watering(current_user):
    return redirect(url_for('index'))

@app.route('/balcony/light', endpoint='balcony_light')
@token_required
def balcony_light(current_user):
    return redirect(url_for('index'))

@app.route('/bedroom/light', endpoint='bedroom_light')
@token_required
def bedroom_light(current_user):
    return redirect(url_for('index'))

@app.route('/bedroom/lightmusic', endpoint='bedroom_lightmusic')
@token_required
def bedroom_lightmusic(current_user):
    return redirect(url_for('index'))

@app.route('/room/light', endpoint='room_light')
@token_required
def room_light(current_user):
    return redirect(url_for('index'))

@app.route('/room/kettle', endpoint='room_kettle')
@token_required
def room_kettle(current_user):
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
