-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-04-19 16:34:45 BRT
--   site:      SQL Server 2012
--   tipo:      SQL Server 2012



CREATE TABLE Monitoring."Ajuste de Insumos" 
    (
     ajuste_id NUMERIC (28) NOT NULL , 
     insumo_id NUMERIC (28) NOT NULL , 
     quantidade_aplicada NUMERIC (10,2) NOT NULL , 
     historico_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Monitoring."Ajuste de Insumos" ADD CONSTRAINT "Ajuste de Insumos_PK" PRIMARY KEY CLUSTERED (ajuste_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Dados.Cultura 
    (
     cultura_id NUMERIC (28) NOT NULL , 
     nome NVARCHAR (100) , 
     descricao NVARCHAR (255) , 
     plantacao_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Dados.Cultura ADD CONSTRAINT Cultura_PK PRIMARY KEY CLUSTERED (cultura_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Monitoring.Historico 
    (
     historico_id NUMERIC (28) NOT NULL , 
     data_registro DATETIME NOT NULL , 
     descricao NVARCHAR (255) , 
     usuario NVARCHAR (100) NOT NULL , 
     cultura_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Monitoring.Historico ADD CONSTRAINT Historico_PK PRIMARY KEY CLUSTERED (historico_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Config.Insumo 
    (
     insumo_id NUMERIC (28) NOT NULL , 
     nome NVARCHAR (100) NOT NULL , 
     dosagem_recomendada NUMERIC (10,2) NOT NULL , 
     cultura_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Config.Insumo ADD CONSTRAINT Insumo_PK PRIMARY KEY CLUSTERED (insumo_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Monitoring."Leitura do Sensor" 
    (
     leitura_id NUMERIC (28) NOT NULL , 
     sensor_id NUMERIC (28) NOT NULL , 
     valor NUMERIC (10,2) NOT NULL , 
     historico_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Monitoring."Leitura do Sensor" ADD CONSTRAINT Leitura_PK PRIMARY KEY CLUSTERED (leitura_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Dados.Plantacao 
    (
     plantacao_id NUMERIC (28) NOT NULL , 
     nome NVARCHAR (100) NOT NULL , 
     lote NUMERIC (28) NOT NULL , 
     area NUMERIC (10,2) NOT NULL , 
     produtor_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Dados.Plantacao ADD CONSTRAINT Plantacao_PK PRIMARY KEY CLUSTERED (plantacao_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Dados.Produtor 
    (
     produtor_id NUMERIC (28) NOT NULL , 
     nome NVARCHAR (100) , 
     contato NVARCHAR (50) , 
     endereco NVARCHAR (255) 
    )
GO

ALTER TABLE Dados.Produtor ADD CONSTRAINT Produtor_PK PRIMARY KEY CLUSTERED (produtor_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Monitoring.Sensor 
    (
     sensor_id NUMERIC (28) NOT NULL , 
     tipo_id NUMERIC (28) NOT NULL , 
     descricao NVARCHAR (255) , 
     cultura_id NUMERIC (28) NOT NULL 
    )
GO

ALTER TABLE Monitoring.Sensor ADD CONSTRAINT Sensor_PK PRIMARY KEY CLUSTERED (sensor_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE Monitoring."Tipo de Sensor" 
    (
     tipo_id NUMERIC (28) NOT NULL , 
     modelo NVARCHAR (100) NOT NULL , 
     tipo NVARCHAR (100) NOT NULL 
    )
GO

ALTER TABLE Monitoring."Tipo de Sensor" ADD CONSTRAINT "Tipo de Sensor_PK" PRIMARY KEY CLUSTERED (tipo_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

ALTER TABLE Dados.Cultura 
    ADD CONSTRAINT "1:N → Cultura" FOREIGN KEY 
    ( 
     plantacao_id
    ) 
    REFERENCES Dados.Plantacao 
    ( 
     plantacao_id 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Dados.Plantacao 
    ADD CONSTRAINT "1:N → Plantacao" FOREIGN KEY 
    ( 
     produtor_id
    ) 
    REFERENCES Dados.Produtor 
    ( 
     produtor_id 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring.Historico 
    ADD CONSTRAINT Historico_Cultura_FK FOREIGN KEY 
    ( 
     cultura_id
    ) 
    REFERENCES Dados.Cultura 
    ( 
     cultura_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring.Sensor 
    ADD CONSTRAINT Sensor_Cultura_FK FOREIGN KEY 
    ( 
     cultura_id
    ) 
    REFERENCES Dados.Cultura 
    ( 
     cultura_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring.Sensor 
    ADD CONSTRAINT "Sensor_Tipo de Sensor_FK" FOREIGN KEY 
    ( 
     tipo_id
    ) 
    REFERENCES Monitoring.""Tipo de Sensor"" 
    ( 
     tipo_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Config.Insumo 
    ADD CONSTRAINT TABLE_20_Cultura_FK FOREIGN KEY 
    ( 
     cultura_id
    ) 
    REFERENCES Dados.Cultura 
    ( 
     cultura_id 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring."Leitura do Sensor" 
    ADD CONSTRAINT TABLE_23_Historico_FK FOREIGN KEY 
    ( 
     historico_id
    ) 
    REFERENCES Monitoring.Historico 
    ( 
     historico_id 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring."Leitura do Sensor" 
    ADD CONSTRAINT TABLE_23_Sensor_FK FOREIGN KEY 
    ( 
     sensor_id
    ) 
    REFERENCES Monitoring.Sensor 
    ( 
     sensor_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring."Ajuste de Insumos" 
    ADD CONSTRAINT TABLE_24_Historico_FK FOREIGN KEY 
    ( 
     historico_id
    ) 
    REFERENCES Monitoring.Historico 
    ( 
     historico_id 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
GO

ALTER TABLE Monitoring."Ajuste de Insumos" 
    ADD CONSTRAINT TABLE_24_Insumo_FK FOREIGN KEY 
    ( 
     insumo_id
    ) 
    REFERENCES Config.Insumo 
    ( 
     insumo_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             9
-- CREATE INDEX                             0
-- ALTER TABLE                             19
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE DATABASE                          0
-- CREATE DEFAULT                           0
-- CREATE INDEX ON VIEW                     0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE ROLE                              0
-- CREATE RULE                              0
-- CREATE SCHEMA                            0
-- CREATE SEQUENCE                          0
-- CREATE PARTITION FUNCTION                0
-- CREATE PARTITION SCHEME                  0
-- 
-- DROP DATABASE                            0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
