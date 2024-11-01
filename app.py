from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from urllib.parse import quote as url_quote  # Updated import
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Set up the SQLAlchemy database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'hitc_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'age': self.age}

with app.app_context():
    db.create_all()

@app.route('/hello', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'hey there! welcome to the headintheclouds community! :)'}), 200)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(username=data['username'], email=data['email'], age=data['age'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'User successfully created!'}), 201)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'message': 'User with this username or email already exists.'}), 400)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while creating the user.'}), 500)

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'message': 'All users fetched successfully', 'users': [user.json() for user in users]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while fetching users.'}), 500)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'message': 'User found!', 'user': user.json()}), 200)
        return make_response(jsonify({'message': 'User not found.'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while fetching the user.'}), 500)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.username = data['username']
            user.email = data['email']
            user.age = data['age']
            db.session.commit()
            return make_response(jsonify({'message': 'User details successfully updated!'}), 200)
        return make_response(jsonify({'message': 'User not found.'}), 404)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'message': 'User with this username or email already exists.'}), 400)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while updating user details.'}), 500)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'User successfully deleted!'}), 200)
        return make_response(jsonify({'message': 'User not found.'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while deleting the user.'}), 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
