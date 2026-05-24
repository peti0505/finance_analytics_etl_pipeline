CREATE OR ALTER VIEW [dbo].[v_date_dimension] AS
SELECT
*
FROM 
    date_dim
WHERE  
    dates_dim >= (SELECT MIN(Date_only) FROM finance_table)
    AND dates_dim <= (SELECT MAX(Date_only) FROM finance_table)