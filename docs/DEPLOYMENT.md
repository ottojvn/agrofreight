# Deployment Guide

## Overview
AgroFreight Intelligence uses a hybrid development workflow to accommodate containerized Data Engineering and Windows-based Business Intelligence. This guide covers environment setup and migration procedures.

## System Architecture

### Data Engineering Layer
| Component | Technology |
|-----------|------------|
| Data Source | Local CSV files generated via Python |
| Processing Layer | Python scripts |
| Storage Layer | SQL Server 2022 (Docker Container) |
| Management | SQL Client (e.g., SSMS, Azure Data Studio, DBeaver) |

### Visualization Layer
| Component | Technology |
|-----------|------------|
| Storage Layer | SQL Server Developer Edition (Windows) |
| Presentation Layer | Power BI Desktop |

## Environment Setup

### Container Environment Setup

#### 1. Docker Installation
Ensure Docker is running on your system. Verify with:
```bash
docker --version
docker info
```

#### 2. Start SQL Server Container
Use the provided `docker-compose.yml`:
```bash
# Create .env file with password
echo "MSSQL_SA_PASSWORD=YourStrongPassword123!" > .env

# Start the container
docker-compose up -d
```

#### 3. ODBC Driver
Install `msodbcsql17` or `msodbcsql18`. See [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) for platform-specific installation instructions.

#### 4. Python Dependencies
```bash
python -m venv venv

# Activate virtual environment
# On Unix/macOS: source venv/bin/activate
# On Windows: venv\Scripts\activate

pip install pandas numpy sqlalchemy pyodbc
```

#### 5. Database Authentication
Use SQL Authentication for Docker:
- **User:** `sa`
- **Password:** Strong password defined in `.env` file
- **Port:** `1433`

### Visualization Environment Setup

#### 1. SQL Server Developer Edition
Install SQL Server Developer Edition locally.

#### 2. Power BI Desktop
Install the latest version from Microsoft Store or official download.

#### 3. SQL Client
A SQL client (e.g., SSMS, Azure Data Studio, DBeaver) is recommended for database backup/restore operations.

## Connection Strings

### Docker (Container Environment)
```
Server=localhost,1433;Database=AgroFreight;User Id=sa;Password=<your_password>;TrustServerCertificate=true;
```

### Local (Visualization Environment)
```
Server=localhost;Database=AgroFreight;Trusted_Connection=True;
```

### Python SQLAlchemy Format
```python
# Docker (Container Environment)
engine = create_engine(
    "mssql+pyodbc://sa:<password>@localhost:1433/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

# Local (Visualization Environment with Trusted Connection)
engine = create_engine(
    "mssql+pyodbc://localhost/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Trusted_Connection=yes"
)
```

## Migration Strategy (The Bridge)

To transition data from the Container Environment to the Visualization Environment for Power BI integration:

### Step 1: Create Database Backup
Execute in your SQL client (connected to Docker):
```sql
BACKUP DATABASE AgroFreight
TO DISK = '/var/opt/mssql/backup/AgroFreight.bak'
WITH FORMAT, INIT, NAME = 'AgroFreight Full Backup';
```

### Step 2: Copy Backup File
Copy the `.bak` file from the Docker container to the visualization environment:
```bash
docker cp agrofreight_sql:/var/opt/mssql/backup/AgroFreight.bak ./AgroFreight.bak
```

### Step 3: Restore Database
Using a SQL client:
1. Right-click **Databases** → **Restore Database**
2. Select **Device** → Browse to the `.bak` file
3. Verify file paths and click **OK**

### Step 4: Connect Power BI
1. Open Power BI Desktop
2. **Get Data** → **SQL Server**
3. Server: `localhost`
4. Database: `AgroFreight`
5. Use Windows Authentication

## Troubleshooting

### Docker Connection Issues
- Verify container is running: `docker ps`
- Check logs: `docker logs agrofreight_sql`
- Ensure port 1433 is not blocked

### ODBC Driver Errors
- Verify driver installation: `odbcinst -q -d`
- Use `TrustServerCertificate=yes` for self-signed certificates

### Power BI Refresh Failures
- Verify SQL Server service is running on Windows
- Check Windows Firewall settings
- Ensure correct authentication mode
