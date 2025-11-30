# Technical Specification

## 1. System Architecture
The solution follows a standard ETL (Extract, Transform, Load) architecture designed for a local development environment.

1.  **Data Source:** Local CSV files simulating exports from legacy ERP systems.
2.  **Processing Layer (Python):** Script responsible for reading files, applying business rules (Sanity Check), and handling data types.
3.  **Storage Layer (SQL Server):** Relational database optimized for analytics using a Star Schema model.
4.  **Presentation Layer (Power BI):** Interactive dashboard connected directly to the database.

## 2. Technology Stack

### 2.1. Programming Language & Libraries
-   **Python 3.10+**
-   **Pandas:** For data manipulation and tabular operations.
-   **NumPy:** For numerical calculations (specifically for vectorized operations in validation logic).
-   **SQLAlchemy:** For Object-Relational Mapping and database connection abstraction.
-   **PyODBC:** The underlying driver to allow communication between Python and SQL Server.

### 2.2. Database Management
-   **Microsoft SQL Server 2022:** Developer or Express Edition.
-   **SSMS (SQL Server Management Studio):** For database administration and query testing.

### 2.3. Visualization
-   **Microsoft Power BI Desktop:** For report creation.

## 3. Data Model Design (Star Schema)
The database will be structured to separate analyzing entities (Dimensions) from metrics (Facts).

### Fact Table
-   **Fact_Freight:** Contains transactional data.
    -   *Columns:* ID, DateID, RouteID, VehicleID, FreightValue, DieselPrice, WeightTon.

### Dimension Tables
-   **Dim_Route:**
    -   *Columns:* RouteID, OriginCity, DestinationCity, DistanceKM.
-   **Dim_Vehicle:**
    -   *Columns:* VehicleID, PlateNumber, VehicleType (e.g., Bitrem, Vanderleia).
-   **Dim_Date:**
    -   *Columns:* DateID, Date, Month, Year, Quarter, IsHarvestSeason (Boolean).

### Support Tables
-   **Log_Errors:** Stores records rejected during the ETL process for audit purposes.

## 4. Development Environment Requirements
To execute this project, the following environment variables and configurations are required:

1.  **ODBC Driver:** "ODBC Driver 17 (or 18) for SQL Server" must be installed.
2.  **Authentication:** Windows Authentication (Trusted Connection) is recommended for local development to avoid complex user management.

## 5. Code Standards
-   **Nomenclature:** Variables and functions must use `snake_case` (e.g., `calculate_freight_cost`). Classes must use `PascalCase`.
-   **Comments:** All complex logic (especially the Sanity Check) must be documented within the code.
-   **Modularity:** Database connection logic must be separated from business logic.
