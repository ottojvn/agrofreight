# Guia de Implantação

Instruções para configuração do ambiente de desenvolvimento híbrido (Engenharia e Visualização).

## Pré-requisitos
*   **Container Engine:** Docker e Docker Compose.
*   **Linguagem:** Python 3.10+.
*   **Banco de Dados:** SQL Server 2022 (Imagem Container).
*   **Visualização:** Power BI Desktop (Requer ambiente Windows).
*   **Drivers:** ODBC Driver 17 ou 18 para SQL Server.

## Configuração do Ambiente

### 1. Banco de Dados (Container)
O projeto utiliza um container SQL Server para a camada de engenharia.

1.  Defina a variável de ambiente `MSSQL_SA_PASSWORD` (via arquivo `.env` ou exportação no shell).
2.  Execute o serviço via Docker Compose:
    ```bash
    docker-compose up -d
    ```
3.  Conecte-se à porta `1433` utilizando um cliente SQL de sua preferência (autenticação SQL, usuário `sa`).

### 2. Ambiente Python (ETL)
1.  Crie e ative um ambiente virtual Python.
2.  Instale as dependências listadas (pandas, sqlalchemy, pyodbc):
    ```bash
    pip install pandas numpy sqlalchemy pyodbc
    ```

### 3. Ambiente de Visualização (Power BI)
Devido a requisitos da ferramenta, esta etapa necessita de ambiente Windows.

1.  Instale o Power BI Desktop.
2.  Garanta acesso a uma instância SQL Server compatível para carga de dados (seja via conexão direta ao Docker ou restauração local).

## Strings de Conexão

Utilize as strings abaixo conforme o driver ODBC instalado no seu sistema:

**Python (SQLAlchemy):**
```python
# Exemplo para autenticação SQL (Container)
engine = create_engine(
    "mssql+pyodbc://sa:<password>@localhost:1433/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)
```
