import requests

url='http://localhost:5000/write'

data = {
    'name': 'ryota',
    'email': 'al21011@shiabura-it.ac.jp'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Data written Successfully:", response.json())
else:
    print('Failed to write data:', response.status_code)
    