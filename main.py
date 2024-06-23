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
    last_action = db.Column(db.String(200), nullable=True)
    curtain_time = db.Column(db.String(200), nullable=True)
    watering_time = db.Column(db.String(200), nullable=True)
    temperature = db.Column(db.String(200), nullable=True)
    humidity = db.Column(db.String(200), nullable=True)  # Added humidity field

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
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
            current_user.last_action = request.path
            db.session.commit()
        except:
            return 'Неправильный токен', 403
        return f(current_user, *args, **kwargs)
    return wrap

@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/livingroom/curtains', endpoint='livingroom_curtains')
@token_required
def livingroom_curtains(current_user):
    print(f'{current_user.username} accessed livingroom_curtains')
    return redirect(url_for('index'))

@app.route('/livingroom/light', endpoint='livingroom_light')
@token_required
def livingroom_light(current_user):
    print(f'{current_user.username} accessed livingroom_light')
    return redirect(url_for('index'))

@app.route('/livingroom/radiator', endpoint='livingroom_radiator')
@token_required
def livingroom_radiator(current_user):
    print(f'{current_user.username} accessed livingroom_radiator')
    return redirect(url_for('index'))

@app.route('/greenhouse/watering', endpoint='greenhouse_watering')
@token_required
def greenhouse_watering(current_user):
    print(f'{current_user.username} accessed greenhouse_watering')
    return redirect(url_for('index'))

@app.route('/balcony/light', endpoint='balcony_light')
@token_required
def balcony_light(current_user):
    print(f'{current_user.username} accessed balcony_light')
    return redirect(url_for('index'))

@app.route('/bedroom/light', endpoint='bedroom_light')
@token_required
def bedroom_light(current_user):
    print(f'{current_user.username} accessed bedroom_light')
    return redirect(url_for('index'))

@app.route('/bedroom/lightmusic', endpoint='bedroom_lightmusic')
@token_required
def bedroom_lightmusic(current_user):
    print(f'{current_user.username} accessed bedroom_lightmusic')
    return redirect(url_for('index'))

@app.route('/room/light', endpoint='room_light')
@token_required
def room_light(current_user):
    print(f'{current_user.username} accessed room_light')
    return redirect(url_for('index'))

@app.route('/room/kettle', endpoint='room_kettle')
@token_required
def room_kettle(current_user):
    print(f'{current_user.username} accessed room_kettle')
    return redirect(url_for('index'))

@app.route('/api/user_settings', methods=['GET'])
def get_user_settings():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            'curtain_time': user.curtain_time,
            'watering_time': user.watering_time,
            'temperature': user.temperature,
            'humidity': user.humidity  # Added humidity field in response
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user_settings', methods=['POST'])
def set_user_settings():
    data = request.json
    token = data.get('jwt')
    curtain_time = data.get('curtain_time')
    watering_time = data.get('watering_time')
    temperature = data.get('temperature')
    humidity = data.get('humidity')  # Added humidity field in request

    if token:
        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(username=token_data['username']).first()
        except:
            return jsonify({'error': 'Invalid token'}), 403

        if user:
            if curtain_time:
                user.curtain_time = curtain_time
            if watering_time:
                user.watering_time = watering_time
            if temperature:
                user.temperature = temperature
            if humidity:
                user.humidity = humidity
            db.session.commit()
            return jsonify({'message': 'Settings updated successfully'})
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/user_last_action', methods=['POST'])
def user_last_action():
    data = request.json
    if 'jwt' in data:
        try:
            token_data = jwt.decode(data['jwt'], app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(username=token_data['username']).first()
        except:
            return jsonify({'error': 'Invalid token'}), 403
    elif 'mail' in data:
        user = User.query.filter_by(mail=data['mail']).first()
    elif 'username' in data:
        user = User.query.filter_by(username=data['username']).first()
    else:
        return jsonify({'error': 'No valid identifier provided'}), 400

    if user:
        return jsonify({'last_action': user.last_action})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
