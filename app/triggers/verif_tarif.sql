CREATE OR REPLACE FUNCTION verif_tarif() RETURNS TRIGGER AS $verif_tarif$
	
	BEGIN

		IF (NEW.tarif NOT LIKE 'Jour') THEN
			IF(NEW.tarif NOT LIKE 'Nuit') THEN
				RAISE EXCEPTION 'Le tarif doit être de jour ou de nuit !';
			END IF;
		END IF;

	RETURN NULL;
	END;

$verif_tarif$ LANGUAGE plpgsql;

CREATE TRIGGER verif_tarif 
	AFTER INSERT OR UPDATE ON forfaits
	FOR EACH ROW EXECUTE PROCEDURE verif_tarif()
