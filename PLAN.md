# Thabo's Corner Store - Project Plan

## Computational Thinking

## Project Overview

Thabo owns a small corner store and keeps track of his products and sales using spreadsheets. Over time, the data has become difficult to work with because there are missing values, duplicates, and inconsistent formats. This makes it harder to get accurate information about sales performance and stock levels.

The purpose of this project is to develop a Python-based system that cleans and organises the data, stores it in an SQLite database, analyses sales information, and creates visual reports. The system will also include basic password protection to ensure that only authorised users can access the reports. By improving the quality and organisation of the data, Thabo will be able to make better-informed business decisions.

---

### 1. Decompose the Problem

To make the project easier to manage, I have divided it into a number of smaller tasks:

1. Clean the raw sales and product data.
2. Store the cleaned data in an SQLite database.
3. Analyse the data to identify useful trends and insights.
4. Create charts and graphs to present the results.
5. Add a password system to protect access to reports.

Breaking the work into smaller sections will make it easier to develop, test, and troubleshoot each part of the system.

### 2. Identify Patterns

While reviewing the datasets, several common data quality issues were identified.

**Products data:**

- Missing product names
- Missing prices
- Different capitalisation styles in categories
- Duplicate product records

**Sales data:**

- Dates stored in different formats
- Missing dates
- Missing quantities
- Missing payment methods
- Product IDs that do not match the products dataset
- Duplicate sales transactions

Instead of fixing these issues individually, the system will apply consistent cleaning rules to all records with the same type of problem.

### 3. Abstraction

Only the information that is relevant to the project's goals will be used during analysis. This includes:

- Product information
- Product prices
- Quantities sold
- Sale dates
- Payment methods
- Customer types

Any unnecessary information will be ignored so that the analysis remains focused and efficient. The original CSV files will not be changed, and any cleaning decisions made during the process will be clearly documented. For example, if dates appear in different formats, the method used to standardise them will be recorded.

### 4. Algorithm Design

The system will follow the steps below:

1. Load the `products.csv` and `sales.csv` files.
2. Clean and validate the products dataset.
3. Clean and validate the sales dataset.
4. Create the SQLite database and the required tables.
5. Insert the cleaned data into the database.
6. Run SQL queries to generate useful business information.
7. Calculate sales statistics and identify trends.
8. Create charts and graphs to display the findings.
9. Implement password protection for report access.
10. Test the system and document the final solution in the README file.

---

## Planned Module Order

### 1. `data_cleaning.py`

This module will be developed first because the rest of the project depends on having accurate and reliable data.

### 2. `database.py`

Once the data has been cleaned, it will be stored in an SQLite database using appropriate primary and foreign key relationships.

### 3. `analysis.py`

This module will perform calculations and generate business insights such as:

- Total records processed
- Sales trends
- Low-stock alerts
- Transaction summaries
- Monthly sales performance

### 4. `visualize.py`

The results from the analysis stage will be presented using charts and graphs, making the information easier to understand.

### 5. `security.py`

This module will add a simple login system that uses hashed passwords to protect access to reports and analysis results.

---

## Reason for the Module Order

The modules are arranged in the order that they depend on one another. The data must first be cleaned before it can be stored in the database. Once the database has been created and populated, the data can be analysed. The analysis results are then used to generate charts and reports. Security features are added afterwards to protect access to the completed system.
