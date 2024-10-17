-- Write a SQL script that creates a function SafeDiv that divides (and returns) 
-- the first by the second number or returns 0 if the second number is equal to 0.

DELIMITER $$

CREATE FUNCTION SafeDiv(
    i INT,
    j INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE result FLOAT;
    
    IF j = 0 THEN
        RETURN 0;
    END IF;
    
    SET result = (i * 1.0) / j;
    RETURN result;
END$$

DELIMITER ;
