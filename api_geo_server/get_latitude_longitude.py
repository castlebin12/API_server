import requests
import logging
import json

def get_latitude_longitude_location(location):
    API_key = ''
    address = location
    address = address.replace(' ', '+')
    geocode_parameter = {'address' : address, 'key' : API_key}
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params= geocode_parameter)

    if response.status_code == 200:
        print('URL : ', response.url)
        latitude = response.json()['results'][0]['geometry']['location']['lat']
        longitude = response.json()['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        logging.error('Cant get correct API')
        raise ValueError

def get_restaurants(latitude, longitude, meal_list):
    url = 'https://api.foursquare.com/v2/venues/explore'
    client_id = ''
    client_secret = ''
    restaurants_list = []

    for _ in meal_list:
    
        params = dict(
            client_id=client_id,
            client_secret=client_secret,
            v='20180323',
            ll= f'{latitude},{longitude}',
            query='pizza',
            limit=2
        )
        resp = requests.get(url=url, params=params)
        restaurants.append() = resp.json()
    return restaurants

if __name__ == '__main__':
    location_list = ['itaewon seoul', 'hongdae seoul', 'ilsan', 'eujeongbu']
    meal_list = ['pizza', 'hamburger']
    latitude, longitude = get_latitude_longitude_location('seoul')
    restaurants = get_restaurants(latitude, longitude)
    print(json.dumps(restaurants, indent=2))