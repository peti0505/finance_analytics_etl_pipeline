# %%
import os
import pandas as pd
import sqlalchemy as sa

# %%
df = pd.read_csv("dummy_transactions.csv", sep=";")
df.drop_duplicates()

# %%
# Deleted redundant columns and switched to english names for readability
df.drop(
    columns=[
        "Pénznem",
        "Könyvelés dátuma",
        "Bejövő/Kimenő",
        "Számla név",
        "Számla szám",
    ],
    inplace=True,
)
df.columns = [
    "Transaction_date",
    "Type",
    "Partner_name",
    "Partner_account",
    "Spending_category",
    "Description",
    "Amount",
]

# %%
# Had to format for appropriate data types
df["Amount"] = df["Amount"].str.replace(",", ".").str.replace(" ", "")
df["Amount"] = df["Amount"].astype(float)

# %%
df["Transaction_date"] = pd.to_datetime(
    df["Transaction_date"], format="%Y-%m-%d %H:%M:%S"
)
df.sort_values("Transaction_date", inplace=True, ignore_index=True)
df.insert(1, "Date_only", df["Transaction_date"].dt.date)


# %%
# Switched Nulls to Unknown in case of future use in visualization
df["Partner_account"] = df["Partner_account"].fillna("Unknown")
df["Partner_account"] = df["Partner_account"].astype(str)

# %%
# Description column had some HTML spacing
df["Description"] = df["Description"].str.replace("&nbsp;", " ")


# %%
# Extracting to SQL, if failed then extracting into .csv and .xlsx instead
try:
    db_user = os.environ.get("db_login_name")
    db_passw = os.environ.get("db_login_passw")
    engine = sa.create_engine(
        f"mssql+pyodbc://{db_user}:{db_passw}@localhost\\SQLEXPRESS/finance_project?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    df.to_sql("finance_table", engine, index=True, if_exists="append")
except Exception as e:
    print("Couldn't write to SQL server, exported to csv and xlsx", e)
    df.to_csv("finance_table_substitution.csv")
    df.to_excel("finance_table.xlsx")
