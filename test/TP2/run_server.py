# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import hashlib  

HTTPS_MODE = True

# définir le message secret
SECRET_MESSAGE = "aziz" # A modifier
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def get_secret_message():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        
        user = User.query.filter_by(username=userName).first()
        
        if user and user.check_password(password):
            return render_template('accueil.html', userName=userName, message=SECRET_MESSAGE)
        else:
            error = 'Erreur. Connexion échouée. Veuillez réessayer.'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

    


if __name__ == "__main__":
    # HTTP version
    # app.run(debug=True, host="0.0.0.0", port=8081)
    # HTTPS version
    # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire

    if HTTPS_MODE == False:
        # HTTP version
        app.run(debug=True, host="0.0.0.0", port=8081)
    else :
        # Crée la base de données et les tables si elles n'existent pas déjà

        with app.app_context():
            db.create_all()
        # HTTPS version
        # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire
        context = ("resources/server-public-key.pem", "resources/server-private-key.pem")
        app.run(debug=True, host="127.0.0.1", port=8081, ssl_context=context)
   
