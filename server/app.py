# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here

@app.route('/games')
def games():

    games = Game.query.all()
    games_data = [g.to_dict() for g in games]

    response = make_response(jsonify(games_data), 200)
    return response

@app.route('/games/<int:id>')
def game_by_id(id: int):
    game = Game.query.get(id)

    if not game:
        return make_response(jsonify({'error': f'The game does not currently exist.'}), 404)
    
    game_dict = game.to_dict()

    response = make_response(jsonify(game_dict), 200)
    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id: int):
    game = Game.query.get(id)

    users = [r.user.to_dict() for user in game.users]

    response = make_response(jsonify(users), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

