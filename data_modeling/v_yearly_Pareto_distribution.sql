CREATE OR ALTER VIEW [dbo].[v_yearly_Pareto_distribution] AS
WITH year_and_partner_aggregated_expenses AS
(
SELECT
    YEAR(Date_only) AS date_year
    ,Partner_name
    --Expenses are negative in the data, making it positive for better visualization
    ,(SUM(Amount))*-1 AS yearly_total
FROM 
    transactions_main
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