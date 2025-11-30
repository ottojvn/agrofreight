# AgroFreight Intelligence

## Sobre o Projeto
O AgroFreight Intelligence é uma solução de Business Intelligence (End-to-End) desenvolvida para monitorar a volatilidade de custos de frete no setor do agronegócio. O sistema centraliza dados históricos de transporte e custos de combustível para identificar rotas com margens de lucro comprometidas durante o período de safra.

## Objetivos Técnicos
Este projeto demonstra a construção de um pipeline de dados robusto, focando nas seguintes competências:

1.  **Engenharia de Dados e ETL:** Desenvolvimento de scripts em Python para ingestão de dados e implementação de algoritmos de "Sanidade Logística" para validação de consistência (ex: rejeição de registros com telemetria inviável).
2.  **Data Warehousing:** Modelagem e implementação de banco de dados relacional em SQL Server utilizando arquitetura Star Schema (Fatos e Dimensões).
3.  **Análise de Dados:** Criação de dashboards em Power BI para visualização de indicadores chave (KPIs) como Custo por Tonelada/KM e variação de preço do Diesel.

## Stack Tecnológico
-   **Linguagem:** Python 3.10+ (Pandas, NumPy, SQLAlchemy, PyODBC).
-   **Banco de Dados:** Microsoft SQL Server 2022.
-   **Visualização:** Microsoft Power BI.
-   **Controle de Versão:** Git & GitHub.

## Estrutura do Repositório
-   **docs/**: Contém as regras de negócio (Project Charter) e especificações técnicas.
-   **src/**: Código fonte dos scripts de ETL e validação de dados.
-   **sql/**: Scripts DDL para criação de tabelas e procedures no banco de dados.
-   **BACKLOG.md**: Lista mestre de requisitos e planejamento de sprints.

## Status do Projeto
Atualmente em fase de desenvolvimento (Sprint 1), com foco na configuração do ambiente e modelagem de dados no SQL Server.
