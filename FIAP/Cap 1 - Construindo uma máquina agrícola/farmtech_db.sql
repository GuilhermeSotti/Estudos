USE [master];

CREATE LOGIN [admin] 
WITH PASSWORD = 'adm!1234', 
     CHECK_POLICY = OFF;
CREATE USER [admin] FOR LOGIN [admin];
ALTER ROLE db_owner ADD MEMBER [admin];

CREATE USER [admin] FOR LOGIN [admin];

ALTER ROLE db_owner ADD MEMBER [admin];
GO
CREATE SCHEMA Dados;
GO
CREATE SCHEMA Config;
GO
CREATE SCHEMA Monitoring;
GO

-- Tabela: Dados.Produtor
CREATE TABLE Dados.Produtor (
    produtor_id NUMBER PRIMARY KEY,
    nome VARCHAR(100),
    contato VARCHAR(50),
    endereco VARCHAR(255)
);

-- Tabela: Dados.Plantacao
CREATE TABLE Dados.Plantacao (
    plantacao_id NUMBER PRIMARY KEY,
    nome VARCHAR(100),
    lote NUMBER,
    area NUMBER(10,2),
    produtor_id NUMBER,
    FOREIGN KEY (produtor_id) REFERENCES Dados.Produtor(produtor_id)
);

-- Tabela: Dados.Cultura
CREATE TABLE Dados.Cultura (
    cultura_id NUMBER PRIMARY KEY,
    nome VARCHAR(100),
    descricao VARCHAR(255),
    plantacao_id NUMBER,
    FOREIGN KEY (plantacao_id) REFERENCES Dados.Plantacao(plantacao_id)
);

-- Tabela: Config.Insumo
CREATE TABLE Config.Insumo (
    insumo_id NUMBER PRIMARY KEY,
    nome VARCHAR(100),
    dosagem_recomendada NUMBER(10,2),
    cultura_id NUMBER,
    FOREIGN KEY (cultura_id) REFERENCES Dados.Cultura(cultura_id)
);

-- Tabela: Monitoring.Tipo_de_Sensor
CREATE TABLE Monitoring.Tipo_de_Sensor (
    tipo_id NUMBER PRIMARY KEY,
    modelo VARCHAR(100),
    tipo VARCHAR(100)
);

-- Tabela: Monitoring.Sensor
CREATE TABLE Monitoring.Sensor (
    sensor_id NUMBER PRIMARY KEY,
    tipo_id NUMBER,
    descricao VARCHAR(255),
    cultura_id NUMBER,
    FOREIGN KEY (tipo_id) REFERENCES Monitoring.Tipo_de_Sensor(tipo_id),
    FOREIGN KEY (cultura_id) REFERENCES Dados.Cultura(cultura_id)
);

-- Tabela: Monitoring.Historico
CREATE TABLE Monitoring.Historico (
    historico_id NUMBER PRIMARY KEY,
    data_registro TIMESTAMP,
    descricao VARCHAR(255),
    usuario VARCHAR(100),
    cultura_id NUMBER,
    FOREIGN KEY (cultura_id) REFERENCES Dados.Cultura(cultura_id)
);

-- Tabela: Monitoring.Leitura_do_Sensor
CREATE TABLE Monitoring.Leitura_do_Sensor (
    leitura_id NUMBER PRIMARY KEY,
    sensor_id NUMBER,
    valor NUMBER(10,2),
    historico_id NUMBER,
    FOREIGN KEY (sensor_id) REFERENCES Monitoring.Sensor(sensor_id),
    FOREIGN KEY (historico_id) REFERENCES Monitoring.Historico(historico_id)
);

-- Tabela: Monitoring.Ajuste_de_Insumos
CREATE TABLE Monitoring.Ajuste_de_Insumos (
    ajuste_id NUMBER PRIMARY KEY,
    insumo_id NUMBER,
    quantidade_aplicada NUMBER(10,2),
    historico_id NUMBER,
    FOREIGN KEY (insumo_id) REFERENCES Config.Insumo(insumo_id),
    FOREIGN KEY (historico_id) REFERENCES Monitoring.Historico(historico_id)
);
