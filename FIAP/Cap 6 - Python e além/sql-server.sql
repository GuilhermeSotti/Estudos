USE [master];

CREATE LOGIN [admin] 
WITH PASSWORD = 'adm!1234', 
     CHECK_POLICY = OFF;
CREATE USER [admin] FOR LOGIN [admin];
ALTER ROLE db_owner ADD MEMBER [admin];

CREATE USER [admin] FOR LOGIN [admin];

ALTER ROLE db_owner ADD MEMBER [admin];
GO
CREATE SCHEMA raw_data;
GO
CREATE SCHEMA staging;
GO
CREATE SCHEMA analytics;
GO
CREATE TABLE raw_data.tb_faostat_raw (
  source      NVARCHAR(50)    NOT NULL,
  ingest_ts   DATETIME2       DEFAULT SYSUTCDATETIME() NOT NULL,
  payload     NVARCHAR(MAX)   NOT NULL
);
GO
CREATE TABLE raw_data.tb_comexstat_raw (
  source      NVARCHAR(50)    NOT NULL,
  ingest_ts   DATETIME2       DEFAULT SYSUTCDATETIME() NOT NULL,
  payload     NVARCHAR(MAX)   NOT NULL
);
GO

CREATE TABLE staging.stg_insumos (
  insumo_id   INT IDENTITY(1,1) PRIMARY KEY,
  cultura     NVARCHAR(100)   NOT NULL,
  pais        NVARCHAR(100),
  quantidade  FLOAT,
  unidade     NVARCHAR(20),
  ano         INT,
  load_ts     DATETIME2       DEFAULT SYSUTCDATETIME() NOT NULL,
  valid_flag  CHAR(1)         DEFAULT 'Y' NOT NULL
);

CREATE TABLE analytics.dim_cultura (
    cultura_id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE analytics.dim_produtor (
    produtor_id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    region_id INT NOT NULL
);

CREATE TABLE analytics.fact_colheita (
    fact_id INT IDENTITY(1,1) PRIMARY KEY,
    produtor_id INT,
    cultura_id INT,
    data_id DATE,
    quantidade INT,
    perda_percent FLOAT,
    FOREIGN KEY (produtor_id) REFERENCES analytics.dim_produtor(produtor_id),
    FOREIGN KEY (cultura_id) REFERENCES analytics.dim_cultura(cultura_id)
);

INSERT INTO analytics.dim_cultura (nome)
VALUES 
    ('Milho'),
    ('Soja'),
    ('Café'),
    ('Trigo'),
    ('Arroz'),
    ('Feijão'),
    ('Tomate'),
    ('Batata'),
    ('Alface'),
    ('Cenoura'),
    ('Pepino'),
    ('Melancia'),
    ('Abóbora'),
    ('Laranja'),
    ('Limão'),
    ('Uva'),
    ('Pera'),
    ('Maçã'),
    ('Cebola'),
    ('Goiaba');

INSERT INTO analytics.dim_produtor (nome, region_id)
VALUES 
    ('Produtor A', 1),
    ('Produtor B', 2),
    ('Produtor C', 3),
    ('Produtor D', 4),
    ('Produtor E', 5),
    ('Produtor F', 6),
    ('Produtor G', 7),
    ('Produtor H', 8)

INSERT INTO analytics.fact_colheita (produtor_id, cultura_id, hora_insercao, quantidade, perda_percent)
VALUES 
    (1, 1, '2023-05-10', 1000, 5.0), 
    (1, 2, '2023-05-12', 2000, 3.0), 
    (1, 3, '2023-06-01', 1500, 4.0), 
    (1, 4, '2023-07-15', 500, 2.0),  
    (2, 5, '2023-08-10', 1200, 6.0), 
    (3, 6, '2023-09-05', 800, 7.0), 
    (3, 7, '2023-10-10', 600, 5.5), 
    (3, 8, '2023-11-20', 700, 4.5), 
    (2, 9, '2023-12-25', 400, 3.5), 
    (2, 10, '2024-01-15', 300, 8.0), 
    (4, 11, '2024-02-10', 1500, 5.2), 
    (4, 12, '2024-03-30', 1100, 6.0), 
    (5, 13, '2024-04-25', 1300, 4.7), 
    (5, 14, '2024-05-18', 1000, 3.0), 
    (6, 15, '2024-06-20', 800, 2.5),  
    (6, 16, '2024-07-12', 1200, 3.5), 
    (7, 17, '2024-08-10', 700, 6.5),  
    (8, 18, '2024-09-15', 1500, 4.0), 
    (8, 19, '2024-10-10', 1300, 5.0), 
    (8, 20, '2024-11-25', 1000, 7.0);
