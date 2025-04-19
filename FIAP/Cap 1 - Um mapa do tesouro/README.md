# Cap 1 - Um mapa do tesouro - Modelagem de Banco de Dados Relacional

## 📘 Visão Geral do Projeto

Este projeto foi desenvolvido pela equipe de desenvolvedores da startup **FarmTech Solutions** para atender a uma fazenda que migrou para Agricultura Digital. O objetivo é oferecer uma solução inteligente de **armazenamento e análise de dados coletados por sensores** agrícolas, além de registrar ajustes de irrigação e fertilização com rastreabilidade total.

## 🧠 Arquitetura do Banco de Dados

O banco foi modelado com base no uso de sensores do tipo:

- **S1** – Umidade do solo
- **S2** – pH do solo
- **S3** – Nutrientes (Fósforo e Potássio – NPK)

### 🔧 Entidades Principais

| Entidade             | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `Produtor`           | Dados do agricultor responsável.                                          |
| `Plantacao`          | Área cultivada pelo produtor.                                             |
| `Cultura`            | Tipo de cultivo (ex: café, milho).                                        |
| `Sensor`             | Dispositivo instalado na lavoura.                                         |
| `Tipo de Sensor`     | Tipo do sensor do instalado na lavoura                                    |
| `Leitura do Sensor`  | Registro de dados em tempo real captados pelos sensores.                  |
| `Historico`          | Registro de histórico pai para auditoria e rastreabilidade.               |
| `Insumo`             | Produtos utilizados na plantação (fertilizantes, corretivos, etc.).       |
| `Ajuste de Insumo`   | Associação entre os insumos aplicados.                                    |

## 🖥️ Ferramentas Utilizadas

- Oracle SQL Developer Data Modeler
- GitHub para versionamento

---

## 📎 Documentação e Arquivos

- 🔗 [📄 DER - Modelo Entidade Relacionamento (PDF)](https://github.com/GuilhermeSotti/Estudos/blob/dev/FIAP/Cap%201%20-%20Um%20mapa%20do%20tesouro/Diagrama/DER%20-%20SubView.pdf)
- 🔗 [📂 Script SQL - Exportação do DDL (arquivo .sql)](https://github.com/GuilhermeSotti/Estudos/blob/dev/FIAP/Cap%201%20-%20Um%20mapa%20do%20tesouro/Diagrama/DER%20-%20BD%20SQL%20Server%202012.ddl)

---

## 🚀 Como Contribuir

1. Clone o repositório com `git clone`.
2. Abra o projeto no Oracle SQL Developer Data Modeler.
3. Execute ou modifique o script `DDL` conforme necessário.

---

## 🧑‍🌾 Objetivo Final

Com esta base de dados, a FarmTech oferece **uma gestão agrícola inteligente, baseada em dados reais**, promovendo **sustentabilidade, produtividade e inovação no campo**. 🌿

