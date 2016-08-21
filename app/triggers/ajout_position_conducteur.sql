CREATE OR REPLACE FUNCTION ajout_position_conducteur() RETURNS TRIGGER AS $ajout_position_conducteur$
    
	DECLARE
    
	BEGIN
	
        -- Lors de la mise à jour d'un conducteur, mettre sa position dans position pour garder un historique
        
		INSERT INTO positions VALUES(OLD.telephone, CURRENT_TIMESTAMP-time '00:00:10', OLD.position, OLD.statut);
    RETURN NULL;    
    END;
    
$ajout_position_conducteur$ LANGUAGE plpgsql;
    
CREATE TRIGGER ajout_position_conducteur
    AFTER UPDATE OF position ON conducteurs
    FOR EACH ROW EXECUTE PROCEDURE ajout_position_conducteur()