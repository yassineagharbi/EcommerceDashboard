import os
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text

server = 'localhost\\SQLEXPRESS'
database = 'EcommerceDashboard'
driver = 'ODBC+Driver+17+for+SQL+Server'
engine = create_engine(f'mssql+pyodbc://{server}/{database}?driver={driver}')

# Extraction des données
file_path = 'C:/Users/Moi/sql-insurance-dw/EcommerceDashboard/data/data_retail_online.xlsx'
df = pd.read_excel(file_path)

# Transformation (exemple : nettoyage)
df = df.dropna(subset=['CustomerID', 'InvoiceDate'])
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# --- Création de la table stg_retail_online 
with engine.begin() as conn:
    conn.execute(text("""
    IF OBJECT_ID('dbo.stg_online_retail', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.stg_online_retail (
            InvoiceNo       NVARCHAR(50),
            StockCode       NVARCHAR(50),
            Description     NVARCHAR(255),
            Quantity        INT,
            InvoiceDate     DATETIME,
            UnitPrice       DECIMAL(10,2),
            CustomerID      INT,
            Country         NVARCHAR(255)
        );
        CREATE INDEX idx_stg_customer ON dbo.stg_online_retail(CustomerID);
        CREATE INDEX idx_stg_invoice_date ON dbo.stg_online_retail(InvoiceDate);
    END;
    """))
    print("Table stg_online_retail et indexes vérifiés/créés.")

# Chargement en SQL Server dans stg_retail_online (staging)
df.to_sql('stg_online_retail', engine, if_exists='replace', index=False)
print("Données chargées dans SQL Server")

