-- Write a SQL script that creates a stored procedure 
-- ComputeAverageWeightedScoreForUsers that computes 
-- And store the average weighted score for all students.that

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  -- Update the users table with the average weighted score
  UPDATE users AS UD
  JOIN (
    -- Subquery to calculate the weighted average for each user
    SELECT 
      C.user_id AS user_id,
      SUM(C.score * P.weight) / SUM(P.weight) AS wei_AVG
    FROM 
      corrections AS C
    JOIN 
      projects AS P ON C.project_id = P.id
    GROUP BY 
      C.user_id
  ) AS W_AVG ON UD.id = W_AVG.user_id
  SET UD.average_weighted_score = W_AVG.wei_AVG;
  
END$$

DELIMITER ;
