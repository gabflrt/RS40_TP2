import argparse
from run_server import db, User, app

def main(username, password):
    with app.app_context():
        # Vérifiez si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"L'utilisateur '{username}' a été créé.")
        else:
            print(f"L'utilisateur '{username}' existe déjà.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add a new user to the database.')
    parser.add_argument('username', type=str, help='The username of the new user')
    parser.add_argument('password', type=str, help='The password of the new user')
    
    args = parser.parse_args()
    main(args.username, args.password)
