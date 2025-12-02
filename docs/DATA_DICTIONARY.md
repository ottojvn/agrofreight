# Data Dictionary

## Overview
This document defines the database schema and ETL rules for the AgroFreight Intelligence data warehouse. The database uses a **Star Schema** design pattern with fact and dimension tables.

## Data Model (Star Schema)

### Fact Table

#### Fact_Freight
Transactional records containing freight movement data.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| FreightID | INTEGER | PRIMARY KEY, IDENTITY | Unique identifier for each freight record |
| DateID | INTEGER | FOREIGN KEY → Dim_Date | Reference to date dimension |
| RouteID | INTEGER | FOREIGN KEY → Dim_Route | Reference to route dimension |
| VehicleID | INTEGER | FOREIGN KEY → Dim_Vehicle | Reference to vehicle dimension |
| FreightValue | DECIMAL(10,2) | NOT NULL | Total freight cost in BRL |
| DieselPrice | DECIMAL(10,2) | NOT NULL | Diesel price per liter at time of transport |
| WeightTon | DECIMAL(10,2) | NOT NULL | Total weight transported in tons |

### Dimension Tables

#### Dim_Date
Calendar dimension for time-based analysis.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| DateID | INTEGER | PRIMARY KEY, IDENTITY | Unique identifier |
| RecordDate | DATE | NOT NULL | Full date value |
| Month | INTEGER | NOT NULL | Month number (1-12) |
| Year | INTEGER | NOT NULL | Year (e.g., 2024) |
| IsHarvestSeason | BIT | NOT NULL | Flag indicating harvest period (March-May) |

#### Dim_Route
Route information for geographic analysis.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| RouteID | INTEGER | PRIMARY KEY, IDENTITY | Unique identifier |
| Origin | VARCHAR(100) | NOT NULL | Origin city/location |
| Destination | VARCHAR(100) | NOT NULL | Destination city/location |
| DistanceKM | INTEGER | NOT NULL | Route distance in kilometers |

#### Dim_Vehicle
Vehicle information for fleet analysis.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| VehicleID | INTEGER | PRIMARY KEY, IDENTITY | Unique identifier |
| PlateNumber | VARCHAR(20) | NOT NULL | Vehicle license plate |
| VehicleType | VARCHAR(50) | NOT NULL | Type of vehicle (e.g., Truck, Semi-trailer) |
| Capacity | INTEGER | NOT NULL | Maximum load capacity in tons |

### Support Tables

#### Log_Errors
Records that fail the Sanity Check validation are logged here.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| ErrorID | INTEGER | PRIMARY KEY, IDENTITY | Unique identifier |
| RawData | NVARCHAR(MAX) | NOT NULL | Original record data in JSON format |
| ErrorMessage | VARCHAR(255) | NOT NULL | Description of validation failure |
| ErrorDate | DATE | NOT NULL, DEFAULT GETDATE() | Date when error was logged |

## ETL Rules

### Data Validation (Logistics Sanity Check)
All incoming records must pass the following validation rules before insertion into the fact table:

#### Rule 1: Maximum Speed Feasibility
```
average_speed = Distance (KM) / (Arrival Time - Departure Time in hours)
```
- **REJECT** if `average_speed > 90 KM/h` (heavy trucks cannot sustain this safely)
- **REJECT** if `Arrival Time <= Departure Time` (invalid time sequence)

#### Rule 2: Cost Consistency
- **REJECT** if `Freight Value <= 0` (freight value must be positive)

### Data Type Requirements
| Source Field | Required Format | Transformation Notes |
|--------------|-----------------|---------------------|
| Date fields | ISO 8601 (YYYY-MM-DD) | Parse to DATE type |
| Numeric values | Decimal with period separator | Use DECIMAL(10,2) for currency |
| Text fields | UTF-8 encoded | Trim whitespace, validate length |

### Error Handling
1. Records failing validation are logged to `Log_Errors` with the full raw data
2. Valid records are inserted into appropriate dimension and fact tables
3. ETL process generates summary report with:
   - Total records processed
   - Records successfully loaded
   - Records rejected (with breakdown by error type)

## Code Standards
- **Nomenclature:** `snake_case` for Python variables/functions; `PascalCase` for Classes
- **Credentials:** NEVER hardcode passwords. Use environment variables or a separate `secrets.py` (listed in `.gitignore`)
- **Modularity:** Connection strings must be isolated to facilitate switching between Docker and Windows environments
