# Project Backlog: AgroFreight Intelligence

## Sprint 1: Infrastructure & Data Modeling (Environment: Arch Linux)
**Goal:** Establish the containerized database environment and define the structural schema.
- [ ] **Task 1.1:** Linux Environment Setup. Install Docker for SQL Server 2022. Install Visual Studio Code and the MSSQL Extension to replace Azure Data Studio.
- [ ] **Task 1.2:** Conceptual Modeling. Create the Entity-Relationship Diagram (ERD) defining Facts and Dimensions based on the Star Schema.
- [ ] **Task 1.3:** Database Implementation. Write and execute T-SQL DDL scripts within Visual Studio Code (connected to the Docker instance) to create the database, tables, and constraints.

## Sprint 2: Data Engineering & ETL Pipeline (Environment: Arch Linux)
**Goal:** Develop the Python mechanism to generate, validate, and load data into the containerized database.
- [ ] **Task 2.1:** Python Project Setup. Initialize the virtual environment and install Linux-specific dependencies (`pandas`, `sqlalchemy`, `pyodbc`, `msodbcsql18`).
- [ ] **Task 2.2:** Synthetic Data Generation. Create a script to generate realistic CSV files containing valid and invalid logistics data (approx. 5,000 records).
- [ ] **Task 2.3:** Transformation Logic ("Sanity Check"). Implement the algorithm to calculate average speed and filter out physically impossible trips.
- [ ] **Task 2.4:** Database Loading. Implement the connection string using SQL Authentication (`sa` user) and bulk insert logic to move data from Pandas to the SQL Server Docker instance.

## Sprint 3: Migration & Business Intelligence (Environment: Windows)
**Goal:** Migrate the data to the Windows environment and build the visualization layer.
- [ ] **Task 3.1:** Database Migration (The Bridge). Execute a T-SQL `BACKUP DATABASE` command via VS Code in Linux to generate a `.bak` file. Transfer the file to Windows and restore it using SSMS (SQL Server Management Studio).
- [ ] **Task 3.2:** Connectivity. Configure Power BI Desktop to connect to the local Windows SQL Server instance.
- [ ] **Task 3.3:** Measure Creation (DAX). Implement business formulas: Cost per Ton, Cost per KM, and Freight Price MoM variation.
- [ ] **Task 3.4:** Dashboard Construction. Build the interface containing Key Performance Indicators (KPIs), Geospatial maps, and Trend lines.

## Sprint 4: Documentation & Polish
**Goal:** Finalize the project for presentation to potential employers.
- [ ] **Task 4.1:** Code Refactoring. Review Python scripts for readability and ensure connection strings are modular (handling both Docker and Local environments).
- [ ] **Task 4.2:** Documentation. Write the main `README.md` highlighting the hybrid architecture and the use of modern tooling (VS Code + MSSQL).
- [ ] **Task 4.3:** Validation. Perform a full end-to-end test (Generate Data -> Load to Docker -> Migrate -> Refresh Power BI) to ensure the narrative holds up.
