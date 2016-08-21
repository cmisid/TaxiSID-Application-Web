from flask import render_template
from app import app


@app.errorhandler(403)
def interfit(e):
    return render_template('erreur.html', message='403 accès interdit'), 403


@app.errorhandler(404)
def page_non_trouvee(e):
    return render_template('erreur.html', message='404 page non trouvée'), 404


@app.errorhandler(410)
def ne_fonctionne_plus(e):
    return render_template('erreur.html', message='410 ne fonctionne plus'), 410


@app.errorhandler(500)
def erreur_interne(e):
    return render_template('erreur.html', message='500 erreur interne'), 500
