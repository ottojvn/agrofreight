# AgroFreight Intelligence

## Visão Geral
Solução de Business Intelligence "end-to-end" desenvolvida para monitoramento de volatilidade de fretes no setor agroindustrial. O sistema centraliza dados históricos de transporte para identificar rotas com margens de lucro decrescentes durante a safra.

## Arquitetura do Projeto
O projeto adota uma arquitetura híbrida, segregando a engenharia de dados da camada de visualização:

*   **Engenharia de Dados:** Pipeline ETL em Python e banco de dados SQL Server containerizado (Docker).
*   **Visualização:** Dashboard interativo em Power BI consumindo dados de uma instância SQL Server local.

## Estrutura do Repositório
*   `docs/`: Documentação técnica detalhada (Dicionário de Dados e Guia de Deploy).
*   `sql/`: Scripts DDL para criação do banco de dados.
*   `src/`: Scripts Python para geração de dados e pipeline ETL.
*   `docker-compose.yml`: Definição do serviço de banco de dados.

## KPIs Principais
*   **Custo Médio de Frete por Tonelada:** Análise temporal e por rota.
*   **Custo por Quilômetro:** Métrica de eficiência logística.
*   **Taxa de Rejeição:** Percentual de registros reprovados pelas regras de validação (Sanity Check).

## Roadmap e Status
O projeto está estruturado em Sprints para simular um ambiente ágil.

### Sprint 1: Infraestrutura e Modelagem (Concluído)
- [x] Configuração de ambiente containerizado (Docker).
- [x] Modelagem Dimensional (Star Schema).
- [x] Implementação do Banco de Dados (DDL).

### Sprint 2: Engenharia de Dados (Em Andamento)
- [x] Configuração do ambiente Python e dependências.
- [x] Geração de massa de dados sintética.
- [ ] Implementação de lógica de transformação e validação ("Logistics Sanity Check").
- [ ] Carga de dados no ambiente containerizado.

### Sprint 3: Migração e BI (Planejado)
- [ ] Migração de dados entre ambientes (Docker → Local).
- [ ] Conexão e modelagem no Power BI.
- [ ] Desenvolvimento de medidas DAX e Dashboards.

### Sprint 4: Documentação e Refinamento (Planejado)
- [ ] Refatoração de código e modularização.
- [ ] Testes end-to-end e validação final.

---
*Para detalhes sobre regras de negócio e esquema de dados, consulte [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).*
*Para instruções de configuração e execução, consulte [DEPLOYMENT.md](docs/DEPLOYMENT.md).*
