CREATE OR ALTER   view [dbo].[v_balance] AS
With byday AS
(
SELECT
    Date_only AS Date 
    ,Sum(Amount) AS daily_movement
FROM
    finance_table
GROUP BY 
    Date_only
),

accumulated AS
(
SELECT 
    dates_dim
    ,COALESCE(daily_movement,0) as daily_movement
    ,SUM(COALESCE(daily_movement,0)) OVER(ORDER BY dates_dim) AS running_total
FROM 
    date_dim as dd  
    LEFT JOIN byday as bd
    ON dd.dates_dim = bd.date
WHERE 
    dd.dates_dim  >= (SELECT MIN(date) FROM byday)
    AND dd.dates_dim <= (SELECT MAX(date) FROM byday)
)

SELECT
    dates_dim AS Date
    ,running_total
    ,AVG(running_total) OVER(ORDER BY dates_dim ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS moving_average
FROM
    accumulated