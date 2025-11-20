import pandas as pd
from sqlalchemy import create_engine, text

server = 'localhost\\SQLEXPRESS'
database = 'EcommerceDashboard'
driver = 'ODBC+Driver+17+for+SQL+Server'
engine = create_engine(f'mssql+pyodbc://{server}/{database}?driver={driver}')

with engine.begin() as conn:

    # ----------------------
    # Création des tables DW
    # ----------------------
    conn.execute(text("""
    IF OBJECT_ID('dim_customer', 'U') IS NULL
    CREATE TABLE dim_customer (
        CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
        CustomerID INT,
        Country NVARCHAR(255)
    );
    """))

    conn.execute(text("""
    IF OBJECT_ID('dim_product', 'U') IS NULL
    CREATE TABLE dim_product (
        StockCode NVARCHAR(50) PRIMARY KEY,
        Description NVARCHAR(255)
    );
    """))

    conn.execute(text("""
    IF OBJECT_ID('dim_date', 'U') IS NULL
    CREATE TABLE dim_date (
        DateKey INT PRIMARY KEY,
        FullDate DATE,
        Year INT,
        Month INT,
        Day INT
    );
    """))

    conn.execute(text("""
    IF OBJECT_ID('fact_sales', 'U') IS NULL
    CREATE TABLE fact_sales (
        InvoiceNo NVARCHAR(50),
        CustomerKey INT,
        StockCode NVARCHAR(50),
        DateKey INT,
        Quantity INT,
        UnitPrice FLOAT,
        TotalPrice FLOAT
    );
    """))

    # ----------------------
    # Chargement dim_customer
    # ----------------------
    # On insère une ligne par couple (CustomerID, Country) absent dans la dimension
    conn.execute(text("""
    INSERT INTO dim_customer (CustomerID, Country)
    SELECT CustomerID, Country
    FROM (
        SELECT DISTINCT CustomerID, Country
        FROM stg_online_retail
        WHERE CustomerID IS NOT NULL
    ) src
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_customer d
        WHERE d.CustomerID = src.CustomerID
          AND (d.Country = src.Country OR (d.Country IS NULL AND src.Country IS NULL))
    );
    """))

    # ----------------------
    # Chargement dim_product
    # ----------------------
    # On normalise : 1 row par StockCode; on choisit une description arbitraire (ORDER BY Description).
    conn.execute(text("""
    INSERT INTO dim_product (StockCode, Description)
    SELECT StockCode, Description
    FROM (
        SELECT StockCode, Description,
               ROW_NUMBER() OVER (PARTITION BY StockCode ORDER BY Description) AS rn
        FROM (
            SELECT DISTINCT StockCode, Description
            FROM stg_online_retail
            WHERE StockCode IS NOT NULL
        ) x
    ) y
    WHERE y.rn = 1
      AND NOT EXISTS (
          SELECT 1 FROM dim_product d WHERE d.StockCode = y.StockCode
      );
    """))

    # ----------------------
    # Chargement dim_date
    # ----------------------
    conn.execute(text("""
    INSERT INTO dim_date (DateKey, FullDate, Year, Month, Day)
    SELECT DateKey, FullDate, Year, Month, Day
    FROM (
        SELECT DISTINCT
            CONVERT(INT, CONVERT(VARCHAR, InvoiceDate, 112)) AS DateKey,
            CAST(InvoiceDate AS DATE) AS FullDate,
            YEAR(InvoiceDate) AS Year,
            MONTH(InvoiceDate) AS Month,
            DAY(InvoiceDate) AS Day
        FROM stg_online_retail
        WHERE InvoiceDate IS NOT NULL
    ) src
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_date d WHERE d.DateKey = src.DateKey
    );
    """))

    # ----------------------
    # Chargement fact_sales
    # ----------------------
    # On rejoint dim_customer sur CustomerID+Country pour récupérer CustomerKey
    conn.execute(text("""
    INSERT INTO fact_sales
        (InvoiceNo, CustomerKey, StockCode, DateKey, Quantity, UnitPrice, TotalPrice)
    SELECT
        s.InvoiceNo,
        c.CustomerKey,
        s.StockCode,
        CONVERT(INT, CONVERT(VARCHAR, s.InvoiceDate, 112)) AS DateKey,
        s.Quantity,
        s.UnitPrice,
        s.Quantity * s.UnitPrice AS TotalPrice
    FROM stg_online_retail s
    LEFT JOIN dim_customer c
        ON c.CustomerID = s.CustomerID
       AND (c.Country = s.Country OR (c.Country IS NULL AND s.Country IS NULL))
    WHERE s.InvoiceNo IS NOT NULL;
    """))

print("Ingestion DW terminée.")