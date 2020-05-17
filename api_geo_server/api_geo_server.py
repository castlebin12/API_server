import requests
import logging
import json
from datetime import date
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

foursquare_client_id = ''
foursquare_client_secret = ''
google_api_key = ''

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        # RETURN ALL RESTAURANTS IN DATABASE
        restaurants = session.query(Restaurant).all()
        
        return jsonify(restaurants = [i.serialize for i in restaurants])

    elif request.method == 'POST':
        # MAKE A NEW RESTAURANT AND STORE IT IN DATABASE
        location = request.form.get('location')
        food = request.form.get('food')
        latitude, longitude = get_latitude_longitude_location(location)
        restaurant_info = get_restaurants(latitude, longitude, food)
        
        if restaurant_info != 'No Restaurants Found':
            restaurant = Restaurant(restaurant_id = restaurant_info['restaurant_id'], name = restaurant_info['name'], \
                                    location = restaurant_info['location'], food = restaurant_info['food'])
            session.add(restaurant)
            session.commit() 
            return jsonify(restaurant = restaurant.serialize)
        else:
            return jsonify({'error' : f'No Restaurants Found for {food} in {location}' })


def get_latitude_longitude_location(location):
    API_key = google_api_key
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
        response.raise_for_status()


def get_restaurants(latitude, longitude, meal):
    url = 'https://api.foursquare.com/v2/venues/explore'
    client_id = foursquare_client_id
    client_secret = foursquare_client_secret
    
    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v=str(date.today()).replace('-', ''), # Version
        ll= f'{latitude},{longitude}',
        query=meal,
        intent = 'browse',
        radius = 1_000,
        limit=1
    )
    resp = requests.get(url=url, params=params)
    venue = resp.json()['response']['groups'][0]['items'][0]['venue']

    if venue:
        restaurant_id = venue['id']
        name = venue['name']
        location = venue['location']['address']
        restaurant_info = {'food' : meal, 'restaurant_id' : restaurant_id, 'name' : name, 'location' : location}

        return restaurant_info
    
    else:
        return 'No Restaurants Found'

    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

    # meal = 'burger'
    # location = 'itaewon'

    # latitude, longitude = get_latitude_longitude_location(location)
    # restaurant_info = get_restaurants(latitude, longitude, meal)
    
    # print(restaurant_info)