from threading import Thread
from flask.ext.mail import Message
from app import app, mail


def envoyer(destinataire, sujet, corps):
    '''
    Envoyer un mail à une adresse email. Le corps du message est normalement
    du HTML généré à partir de Flask. Les coordonnées de l'expediteur sont
    précisées dans le fichier config.py.
    '''
    expediteur = app.config['ADMINS'][0]
    message = Message(sujet, sender=expediteur, recipients=[destinataire])
    message.html = corps
    # Create a new thread
    thr = Thread(target=envoyer_asynchrone, args=[app, message])
    thr.start()


def envoyer_asynchrone(app, message):
    ''' Envoyer le mail de façon asynchrone. '''
    with app.app_context():
        mail.send(message)