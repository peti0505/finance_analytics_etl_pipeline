MERGE transactions_main AS target
USING transactions_temp as source
ON target.Transaction_id = source.Transaction_id
WHEN MATCHED THEN
UPDATE SET Transaction_date = source.Transaction_date,
Date_only = source.Date_only,
Type = source.Type,
Partner_name = source.Partner_name,
Partner_account = source.Partner_account,
Spending_category = source.Spending_category,
Description = source.Description,
Amount = source.Amount
WHEN NOT MATCHED THEN
INSERT (Transaction_id, Transaction_date, Date_only, Type, Partner_name, Partner_account, Spending_category, Description, Amount)
VALUES (source.Transaction_id, source.Transaction_date, source.Date_only, source.Type, source.Partner_name, source.Partner_account, source.Spending_category, source.Description, source.Amount);