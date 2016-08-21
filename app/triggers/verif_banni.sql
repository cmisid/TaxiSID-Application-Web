CREATE OR REPLACE FUNCTION verif_banni() RETURNS TRIGGER AS $verif_banni$
    
	DECLARE
		ComptBan INTEGER;
    
	BEGIN
    
        -- Vérifie qu'un utilisateur n'est pas bannit
        
        SELECT count(*) INTO ComptBan 
        FROM bannissements B
        WHERE B.utilisateur = NEW.utilisateur
		AND B.fin >= CURRENT_DATE;
        
		IF ComptBan > 0 THEN
            RAISE EXCEPTION 'l''utilisateur est actuellement bannit';
        END IF;
    return null;    
    END;
    
$verif_banni$ lANGUAGE plpgsql;     
    
CREATE TRIGGER verif_banni
    AFTER INSERT OR UPDATE ON Courses
    FOR EACH ROW EXECUTE PROCEDURE verif_banni();
    
-- Test verif_banni
-- Insert into bannissements values('+33628251338','05/01/2016','06/01/2016','Impolitesse')
-- Insert into Courses values(')
