CREATE OR REPLACE FUNCTION assoc_adresse_station() RETURNS TRIGGER AS $assoc_adresse_station$
	DECLARE
	id_adresse adresses.identifiant%TYPE;
	position_adresse adresses.position%TYPE;
	station_adresse stations.nom%TYPE;
	curseur SCROLL CURSOR IS SELECT s.nom, s.adresse, a.position, s.distance_entree
						FROM stations s, adresses a
						WHERE s.adresse = a.identifiant;
	ma_ligne curseur%TYPE;
	distance float;
	
	BEGIN
	
		-- On selectionne l'id de l'adresse qui vient d'être ajoutée
		SELECT identifiant INTO id_adresse
		FROM adresses
		WHERE station IS NULL;
		
		-- On selectionne la position de l'adresse qui d'être ajouté
		SELECT position INTO position_adresse
		FROM adresses
		WHERE station IS NULL;
		

		
		-- On initialise distance à  une grande distance	
		distance = 999999;

		-- On cherche la station la plus proche		
		FOR C1 IN curseur LOOP
		
			FETCH curseur INTO ma_ligne;
			
				

				IF st_distance(st_astext(position_adresse)::geography, st_astext(C1.position)::geography)-C1.distance_entree < distance THEN


					distance = st_distance(st_astext(position_adresse)::geography, st_astext(C1.position)::geography)-C1.distance_entree;
				
				
					--On met à jour le champs section
					UPDATE adresses
					set station = C1.nom
					WHERE identifiant = id_adresse;
					
				
				END IF;
				
				
		END LOOP;
		
		
	RETURN NULL;
	END;
$assoc_adresse_station$ lANGUAGE plpgsql;     
    
CREATE TRIGGER assoc_adresse_station
    AFTER INSERT ON adresses
    EXECUTE PROCEDURE assoc_adresse_station();
