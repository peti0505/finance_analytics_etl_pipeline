# finance_analytics_pipeline
Automated end-to-end ETL data pipeline for personal finance tracking using Python (Pandas), MSSQL and Power BI/DAX

<img width="720" height="405" alt="visualization" src="https://github.com/user-attachments/assets/a2872318-93e7-4c5f-ac07-8255295e77d0" />

## Business problem
Tracking my finances was always a need of mine. Manual tracking and spreadsheets can be time consuming and prone to error, therefore the goal of this project was to build an automated pipeline that extracts raw data, cleans it, models it and visualizes it automatically.

## Tech Stack
The main stack used: **Python -> MSSQL / T-SQL -> Power BI/DAX**

### 1. Data Cleaning (Python/Pandas)
* **Data extraction:** Getting the data from raw CSV file from the banking portal.
* **Data Cleaning:** Getting rid of redundant columns and formatting the data to set the appropriate data types, managing NaN values, etc.
* **Data Loading:** Loading the data into MS SQL Server via **SQLAlchemy** using **Environment Variables**. 

### 2. Data Modeling (SQL Views)
* Making **SQL Views** so Power BI can automatically can refresh if the data changes.
* The heavy lifting is done here as much as possible, so minimal work is left to do in Power BI for **efficiency and transparency**.

### 3. Visualization (Power BI/DAX)
* Connect directly to SQL Views.
* Using **DAX** everywhere it's possible, so the structure is cleaner and more transparent.
* The dashboard contains meaningful visualizations with **Slicers and Bookmarks** helping to understand what happens with the money.


## Data Privacy
**Note:** Regarding my personal and financial privacy I used a ~50 row transactional sample called 'dummy_transactions.csv' instead of the real CSV file. It meant to mimic the structure and the problems of the original transactions.csv file.


# How to Run Locally
1. **Clone the repository:** 
    git clone https://github.com/peti0505/finance_analytics_pipeline.git

2. Setup the following environment variables:
    **Windows Powershell:**
   ```powershell
   $env:db_server="your_servername"        # eg. localhost\SQLEXPRESS
   $env:db_name="your_dbname"             # eg. finance_project
   $env:db_login_name="your_dbusername"
   $env:db_login_passw="your_dbpassword"
   ```
    **Mac/Linux:**
   ```bash
   export db_server="your_servername"    # eg. localhost\SQLEXPRESS
   export db_name="your_dbname"           # eg. finance_project
   export db_login_name="your_dbusername"
   export db_login_passw="your_dbpassword"
   ```
3. Make sure you have a MS SQL Server instance with a database usable for this pipeline.

4. **Executing**:
    Run the data_cleaning/data_cleaning.py and all the .sql files in the data_modeling folder to set everything up.

5. **Visualization**:
    Open the .pbix file and ensure that the connection to your MS SQL server is correct so it can be refreshed automatically.
