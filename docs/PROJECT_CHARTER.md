# Project Charter: AgroFreight Intelligence

## 1. Executive Summary
This project aims to develop a Business Intelligence solution for "AgroLog" (a fictitious logistics operator in the Brazilian Midwest). The system will monitor freight price volatility during the harvest season ("Safrinha"), correlating transport costs with diesel price fluctuations to identify routes with eroding profit margins.

## 2. Business Problem
AgroLog negotiates fixed-price transport contracts with grain producers in January. However, during the harvest (March-May), external factors such as diesel price hikes and high demand for trucks increase the cost of "spot" freight.
Currently, the operations team tracks these costs using decentralized spreadsheets, leading to delayed decision-making and financial losses.

## 3. Project Objectives
1.  **Centralization:** Consolidate data from freight history and fuel costs into a single SQL Server Data Warehouse.
2.  **Data Integrity:** Implement a "Logistics Sanity Check" algorithm to filter out erroneous or fraudulent data inputs before storage.
3.  **Decision Support:** Provide a Power BI Dashboard that allows logistics managers to visualize Cost per Ton/KM and identify inefficient routes.

## 4. Scope
### In Scope
-   **ETL Pipeline:** A Python script to extract data from CSV files, transform/clean it, and load it into the database.
-   **Database:** Design and implementation of a Star Schema in SQL Server.
-   **Validation Logic:** Implementation of strict business rules to validate trip feasibility.
-   **Visualization:** Interactive Power BI dashboard showing key metrics.

### Out of Scope
-   Real-time data streaming.
-   Machine Learning for price prediction (focus is on descriptive analytics).
-   Web interface for data entry.

## 5. Critical Business Rules (The "Logistics Sanity Check")
To ensure data quality, the ETL process must apply the following validation logic. Records failing these checks must be rejected and logged separately:

1.  **Maximum Speed Feasibility:**
    -   Calculate average speed: `Distance (KM) / (Arrival Time - Departure Time)`.
    -   Rule: If average speed > 90 KM/h, mark as invalid (heavy trucks cannot sustain this average safely on local roads).
    -   Rule: If `Arrival Time` <= `Departure Time`, mark as invalid.

2.  **Cost Consistency:**
    -   Rule: Freight Value cannot be negative or zero.

## 6. Key Performance Indicators (KPIs)
-   **Average Freight Cost per Ton:** Evaluated by route and month.
-   **Cost per Kilometer:** To compare efficiency across different routes.
-   **Rejection Rate:** Percentage of records rejected by the Sanity Check.
