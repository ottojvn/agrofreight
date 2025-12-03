# AgroFreight Intelligence

## Visão Geral

Solução de Business Intelligence "end-to-end" desenvolvida para monitoramento estratégico de logística no setor agroindustrial. O sistema centraliza dados de transporte para identificar ineficiências de rotas e volatilidade de fretes durante a safra.

O projeto segue uma abordagem evolutiva, iniciando como um MVP em ambiente controlado (On-Premise/Docker) e expandindo para uma arquitetura Enterprise Cloud-Native (Azure).

## Arquitetura e Evolução

O ciclo de vida do projeto é dividido em duas fases estratégicas:

### Fase 1: Core & MVP (Estado Atual)

Foco na validação de regras de negócio (Sanity Check), modelagem dimensional e visualização.

* **Engenharia:** Pipeline ETL em Python (Pandas/SQLAlchemy).
* **Infraestrutura:** SQL Server containerizado via Docker.
* **Visualização:** Power BI conectado a instância local.

### Fase 2: Expansão Enterprise (Roadmap Futuro)

Migração para o ecossistema Microsoft Azure visando escalabilidade, telemetria IoT e processamento massivo.

* **IoT Industrial:** Simulação de telemetria embarcada (C++) enviando dados via MQTT para **Azure IoT Hub**.
* **Big Data:** Processamento distribuído com **Azure Databricks (Spark)** e arquitetura Medalhão (Bronze/Silver/Gold).
* **Cloud & DevOps:** Infraestrutura como Código (IaC) com **Terraform** e orquestração via **Azure Data Factory**.
* **Armazenamento:** Migração para **Azure SQL Database** e **Data Lake Gen2**.

## Estrutura do Repositório

* `docs/`: Documentação técnica (Dicionário de Dados e Guia de Deploy).
* `sql/`: Scripts DDL para o ambiente Core (SQL Server).
* `src/etl/`: Scripts Python para ingestão e transformação (Fase 1).
* `src/iot/`: (Futuro) Código C++ para simulação de sensores e envio MQTT.
* `infra/`: (Futuro) Scripts Terraform para provisionamento Azure.

## KPIs Principais

* **Custo Médio de Frete (R$/Ton):** Análise temporal e sazonal.
* **Eficiência Logística (R$/Km):** Comparativo de rentabilidade por rota.
* **Integridade de Dados (Data Quality):** Taxa de rejeição de registros baseada em regras físicas (velocidade/tempo).

## Roadmap de Execução

### Fase 1: MVP (Local/Docker)

* [x] **Sprint 1:** Infraestrutura containerizada e Modelagem Star Schema.

* [x] **Sprint 2:** Engenharia de Dados (Geração de massa e ETL Python).
* [ ] **Sprint 3:** Visualização e Storytelling com Power BI.
* [ ] **Sprint 4:** Refinamento, modularização e documentação técnica.

### Fase 2: Expansão Enterprise (Azure)

* [ ] **Expansão I (Infraestrutura):** Provisionamento de Azure SQL e Data Lake via Terraform.

* [ ] **Expansão II (IoT Industrial):** Desenvolvimento de simulador de telemetria em **C++** e ingestão via **Azure IoT Hub**.
* [ ] **Expansão III (Big Data):** Migração do ETL para **Databricks (PySpark)** e implementação de Governança de Dados.

---
*Para regras de negócio detalhadas, consulte [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).*
*Para configuração do ambiente atual (Fase 1), consulte [DEPLOYMENT.md](docs/DEPLOYMENT.md).*
