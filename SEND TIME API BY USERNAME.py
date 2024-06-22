import requests
import jwt

def send_temperature(username, temperature, secret_key):
    url = 'http://localhost:5000/api/user_settings'
    
    # Generate JWT token
    token = jwt.encode({'username': username}, secret_key, algorithm='HS256')
    
    data = {
        'jwt': token,
        'temperature': temperature
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print("Temperature updated successfully")
    else:
        print(f"Error: {response.status_code}, {response.json().get('error')}")

if __name__ == "__main__":
    username = input("Enter the username: ")
    temperature = input("Enter the current temperature: ")
    secret_key = 'your_secret_key'  # Replace with your actual secret key
    send_temperature(username, temperature, secret_key)
