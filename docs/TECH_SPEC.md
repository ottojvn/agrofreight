# Technical Specification

## 1. System Architecture
The solution utilizes a Hybrid Development Workflow to accommodate Linux-based Data Engineering and Windows-based Business Intelligence.

### Phase 1: Data Engineering (Environment: Arch Linux)
1.  **Data Source:** Local CSV files generated via Python.
2.  **Processing Layer:** Python scripts running on Arch Linux.
3.  **Storage Layer:** SQL Server 2022 running inside a Docker Container.
4.  **Management:** Visual Studio Code (Linux) with MSSQL Extension for database administration and query execution.

### Phase 2: Visualization (Environment: Windows)
1.  **Migration:** Database migration via Backup (`.bak`) and Restore.
2.  **Storage Layer:** SQL Server Developer Edition (Native Windows).
3.  **Presentation Layer:** Power BI Desktop connected to the local Windows instance.

## 2. Technology Stack

### 2.1. Programming Language & Libraries (Linux)
-   **Python 3.10+**
-   **Pandas:** For data manipulation and tabular operations.
-   **NumPy:** For numerical calculations and vectorized validation logic.
-   **SQLAlchemy:** ORM/Core for database abstraction.
-   **PyODBC:** ODBC Bridge. requires `msodbcsql18` (AUR package).

### 2.2. Database Management
-   **Engine:** Microsoft SQL Server 2022 (Docker Image: `mcr.microsoft.com/mssql/server:2022-latest`).
-   **Client Tools (Linux):**
    -   **Visual Studio Code:** The primary IDE.
    -   **MSSQL Extension (VS Code):** Required for connecting to the Docker instance, managing schemas, and executing T-SQL queries directly from the editor.
-   **Client Tools (Windows):**
    -   **SSMS (SQL Server Management Studio):** Recommended for the specific task of restoring the database backup (`.bak`) on Windows.

### 2.3. Visualization
-   **Microsoft Power BI Desktop:** For report creation (Windows only).

## 3. Data Model Design (Star Schema)
The database structure remains consistent across both environments.

### Fact Table
-   **Fact_Freight:** Transactional records.
    -   *Columns:* ID, DateID, RouteID, VehicleID, FreightValue, DieselPrice, WeightTon.

### Dimension Tables
-   **Dim_Route:** Origin, Destination, DistanceKM.
-   **Dim_Vehicle:** PlateNumber, VehicleType, Capacity.
-   **Dim_Date:** Date, Month, Year, IsHarvestSeason.

### Support Tables
-   **Log_Errors:** Rejected records failing the Sanity Check.

## 4. Environment Configuration

### 4.1. Linux (Arch) Requirements
-   **Docker:** Service must be active (`systemctl start docker`).
-   **ODBC Driver:** Install `msodbcsql17` or `msodbcsql18` via AUR.
-   **VS Code Extensions:**
    -   `ms-mssql.mssql` (SQL Server).
    -   `ms-python.python` (Python).
-   **Authentication:** SQL Authentication required for Docker.
    -   User: `sa`
    -   Password: Strong password defined in `docker run` command.

### 4.2. Windows Requirements
-   **SQL Server Developer Edition:** Local service.
-   **Power BI Desktop:** Latest version.

## 5. Migration Strategy (The Bridge)
To transition from Phase 1 to Phase 2:
1.  **Backup:** Use the MSSQL Extension in VS Code (or T-SQL command) to generate a full database backup (`.bak` file) from the Docker container.
2.  **Transfer:** Move the `.bak` file to a Windows-accessible partition.
3.  **Restore:** Use SSMS on Windows to restore the database from the `.bak` file.
4.  **Reconnection:** Point Power BI to `localhost` (Windows) instead of the Docker IP.

## 6. Code Standards
-   **Nomenclature:** `snake_case` for Python variables/functions; `PascalCase` for Classes.
-   **Credentials:** NEVER hardcode passwords. Use environment variables or a separate `secrets.py` (listed in `.gitignore`).
-   **Modularity:** Connection strings must be isolated to facilitate switching between the Docker driver and the Windows driver.
