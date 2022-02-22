import requests


if __name__ == '__main__':
    url = 'http://localhost:5000/predict'

    dict_to_send = {'input_data': "1,25,0,22,1\n2,25,0,22,2\n3,25,0,22,3\n4,25,0,22,4\n5,25,0,22,5\n6,25,0,22,6\n7,25,0,22,7"}
    response = requests.post(url, dict_to_send)
    try:
        data = response.json()
        print(data)
    except requests.exceptions.RequestException:
        print(response.text)
