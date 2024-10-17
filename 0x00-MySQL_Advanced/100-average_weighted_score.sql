-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE T_weighted_score INT DEFAULT 0;
    DECLARE T_weight INT DEFAULT 0;

    -- Calculate total weighted score
    SELECT SUM(corrections.score * projects.weight)
    INTO T_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate total weight
    SELECT SUM(projects.weight)
    INTO T_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Check if the total weight is zero to avoid division by zero
    IF T_weight = 0 THEN
        UPDATE users
        SET users.average_score = 0
        WHERE users.id = user_id;
    ELSE
        UPDATE users
        SET users.average_score = T_weighted_score / T_weight
        WHERE users.id = user_id;
    END IF;
    
END$$

DELIMITER ;
