SELECT 
    TUMOURID,
    COUNT(*) AS duplicate_count
FROM AV_TUMOUR
GROUP BY TUMOURID
HAVING COUNT(*) > 1;
 

