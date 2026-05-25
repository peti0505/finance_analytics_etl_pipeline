IF OBJECT_ID('dbo.transactions_main') IS NULL
BEGIN
    CREATE TABLE transactions_main
    (
        Transaction_id BIGINT PRIMARY KEY,
        Transaction_date DATETIME NOT NULL,
        Date_only DATE NOT NULL,
        Type VARCHAR(MAX) NOT NULL,
        Partner_name VARCHAR(MAX) NOT NULL,
        Partner_account VARCHAR(MAX) NOT NULL,
        Spending_category VARCHAR(MAX) NOT NULL,
        Description VARCHAR(MAX),
        AMOUNT FLOAT NOT NULL
    )
END