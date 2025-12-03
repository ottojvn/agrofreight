# Guia de Implantação e Infraestrutura

Este documento detalha os procedimentos para configuração do ambiente atual (Fase 1 - MVP) e descreve a arquitetura de referência para a futura expansão em nuvem (Fase 2 - Enterprise).

---

## 1. Fase 1: Ambiente MVP (Atual)

O ambiente atual opera em arquitetura local containerizada, focado em validação de engenharia e modelagem de dados.

### Pré-requisitos

* **Container Engine:** Docker e Docker Compose.
* **Linguagem:** Python 3.10+.
* **Banco de Dados:** SQL Server 2022 (Imagem Container).
* **Visualização:** Power BI Desktop (Ambiente Windows).
* **Drivers:** ODBC Driver 17 ou 18 para SQL Server.

### Procedimentos de Instalação

#### 1.1. Banco de Dados (Docker)

1. Configure a variável de ambiente `MSSQL_SA_PASSWORD` segura.
2. Inicialize o serviço de banco de dados:

    ```bash
    docker-compose up -d
    ```

3. Valide a conexão na porta `1433` (Usuário: `sa`).

#### 1.2. Pipeline ETL (Python)

1. Crie e ative um ambiente virtual Python (`venv`).
2. Instale as dependências do projeto:

    ```bash
    pip install pandas numpy sqlalchemy pyodbc
    ```

3. Execute os scripts de carga localizados em `src/etl/`.

#### 1.3. Visualização (Power BI)

1. Abra o arquivo `.pbix` no Power BI Desktop.
2. Configure a fonte de dados para `localhost,1433`.

### Strings de Conexão (Desenvolvimento Local)

**Python (SQLAlchemy):**

```python
engine = create_engine(
    "mssql+pyodbc://sa:<password>@localhost:1433/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)
```

---

## 2. Fase 2: Expansão Enterprise (Roadmap Azure)

A próxima fase do projeto migrará a carga de trabalho para uma arquitetura Cloud-Native no Microsoft Azure. Esta seção descreve os componentes planejados e pré-requisitos futuros.

> **Nota:** Os componentes abaixo fazem parte do roadmap de expansão e serão provisionados via Infraestrutura como Código (IaC).

### Arquitetura Alvo

* **Ingestão IoT:** Azure IoT Hub (Substituindo ingestão passiva).
* **Processamento:** Azure Databricks (Substituindo scripts locais Pandas).
* **Armazenamento:** Azure Data Lake Gen2 (Camadas Bronze/Silver/Gold).
* **Serving:** Azure SQL Database (Camada de serviço para BI).

### Pré-requisitos Futuros

* Subscrição Microsoft Azure ativa.
* Azure CLI e Terraform instalados.
* Acesso ao Azure Entra ID (antigo Active Directory) para gestão de identidades.

### Provisionamento (Planejado)

A infraestrutura será implantada de forma automatizada:

1. Autenticação via CLI: `az login`.
2. Execução do plano Terraform: `terraform apply` (Diretório `infra/`).

---

*Para dúvidas sobre a modelagem de dados, consulte [DATA_DICTIONARY.md](DATA_DICTIONARY.md).*
