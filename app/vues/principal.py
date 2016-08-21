from flask import render_template, jsonify, flash, redirect, url_for
import json
from app import app, db, modeles
from app.outils import utile
from app.formulaires import utilisateur as fu
from app.outils import email

@app.route('/carte')
def carte():
    return render_template('carte.html', titre='Carte')


@app.route('/carte_rafraichir', methods=['POST'])
def carte_rafraichir(self):
    conducteurs = modeles.Conducteur.query.all()
    geojson = [
        json.loads(
            db.session.scalar(
                ST_AsGeoJSON(
                    conducteur.position
                )
            )
        )
        for conducteur in conducteurs
    ]
    return jsonify({
        'positions': geojson,
        'conducteurs': conducteurs
    })


@app.route('/tarifs')
def tarifs():
    return render_template('tarifs.html', titre='Tarifs')


@app.route('/informations')
def informations():
    return render_template('informations.html', titre='Informations')


@app.route('/faq')
def faq():
    faq_data = utile.lire_json('app/static/data/faq.json')
    return render_template('faq.html', titre='FAQ', faq_data=faq_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = fu.Contact()

    if form.validate_on_submit():

        msg = form.data
        # Sujet du mail à envoyer
        sujet = form.objet.data
        # Le corps du mail est un template écrit en HTML
        html = render_template('email/requete_utilisateur.html', msg=msg)
        # Envoyer le mail à l'utilisateur
        email.envoyer(app.config['ADMINS'][1], sujet, html)

        flash('Votre email a été envoyé.', 'positive')
        return redirect(url_for('index'))

    return render_template('contact.html', titre='Contact', form=form)
