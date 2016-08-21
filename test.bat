:: On installe les packages nécessaire
pip install -r requirements.txt
:: On supprime l'ancienne BD
python suppression.py
:: On crée la BD
python creation.py
:: On remplit la BD
python insertions.py
:: On lance les tests
py.test tests\test_trigger_verif_banni.py
py.test tests\test_trigger_ajout_position_conducteur.py
py.test tests\test_trigger_suppr_propositions.py
py.test tests\test_trigger_verif_heure_depart.py
py.test tests\test_calculer_ratios.py
py.test tests\test_duree_trajet.py
py.test tests\test_estimation_precise.py
py.test tests\test_seuil.py
py.test tests\test_trigger_initialisation_MEC.py
py.test tests\test_trigger_verif_tarif.py
py.test tests\test_utiles.py
py.test tests\test_course.py
py.test tests\test_lister_conducteurs.py
py.test tests\test_trigger_verif_entreprise.py
:: On lance l'application
python run.py