import requests
import logging

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

if __name__ == '__main__':
    location_list = ['itaewon seoul', 'hongdae seoul', 'ilsan', 'eujeongbu']
    meal_list = ['pizza', '']
    print(get_latitude_longitude_location('hongdae pizza'))