
-- Exécuter cette requete pour céer la table stg_online_retail avant 
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


