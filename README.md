# AgroFreight Intelligence

## Project Overview
AgroFreight Intelligence is an end-to-end Business Intelligence solution developed to monitor freight cost volatility in the agribusiness sector. The system centralizes historical transport data and fuel costs to identify routes with eroding profit margins during the harvest season ("Safrinha").

This project was created for "AgroLog" (a fictitious logistics operator in the Brazilian Midwest) to solve the challenge of tracking freight costs that are currently managed through decentralized spreadsheets, leading to delayed decision-making and financial losses.

## Project Scope

### In Scope
- **ETL Pipeline:** Python scripts to extract data from CSV files, transform/clean it, and load it into the database.
- **Database:** Design and implementation of a Star Schema in SQL Server.
- **Validation Logic:** Implementation of strict business rules to validate trip feasibility (the "Logistics Sanity Check").
- **Visualization:** Interactive Power BI Dashboard showing key metrics.

### Out of Scope
- Real-time data streaming.
- Machine Learning for price prediction (focus is on descriptive analytics).
- Web interface for data entry.

## Key Performance Indicators (KPIs)
| KPI | Description |
|-----|-------------|
| **Average Freight Cost per Ton** | Evaluated by route and month |
| **Cost per Kilometer** | To compare efficiency across different routes |
| **Rejection Rate** | Percentage of records rejected by the Sanity Check |

## Critical Business Rules (Logistics Sanity Check)
To ensure data quality, the ETL process applies the following validation logic. Records failing these checks are rejected and logged separately:

1. **Maximum Speed Feasibility:**
   - Calculate average speed: `Distance (KM) / (Arrival Time - Departure Time)`
   - Rule: If average speed > 90 KM/h, mark as invalid (heavy trucks cannot sustain this average safely on local roads)
   - Rule: If `Arrival Time` <= `Departure Time`, mark as invalid

2. **Cost Consistency:**
   - Rule: Freight Value cannot be negative or zero

## Environment Specifications
| Component | Technology |
|-----------|------------|
| **Source Database** | SQL Server 2022 (Docker) |
| **Visualization Tool** | Power BI Desktop (Windows) |
| **ETL Language** | Python 3.10+ (Pandas, NumPy, SQLAlchemy, PyODBC) |
| **Database Management** | SQL Client (e.g., SSMS, Azure Data Studio, DBeaver) |
| **Version Control** | Git & GitHub |

## Repository Structure
```
├── docs/                 # Data dictionary, deployment instructions
│   ├── DATA_DICTIONARY.md    # Schema & ETL rules
│   └── DEPLOYMENT.md         # Environment setup & migration guide
├── sql/                  # DDL scripts for database tables and procedures
├── src/                  # ETL scripts and data validation code (future)
├── BACKLOG.md            # Sprint planning and task tracking
└── docker-compose.yml    # SQL Server container configuration
```

## Project Status
Currently in development (Sprint 1), with focus on environment configuration and data modeling in SQL Server.
