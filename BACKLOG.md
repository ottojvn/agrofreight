# Project Backlog: AgroFreight Intelligence

## Sprint 1: Infrastructure & Data Modeling (Environment: Arch Linux)
**Goal:** Establish the containerized database environment and define the structural schema.
- [ ] **Task 1.1:** Linux Environment Setup. Install and configure Docker for SQL Server 2022 and Azure Data Studio (via AUR/Flatpak).
- [ ] **Task 1.2:** Conceptual Modeling. Create the Entity-Relationship Diagram (ERD) defining Facts and Dimensions based on the Star Schema.
- [ ] **Task 1.3:** Database Implementation. Write and execute T-SQL DDL scripts in Azure Data Studio to create the database, tables, and constraints within the Docker container.

## Sprint 2: Data Engineering & ETL Pipeline (Environment: Arch Linux)
**Goal:** Develop the Python mechanism to generate, validate, and load data into the containerized database.
- [ ] **Task 2.1:** Python Project Setup. Initialize the virtual environment and install Linux-specific dependencies (`pandas`, `sqlalchemy`, `pyodbc`, `msodbcsql18`).
- [ ] **Task 2.2:** Synthetic Data Generation. Create a script to generate realistic CSV files containing valid and invalid logistics data (approx. 5,000 records).
- [ ] **Task 2.3:** Transformation Logic ("Sanity Check"). Implement the algorithm to calculate average speed and filter out physically impossible trips.
- [ ] **Task 2.4:** Database Loading. Implement the connection string using SQL Authentication (`sa` user) and bulk insert logic to move data from Pandas to the SQL Server Docker instance.

## Sprint 3: Migration & Business Intelligence (Environment: Windows)
**Goal:** Migrate the data to the Windows environment and build the visualization layer.
- [ ] **Task 3.1:** Database Migration (The Bridge). Generate a `.bak` backup file from the Linux Docker container, transfer it to the Windows partition, and restore it on a local SQL Server Developer Edition instance.
- [ ] **Task 3.2:** Connectivity. Configure Power BI Desktop to connect to the local Windows SQL Server instance.
- [ ] **Task 3.3:** Measure Creation (DAX). Implement business formulas: Cost per Ton, Cost per KM, and Freight Price MoM variation.
- [ ] **Task 3.4:** Dashboard Construction. Build the interface containing Key Performance Indicators (KPIs), Geospatial maps, and Trend lines.

## Sprint 4: Documentation & Polish
**Goal:** Finalize the project for presentation to potential employers.
- [ ] **Task 4.1:** Code Refactoring. Review Python scripts for readability and ensure connection strings are modular (handling both Docker and Local environments).
- [ ] **Task 4.2:** Documentation. Write the main `README.md` highlighting the hybrid architecture (Linux Backend / Windows Frontend) as a technical differentiator.
- [ ] **Task 4.3:** Validation. Perform a full end-to-end test (Generate Data -> Load to Docker -> Migrate -> Refresh Power BI) to ensure the narrative holds up.
