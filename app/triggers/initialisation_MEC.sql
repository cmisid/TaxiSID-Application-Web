CREATE FUNCTION initialisation_montant_en_cours() RETURNS TRIGGER AS $initialisation_montant_en_cours$
	
	DECLARE
		nom_ent entreprises.nom%TYPE;

	BEGIN

		SELECT nom INTO nom_ent
		FROM entreprises
		WHERE montant_en_cours IS NULL;

		UPDATE entreprises 
		SET montant_en_cours = 0
		WHERE nom = nom_ent;
	return NULL;
	END;

$initialisation_montant_en_cours$ LANGUAGE 'plpgsql';

CREATE TRIGGER initialisation_montant_en_cours 
	AFTER INSERT ON entreprises
	EXECUTE PROCEDURE initialisation_montant_en_cours();
