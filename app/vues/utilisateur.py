from flask import (Blueprint, render_template, redirect, url_for,
                   abort, flash, Markup)
from flask.ext.login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from app import app, modeles, db
from app.formulaires import utilisateur as fu
from app.outils import email
from app.outils import geographie
from sqlalchemy import func
import datetime


# Serialiseur pour générer des tokens aléatoires
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Créer un patron pour les vues utilisateurs
utilisateurbp = Blueprint('utilisateurbp', __name__, url_prefix='/utilisateur')


@utilisateurbp.route('/enregistrement', methods=['GET', 'POST'])
def enregistrement():
    form = fu.Enregistrement()
    if form.validate_on_submit():

        check = modeles.Utilisateur.query.filter_by(
            telephone=form.telephone.data).first()
        if check is not None:
            if check.avoir_compte:
                flash("Vous êtes déja enregistré, veuillez vous connecter.", 'negative')
                return redirect(url_for('utilisateurbp.connexion'))
            else:
                # Géolocaliser l'adresse
                localisation = ' '.join([
                    form.numero.data,
                    form.adresse.data,
                    form.ville.data
                ])
                position = geographie.geocoder(localisation)
                # Créer une adresse
                adresse = modeles.Adresse(
                    nom_rue=form.adresse.data,
                    numero=form.numero.data,
                    cp=form.cp.data,
                    ville=form.ville.data,
                    position='POINT({0} {1})'.format(
                        position['lat'], position['lon'])
                )
                # Ajouter l'adresse à la BD
                db.session.add(adresse)
                db.session.commit()

                check.civilite = form.civilite.data
                check.email = form.email.data
                check.prenom = form.prenom.data
                check.nom = form.nom.data
                check.notification_email = True
                check.notification_sms = True
                check.adresse = adresse.identifiant
                check.inscription = datetime.datetime.utcnow()
                check.avoir_compte = True
                check.confirmer = False
                check.mdp = form.mdp.data

                db.session.commit()

                # Sujet du mail à envoyer
                sujet = 'Veuillez confirmer votre adresse email.'
                # Générer un token aléatoire
                token = ts.dumps(form.email.data, salt='email-confirm-key')
                # Construire un lien de confirmation à partir du token
                urlConfirmation = url_for('utilisateurbp.confirmation',
                                          token=token, _external=True)
                # Le corps du mail est un template écrit en HTML
                html = render_template('email/confirmation.html',
                                       url_confirmation=urlConfirmation)
                # Envoyer le mail à l'utilisateur
                email.envoyer(form.email.data, sujet, html)
                # On renvoit à la page d'accueil
                signUpMsg = Markup(
                    "<i class='mail outline icon'></i>Vérifiez vos mails pour confirmer votre adresse email.")
                flash(signUpMsg, 'positive')
                return redirect(url_for('index'))
        else:
            # Géolocaliser l'adresse
            localisation = ' '.join([
                form.numero.data,
                form.adresse.data,
                form.ville.data
            ])
            position = geographie.geocoder(localisation)
            # Créer une adresse
            adresse = modeles.Adresse(
                nom_rue=form.adresse.data,
                numero=form.numero.data,
                cp=form.cp.data,
                ville=form.ville.data,
                position='POINT({0} {1})'.format(
                    position['lat'], position['lon'])
            )
            # Ajouter l'adresse à la BD
            db.session.add(adresse)
            db.session.commit()
            # Créer un utilisateur qui n'a pas confirmé son mail
            utilisateur = modeles.Utilisateur(
                telephone=form.telephone.data,
                email=form.email.data,
                confirmation=False,
                civilite=form.civilite.data,
                prenom=form.prenom.data,
                nom=form.nom.data,
                notification_email=True,
                notification_sms=True,
                adresse=adresse.identifiant,
                mdp=form.mdp.data,
                inscription=datetime.datetime.utcnow(),
                avoir_compte=True
            )
            # Insérer un utilisateur dans la BD
            db.session.add(utilisateur)
            db.session.commit()
            # Sujet du mail à envoyer
            sujet = 'Veuillez confirmer votre adresse email.'
            # Générer un token aléatoire
            token = ts.dumps(utilisateur.email, salt='email-confirm-key')
            # Construire un lien de confirmation à partir du token
            urlConfirmation = url_for('utilisateurbp.confirmation',
                                      token=token, _external=True)
            # Le corps du mail est un template écrit en HTML
            html = render_template('email/confirmation.html',
                                   url_confirmation=urlConfirmation)
            # Envoyer le mail à l'utilisateur
            email.envoyer(utilisateur.email, sujet, html)
            # On renvoit à la page d'accueil
            signUpMsg = Markup(
                "<i class='mail outline icon'></i>Vérifiez vos mails pour confirmer votre adresse email.")
            flash(signUpMsg, 'positive')
            return redirect(url_for('index'))
    return render_template('utilisateur/enregistrement.html',
                           form=form, titre='Enregistrement')


@utilisateurbp.route('/confirmation/<token>', methods=['GET', 'POST'])
def confirmation(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    # Le token peut avoir expiré ou être invalide
    except:
        abort(404)
    # L'utilisateur a maintenant confirmé son mail
    db.session.execute('UPDATE utilisateurs SET confirmation=True ' +
                       "WHERE email='{}'".format(email))
    # On met à jour la BD
    db.session.commit()
    # On renvoit à la page de connexion
    flash('Votre adresse email a été confirmée, vous pouvez maintenant ' +
          'vous connecter.', 'positive')
    return redirect(url_for('utilisateurbp.connexion'))


@utilisateurbp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = fu.Connexion()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(
            email=form.email.data).first()
        # On vérifie que l'utilisateur existe
        if utilisateur is not None:
            # On vérifie ensuite que le mot de passe est correct
            if utilisateur.check_password(form.mdp.data):
                login_user(utilisateur)
                # On renvoit à la page d'accueil
                flash('Vous vous êtes connecté avec succès.', 'positive')
                return redirect(url_for('index'))
            else:
                flash('Vous avez rentré un mot de passe invalide.', 'negative')
                return redirect(url_for('utilisateurbp.connexion'))
        else:
            flash("Vous avez rentré une adresse email qui n'est pas associée " +
                  'à un compte.', 'negative')
            return redirect(url_for('utilisateurbp.connexion'))
    return render_template('utilisateur/connexion.html', form=form,
                           titre='Connexion')


@utilisateurbp.route('/deconnexion')
def deconnexion():
    logout_user()
    flash('Vous vous êtes déconnecté avec succès.', 'positive')
    return redirect(url_for('index'))


@utilisateurbp.route('/compte', methods=['GET', 'POST'])
@login_required
def compte():
    adresse = modeles.Adresse.query.filter_by(
        identifiant=current_user.adresse).first()

    # Requête comptant le nombre de courses effectuées par l'utilisateur
    req_nbCourses = "SELECT COUNT(*) FROM utilisateurs U, courses C WHERE U.telephone = C.utilisateur AND U.telephone='{0}'".format(
        current_user.telephone)
    nbCourses = db.session.execute(req_nbCourses).fetchall()
    nbCourses = nbCourses[0][0]
    print(nbCourses)

    req_hist = "SELECT ad.adr_complete as depart, adr.adr_complete as arriver, C.debut as debut FROM adresses ad, adresses adr, courses C, utilisateurs u WHERE ad.identifiant = C.depart AND adr.identifiant = C.arrivee AND u.telephone = C.utilisateur and c.utilisateur = '{0}'".format(
        current_user.telephone)
    tab_hist = db.session.execute(req_hist).fetchall()
    print(tab_hist)

    keys = ['depart', 'arrivee', 'debut']
    test = [dict(zip(keys, row)) for row in tab_hist]

    for el in range(len(test)):
        test[el]['debut'] = test[el]['debut'].strftime('%d-%m-%Y %H:%M')
    print(test)

    form = fu.Modification()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(
            email=current_user.email).first()

        utilisateur.prenom = form.prenom.data
        utilisateur.nom = form.nom.data
        utilisateur.telephone = form.telephone.data

        # Sauvegarder les modifications dans la BD
        db.session.commit()
        # Affichage de la modification
        signUpMsg = Markup(
            "<i class='thumbs outline up icon'></i>Vos informations personnelles ont bien été modifiées.")
        flash(signUpMsg, 'positive')
        return redirect(url_for('utilisateurbp.compte'))
    return render_template('utilisateur/compte.html', titre='Compte', form=form, adresse=adresse, nbCourses=nbCourses, test=test)


@utilisateurbp.route('/oubli', methods=['GET', 'POST'])
def oubli():
    form = fu.Oubli()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(
            email=form.email.data).first()
        # On vérifie que l'utilisateur existe
        if utilisateur is not None:
            # Sujet du mail de confirmation
            sujet = 'Veuillez réinitialiser votre mot de passe.'
            # Générer un token aléatoire
            token = ts.dumps(utilisateur.email, salt='password-reset-key')
            # Construire un lien de réinitialisation à partir du token
            urlReinitialisation = url_for('utilisateurbp.reinitialisation',
                                          token=token, _external=True)
            # Le corps du mail est un template écrit en HTML
            html = render_template('email/reinitialisation.html',
                                   url_reinitialisation=urlReinitialisation)
            # Envoyer le mail à l'utilisateur
            email.envoyer(utilisateur.email, sujet, html)
            # On renvoit à la page d'accueil
            flash('Vérifiez vos mails pour réinitialiser votre mot de passe.',
                  'positive')
            return redirect(url_for('index'))
        else:
            flash("Vous avez rentré une adresse email qui n'est pas associée " +
                  'à un compte.', 'negative')
            return redirect(url_for('utilisateurbp.oubli'))
    return render_template('utilisateur/oubli.html', form=form)


@utilisateurbp.route('/reinitialisation/<token>', methods=['GET', 'POST'])
def reinitialisation(token):
    try:
        email = ts.loads(token, salt='password-reset-key', max_age=86400)
    # Le token peut avoir expiré ou être invalide
    except:
        abort(404)
    form = fu.Reinitialisation()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(email=email).first()
        # On vérifie que l'utilisateur existe
        if utilisateur is not None:
            utilisateur.mdp = form.mdp.data
            # On met à jour la BD
            db.session.commit()
            # On renvoit à la page de connexion
            flash('Votre mot de passe a été mis à jour, vous pouvez ' +
                  'maintenant vous connecter.', 'positive')
            return redirect(url_for('utilisateurbp.connexion'))
        else:
            flash("Vous avez tapé une adresse email qui n'est associée " +
                  'à aucun compte.', 'negative')
            return redirect(url_for('utilisateurbp.oubli'))
    return render_template('utilisateur/reinitialisation.html',
                           form=form, token=token)
