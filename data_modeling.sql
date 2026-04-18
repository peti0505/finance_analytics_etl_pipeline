USE [finance_project]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE OR ALTER     VIEW [dbo].[v_transaction_master] AS
SELECT
    Date_only AS Date
    ,DATENAME(dw, Date_only) AS Weekday
    --Converting week start to monday to match european standards
    ,CASE WHEN (DATEPART(dw, Date_only)+6) % 7 = 0 THEN 7
        ELSE ((DATEPART(dw, Date_only)) + 6) % 7
    END AS weekday_number
    ,Amount
FROM 
    finance_table
GO



CREATE OR ALTER   view [dbo].[v_balance] AS
With byday AS
(
SELECT
    Date_only AS date 
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
    dates_dim
    ,running_total
    ,AVG(running_total) OVER(ORDER BY dates_dim ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS moving_average
FROM
    accumulated
GO



CREATE OR ALTER VIEW [dbo].[v_yearly_Pareto_distribution] AS
WITH year_and_partner_aggregated_expenses AS
(
SELECT
    YEAR(Date_only) AS date_year
    ,Partner_name
    --Expenses are negative in the data, making it positive for better visualization
    ,(SUM(Amount))*-1 AS yearly_total
FROM 
    finance_table
WHERE 
    Amount < 0
GROUP BY    
    YEAR(Date_only)
    ,Partner_name
)

SELECT
    *
    ,yearly_total/SUM(yearly_total) OVER(PARTITION BY date_year)*100 AS yearly_percent
    ,SUM(yearly_total) OVER(PARTITION BY date_year ORDER BY yearly_total DESC)/
    SUM(yearly_total) OVER(PARTITION BY date_year) *100 AS rolling_yearly_percent
FROM
    year_and_partner_aggregated_expenses
GO



CREATE OR ALTER VIEW [dbo].[v_date_dimension] AS
SELECT
*
FROM 
    date_dim
WHERE  
    dates_dim >= (SELECT MIN(Date_only) FROM finance_table)
    AND dates_dim <= (SELECT MAX(Date_only) FROM finance_table)
GO




