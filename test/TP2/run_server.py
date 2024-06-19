# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

import hashlib  

HTTPS_MODE = True

# définir le message secret
SECRET_MESSAGE = "aziz" # A modifier
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Route pour la création d'un utilisateur via une page secrète
@app.route('/admin', methods=['GET', 'POST'])
def admin_create_user():
    # Autorisation simplifiée pour accéder à la page secrète (à améliorer pour un usage réel)
    authorized = True

    if authorized:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Vérifiez si l'utilisateur existe déjà
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('L\'utilisateur existe déjà.', 'error')
                return redirect(url_for('admin_create_user'))  # Redirigez vers la page de création d'utilisateur

            # Créez un nouvel utilisateur
            new_user = User(username=username)
            new_user.set_password(password)  # Vous devrez implémenter cette méthode
            db.session.add(new_user)
            db.session.commit()

            flash('Utilisateur créé avec succès.', 'success')
            return redirect(url_for('get_secret_message'))  # Redirigez vers la page d'accueil ou une autre page

        return render_template('admin.html')

    else:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('get_secret_message'))  # Redirigez vers la page de connexion

# Définition de la classe User pour la table de la base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

# Route principale de l'application
@app.route('/', methods=['GET', 'POST'])
def get_secret_message():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        
        # Recherche de l'utilisateur dans la base de données
        user = User.query.filter_by(username=userName).first()
        
        if user and user.check_password(password):
            # Affichage de la page d'accueil avec le message secret
            return render_template('accueil.html', userName=userName, message=SECRET_MESSAGE)
        else:
            # Affichage de la page de connexion avec un message d'erreur
            error = 'Erreur. Connexion échouée. Veuillez réessayer.'
            return render_template('index.html', error=error)
    else:
        # Affichage de la page de connexion
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
   
