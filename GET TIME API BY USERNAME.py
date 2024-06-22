import requests

def get_user_settings(username):
    url = f'http://localhost:5000/api/user_settings?username={username}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            curtain_time = data.get('curtain_time', 'Not set')
            watering_time = data.get('watering_time', 'Not set')
            print(f"Curtain Closing Time: {curtain_time}")
            print(f"Greenhouse Watering Time: {watering_time}")
    else:
        print(f"Error: {response.status_code}, {response.json().get('error')}")

if __name__ == "__main__":
    username = input("Enter the username: ")
    get_user_settings(username)
