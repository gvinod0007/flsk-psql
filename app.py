from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Set the SQLALCHEMY_DATABASE_URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')  # Ensure this matches your deployment variable

# Initialize SQLAlchemy
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

# Head in the clouds test route
@app.route('/hello', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'hey there! welcome to the headintheclouds community! :)'}), 200)

# Create a user
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

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'message': 'All users fetched successfully', 'users': [user.json() for user in users]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while fetching users.'}), 500)

# Get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'message': 'User found!', 'user': user.json()}), 200)
        return make_response(jsonify({'message': 'User not found.'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Oops! Something went wrong while fetching the user.'}), 500)

# Update a user by id
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

# Delete a user
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
    app.run(host='0.0.0.0', port=5000)  # Change port to 5000 to match your deployment YAML
