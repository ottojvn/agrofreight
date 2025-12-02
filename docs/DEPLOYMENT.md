# Deployment Guide

## Overview
AgroFreight Intelligence uses a hybrid development workflow to accommodate Linux-based Data Engineering and Windows-based Business Intelligence. This guide covers environment setup and migration procedures.

## System Architecture

### Phase 1: Data Engineering (Linux Environment)
| Component | Technology |
|-----------|------------|
| Data Source | Local CSV files generated via Python |
| Processing Layer | Python scripts |
| Storage Layer | SQL Server 2022 (Docker Container) |
| Management | VS Code with MSSQL Extension or Azure Data Studio |

### Phase 2: Visualization (Windows Environment)
| Component | Technology |
|-----------|------------|
| Storage Layer | SQL Server Developer Edition (Native Windows) |
| Presentation Layer | Power BI Desktop |

## Environment Setup

### Linux Requirements

#### 1. Docker Installation
Ensure Docker service is active:
```bash
systemctl start docker
systemctl enable docker
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
Install `msodbcsql17` or `msodbcsql18` for your distribution:
- **Ubuntu/Debian:** Follow Microsoft's official APT repository setup
- **Arch Linux:** Install via AUR

#### 4. VS Code Extensions
Install the following extensions:
- `ms-mssql.mssql` (SQL Server)
- `ms-python.python` (Python)

#### 5. Python Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install pandas numpy sqlalchemy pyodbc
```

#### 6. Database Authentication
Use SQL Authentication for Docker:
- **User:** `sa`
- **Password:** Strong password defined in `.env` file
- **Port:** `1433`

### Windows Requirements

#### 1. SQL Server Developer Edition
Install SQL Server Developer Edition locally.

#### 2. Power BI Desktop
Install the latest version from Microsoft Store or official download.

#### 3. SQL Server Management Studio (SSMS)
Recommended for database backup/restore operations.

## Connection Strings

### Docker (Linux)
```
Server=localhost,1433;Database=AgroFreight;User Id=sa;Password=<your_password>;TrustServerCertificate=true;
```

### Local (Windows)
```
Server=localhost;Database=AgroFreight;Trusted_Connection=True;
```

### Python SQLAlchemy Format
```python
# Docker (Linux)
engine = create_engine(
    "mssql+pyodbc://sa:<password>@localhost:1433/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

# Windows (Trusted Connection)
engine = create_engine(
    "mssql+pyodbc://localhost/AgroFreight"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Trusted_Connection=yes"
)
```

## Migration Strategy (The Bridge)

To transition from Phase 1 (Linux/Docker) to Phase 2 (Windows/Power BI):

### Step 1: Create Database Backup
Execute in VS Code or Azure Data Studio (connected to Docker):
```sql
BACKUP DATABASE AgroFreight
TO DISK = '/var/opt/mssql/backup/AgroFreight.bak'
WITH FORMAT, INIT, NAME = 'AgroFreight Full Backup';
```

### Step 2: Copy Backup File
Copy the `.bak` file from the Docker container to a Windows-accessible location:
```bash
docker cp agrofreight_sql:/var/opt/mssql/backup/AgroFreight.bak ./AgroFreight.bak
```

### Step 3: Restore on Windows
Using SSMS on Windows:
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
