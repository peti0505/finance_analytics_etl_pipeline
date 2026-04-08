USE [finance_project]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE OR ALTER     VIEW [dbo].[v_transaction_master] AS
SELECT
    Transaction_date AS Date
    ,DATENAME(dw, Transaction_date) AS Weekday
    --Converting week start to monday to match european standards
    ,CASE WHEN DATEPART(dw, Transaction_date) % 7 = 0 THEN 0 
        ELSE ((DATEPART(dw, Transaction_date)) + 6) % 7
    END AS weekday_number
    ,Amount
FROM 
    finance_table
GO



CREATE OR ALTER   view [dbo].[v_balance] AS
With byday AS
(
SELECT
    Transaction_date AS date 
    ,Sum(Amount) AS daily_movement
FROM
    finance_table
GROUP BY 
    Transaction_date
),

accumulated AS
(
SELECT 
    *
    ,SUM(daily_movement) OVER(ORDER BY date) AS running_total
FROM byday
)

SELECT
    running_total
    ,AVG(running_total) OVER(ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS moving_average
FROM
    accumulated
GO



CREATE OR ALTER VIEW [dbo].[v_yearly_Pareto_distribution] AS
WITH year_and_partner_aggregated_expenses AS
(
SELECT
    YEAR(Transaction_date) AS date_year
    ,Partner_name
    --Expenses are negative in the data, making it positive for better visualization
    ,(SUM(Amount))*-1 AS yearly_total
FROM 
    finance_table
WHERE 
    Amount < 0
GROUP BY    
    YEAR(Transaction_date)
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



