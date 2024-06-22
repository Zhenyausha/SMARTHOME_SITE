import requests

# URL вашего приложения
base_url = 'http://localhost:5000'

# Информация для идентификации пользователя
jwt_token = 'YOUR_JWT_TOKEN'
mail = 'zhena777'
username='www'
# Заголовки для запроса
headers = {
    'Content-Type': 'application/json',
    'x-access-token': jwt_token  # добавьте это, если вы используете JWT для аутентификации
}

# Данные для идентификации пользователя
data = {
    # 'jwt': jwt_token,  # Используйте это, если хотите аутентифицироваться через JWT
    #'mail': mail,
    'username': username  # Используйте это, если хотите аутентифицироваться через username
}

# Отправка POST запроса
response = requests.post(f'{base_url}/api/user_last_action', json=data, headers=headers)

# Проверка ответа
if response.status_code == 200:
    print('Последнее действие пользователя:', response.json()['last_action'])
else:
    print('Ошибка:', response.json())
