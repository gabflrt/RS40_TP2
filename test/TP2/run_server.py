# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask
from flask import request
from flask import render_template
import hashlib  

HTTPS_MODE = True

# définir le message secret
SECRET_MESSAGE = "J'explique !" # A modifier
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def get_secret_message():
    if request.method == 'POST':
        # Reception des donnees du formulaire
        userName = request.form['userName']
        password = request.form['password']
        #hash du mot de passe en entré pour obtenir le même résultat
        inputPassword = hashlib.sha256(password.encode()).hexdigest()
        # Verification du login. 
        # Si correct -> redirection vers page.html
        # Sinon redirection vers la page login.html avec message d'erreur
        if userName == "user" and inputPassword == mdpHasher:
            return render_template('accueil.html', userName=userName, message=
    SECRET_MESSAGE)
        else:
            error = 'Oups! Votre login ou mot de passe est incorrect. Veuillez réessayer.'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

#definition du mot de passe
userPassword = "mdp"
#hash du mot de passe avec SHA256 pour plus de sécurité
mdpHasher = hashlib.sha256(userPassword.encode()).hexdigest()


if __name__ == "__main__":
    # HTTP version
    # app.run(debug=True, host="0.0.0.0", port=8081)
    # HTTPS version
    # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire

    if HTTPS_MODE == False:
        # HTTP version
        app.run(debug=True, host="0.0.0.0", port=8081)
    else :
        # HTTPS version
        # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire
        context = ("resources/server-public-key.pem", "resources/server-private-key.pem")
        app.run(debug=True, host="127.0.0.1", port=8081, ssl_context=context)
   
