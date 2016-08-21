CREATE OR REPLACE FUNCTION verif_heure_depart() RETURNS TRIGGER AS $verif_heure_depart$
	DECLARE
		nb_err INTEGER;
	
	BEGIN  
      
        -- Vérifier lors de la création d'une course
		-- que l'heure de départ est bien postérieure au moment de la création
       
		SELECT COUNT(*) INTO nb_err
		FROM courses
		WHERE DATE_PART('day',debut - CURRENT_TIMESTAMP) * 24 + 
						DATE_PART('hour',debut - CURRENT_TIMESTAMP) *60 +
						DATE_PART('minutes',debut - CURRENT_TIMESTAMP) <= 0 AND
						finie is not TRUE;

		IF nb_err > 0 THEN
		RAISE EXCEPTION 'L''heure de depart de la course doit etre posterieure a l''heure de la commande';
		END IF;
	RETURN NULL;	
	END;
$verif_heure_depart$ lANGUAGE plpgsql;
    
CREATE TRIGGER verif_heure_depart
    AFTER INSERT OR UPDATE ON courses
    FOR EACH ROW EXECUTE PROCEDURE verif_heure_depart();