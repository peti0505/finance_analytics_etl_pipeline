# On-Premise Finance Analytics Pipeline
Automated end-to-end ETL data pipeline for tracking personal finance on an On-Premise Microsoft SQL Server.

<img width="720" height="405" alt="fvisualizationfinal" src="https://github.com/user-attachments/assets/bdd38cd1-7e49-4ecd-a85c-4004f8400c62" />


## Business problem
Tracking my finances was always a need of mine. Manual tracking and spreadsheets can be time consuming and prone to error, therefore the goal of this project was to build an automated pipeline that extracts raw data, cleans it, models it and visualizes it automatically.

## Architecture and Dataflow

(workflow diagram img)

## Tech Stack
* **Extraction and Transformation:** Python -> Pandas, comprehensive logging and error-handling
* **Data Loading & Orchestration:** Python -> SQLAlchemy, logged and error-handled aswell
* **Data Warehouse:**  Microsoft SQL Server 2022 -> On-Premise DWH
* **Modeling:** T-SQL -> Executing the `.sql` files with python. Making views and tables.
* **Containerization:** Docker and Docker Compose -> Separating the ETL pipeline and the MSSQL Server into different containers.
* **Visualization:** Power BI -> Dax measures, bookmarks

## Data Lineage

(data lineage img)

1. **Source:** Extracting transactions from `.csv`
2. **Loading:** The data is loaded into a temporary table.
3. **Core**: The new data from temp is upserted into the main table, preserving idempotency. Creating a date dimension table for future views.
4. **Analytics:** Making views to prepare the data for visualization.

## Project Structure

<details open>
<summary><b>Click here to collapse the full project structure</b></summary>

```text
(filetree here)
```
</details>

## Pipeline features
1. **Deterministic Surrogate Key:** <br>
Each transactions gets a deterministic key using the **hash_pandas_object** function so every row has an **unique key**. This is essential for future identification.
2. **Data Loading**: <br>
The data is loaded into the transactions_temp table with **replacing**, so only the latest batch will be stored here.
3. **Idempotency:** <br>
From the transactions_temp table the data is loaded into the transactions_main table using the **MERGE(upsert) statements** based on the **previously created deterministic IDs**.
4. **Modeling:** <br>
Every modeling that can be done in the database is made with SQL to spare Power BI as much as possible.
5. **Database-as-Code:** <br>
To maintain a **single source of truth** for the database all modeling and configuration is stored in .sql files using **Create OR ALTER** statements. These files are ran by python along the pipeline so it can be **version controlled and traced**.
6. **Visualization:** <br>
Where it is possible everything was done by **DAX** and **measures**.

**Note: The dummy_transactions.csv file contains fictional transactions, it doesn't resemble any bank account history.**

# How to Run Locally

### Prequisite
You need to have **Docker** and **Docker Compose** downloaded.

1. **Clone the repository:**
    ```bash
    git clone https://github.com/peti0505/finance_analytics_etl_pipeline.git
    cd finance_analytics_etl_pipeline
    ```

2. **Configure environment variables** <br>
Open the .envEXAMPLE file, write your environment variables according to the instructions then delete the .EXAMPLE from the file name.

3. **Start the pipeline::**  <br>
```bash
docker compose up -d
```

5. **Visualization**:
    * The .pbix file contains the data from the dummy transactions, you can explore it instantly.
    * If you want to use your own data connect to the database.
