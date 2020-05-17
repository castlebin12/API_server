import requests
import logging
import json

logging.info('Running Endpoint Tester')
address = 'http://localhost:5000/restaurants'

try:
    print('test 1 : Creating New restaurant...')
    location = 'itaewon seoul'
    food = 'pizza'
    param = {
        'location' : location,
        'food' : food
    }
    # response = requests.get(address)
    response = requests.post(address, data=param)
    print(response.status_code)
    print(response.text)

except Exception as e:
    print(e)