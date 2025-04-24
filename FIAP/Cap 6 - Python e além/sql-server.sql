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

CREATE TABLE analytics.dim_produtor (
  produtor_id INT IDENTITY(1,1) PRIMARY KEY,
  nome        NVARCHAR(150) NOT NULL,
  region_id   INT
);
GO
CREATE TABLE analytics.dim_cultura (
  cultura_id  INT IDENTITY(1,1) PRIMARY KEY,
  nome        NVARCHAR(100)  NOT NULL
);
GO
CREATE TABLE analytics.dim_tempo (
  data_id     DATE            NOT NULL PRIMARY KEY,
  ano         INT             NOT NULL,
  mes         INT             NOT NULL,
  dia         INT             NOT NULL
);
GO
CREATE TABLE analytics.fact_colheita (
  fact_id       INT IDENTITY(1,1) PRIMARY KEY,
  produtor_id   INT           NOT NULL,
  cultura_id    INT           NOT NULL,
  data_id       DATE          NOT NULL,
  quantidade    FLOAT,
  perda_percent DECIMAL(5,2),
  CONSTRAINT fk_colheita_produtor FOREIGN KEY (produtor_id) REFERENCES analytics.dim_produtor(produtor_id),
  CONSTRAINT fk_colheita_cultura  FOREIGN KEY (cultura_id)  REFERENCES analytics.dim_cultura(cultura_id),
  CONSTRAINT fk_colheita_tempo    FOREIGN KEY (data_id)      REFERENCES analytics.dim_tempo(data_id)
);
GO
CREATE VIEW analytics.vw_dashboard_insumos AS
SELECT c.nome   AS cultura,
       AVG(f.quantidade) AS qtd_media,
       AVG(f.perda_percent) AS perda_media
FROM analytics.fact_colheita AS f
JOIN analytics.dim_cultura AS c
  ON f.cultura_id = c.cultura_id
GROUP BY c.nome;
GO
