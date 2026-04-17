USE finance_project
SET NOCOUNT ON
GO

DECLARE @datefiller DATE

IF OBJECT_ID('dbo.date_dim') IS NOT NULL
    DROP TABLE date_dim

CREATE TABLE date_dim
(
    dates_dim DATE PRIMARY KEY, 
    year_dim INT, 
    month_dim INT,
    monthname_dim VARCHAR(9), 
    day_dim INT,
    weekday_dim INT,
    weekdayname_dim VARCHAR(9)
)

SET @datefiller = '2000-01-01'

WHILE @datefiller != '2100-01-01'
BEGIN
    INSERT INTO date_dim 
    VALUES
    (@datefiller, 
    YEAR(@datefiller), 
    MONTH(@datefiller), 
    DATENAME(M, @datefiller),
    DAY(@datefiller),
    CASE WHEN (DATEPART(dw, @datefiller)+6) % 7 = 0 THEN 7
        ELSE ((DATEPART(dw, @datefiller)) + 6) % 7
    END,
    DATENAME(DW, @datefiller) 
    )
    SET @datefiller = DATEADD(DAY, 1, @datefiller)
END

ALTER TABLE finance_table ADD CONSTRAINT financeTable_dateOnly_FK
FOREIGN KEY (Date_only) REFERENCES date_dim(dates_dim)
