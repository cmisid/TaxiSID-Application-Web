CREATE OR REPLACE FUNCTION insert_montant_en_cours() RETURNS TRIGGER AS $insert_montant_en_cours$
    
	DECLARE
		
		prix_course INTEGER;
		entr courses.entreprise%TYPE;
		dep courses.depart%TYPE;
		arr courses.arrivee%TYPE;
		dest1 forfaits.destination_1%TYPE;
		dest2 forfaits.destination_2%TYPE;
		mont forfaits.montant%TYPE;
    
	BEGIN  
            
		SELECT montant into prix_course
		FROM factures 
		WHERE course = NEW.course;
        
		SELECT entreprise into entr
		FROM courses C, factures F
		WHERE C.numero = F.course
		AND F.course = NEW.course;

		IF entr != 'NULL' THEN

			SELECT depart into dep
			FROM courses C, factures F
			WHERE C.numero = F.course
			AND F.course = NEW.course;

			SELECT arrivee into arr
			FROM courses C, factures F
			WHERE C.numero = F.course
			AND F.course = NEW.course;

			SELECT destination_1 into dest1 
			FROM forfaits Forf, entreprises E, courses C, factures F
			WHERE Forf.entreprise = E.nom
			AND E.nom = C.entreprise
			AND C.numero = F.course
			AND F.course = NEW.course;

			SELECT destination_2 into dest2 
			FROM forfaits Forf, entreprises E, courses C, factures F
			WHERE Forf.entreprise = E.nom
			AND E.nom = C.entreprise
			AND C.numero = F.course
			AND F.course = NEW.course;

			IF dep = dest1 AND arr = dest2 OR dep = dest2 AND arr = dest1 THEN

				SELECT Forf.montant into mont 
				FROM forfaits Forf, entreprises E, courses C, factures F
				WHERE Forf.entreprise = E.nom
				AND E.nom = C.entreprise
				AND C.numero = F.course
				AND F.course = NEW.course;

				IF mont != prix_course THEN
					RAISE EXCEPTION 'Le montant de la course doit être le égal au montant du forfait';
				END IF;
			END IF;

            UPDATE entreprises
            SET montant_en_cours = montant_en_cours + prix_course
            WHERE nom in(SELECT nom 
						 FROM entreprises E, courses C, Factures F
						 WHERE E.nom = C.entreprise
						 AND C.numero = F.course
						 AND F.course = NEW.course);

		END IF;
	return null;
    END;
 
$insert_montant_en_cours$ lANGUAGE plpgsql;
    
CREATE TRIGGER insert_montant_en_cours
    AFTER INSERT ON factures
    FOR EACH ROW EXECUTE PROCEDURE insert_montant_en_cours();