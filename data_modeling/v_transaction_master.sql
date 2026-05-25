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
    transactions_main
