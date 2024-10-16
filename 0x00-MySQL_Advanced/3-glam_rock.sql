SELECT band_name, 
       (IFNULL(split, YEAR(CURDATE())) - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
