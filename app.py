from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@pg-srv/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

# Création des tables de la base de données
@app.before_first_request
def create_tables():
    db.create_all()

# Route pour ajouter un utilisateur
@app.route('/add_user/', methods=['POST'])
def add_user():
    name = request.json['name']
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Route pour lister tous les utilisateurs
@app.route('/users/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)