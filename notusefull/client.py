import requests
import json

def send_data_to_server(data):
    server_url = "http://127.0.0.1"
    
    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data successfully sent to the server.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to the server: {e}")

def get_user_input():
    name = input("Enter the person's name: ")
    age = input("Enter the person's age: ")
    email = input("Enter the person's email: ")
    
    user_data = {
        "name": name,
        "age": age,
        "email": email,
    }
    
    return user_data

def main():
    user_data = get_user_input()
    send_data_to_server(user_data)

if __name__ == "__main__":
    main()
