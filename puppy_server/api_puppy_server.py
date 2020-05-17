from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy
import logging

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/puppies', methods = ['POST', 'GET'])
def puppies_function():
    if request.method == 'GET':
        return get_all_puppies()

    elif request.method =='POST':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        logging.info(f'Making a New Puppy name : {name}, description : {description}')

        return make_a_new_puppy(name, description)


@app.route('/puppies/<int:id>', methods = ['PUT', 'GET', "DELETE"])
def puppies_id_function(id):
    if request.method == 'GET':
        return get_puppy(id)
    
    elif request.method == 'PUT':
        name = request.args.get('name', '')
        description = request.args.get('description', '')

        return update_puppy(id, name, description)
    
    elif request.method == 'DELETE':

        return delete_puppy(id)

def get_all_puppies():
    puppies = session.query(Puppy).all()

    return jsonify(Puppies = [puppy.serialize for puppy in puppies])

def get_puppy(id):
    puppy = session.query(Puppy).filter_by(id = id).one()

    return jsonify(puppy = puppy.serialize)

def make_a_new_puppy(name, description):
    puppy = Puppy(name = name, description = description)
    session.add(puppy)
    session.commit()

    return jsonify(Puppy=puppy.serialize)

def update_puppy(id, name, description):
    puppy = session.query(Puppy).filter_by(id = id).one()
    if not name:
        puppy.name = name
    if not description:
        puppy.description = description
    
    session.add(puppy)
    session.commit()
    
    return f'Updated a puppy with id : {id}'

def delete_puppy(id):
    puppy = session.query(Puppy).filter_by(id = id).one()
    session.delete(puppy)
    session.commit()

    return f'Removed puppy with id : {id}'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	
