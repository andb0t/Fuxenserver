import requests


def read_messages():
    response = requests.get('http://localhost:5000/messages')
    print('TODO: implement check for json data')
    print(response.text)
    print('response.json()    :', response.json())
    print('response.json()[0] :', response.json()[0])


def post_message(username, message):
    response = requests.post('http://localhost:5000/messages',
                             json={'message': message,
                                   'username': username
                                   }
                             )
    # if request fails or throws error
    response.raise_for_status()


read_messages()
post_message('andb0t', 'Hi, posting message!')
read_messages()
