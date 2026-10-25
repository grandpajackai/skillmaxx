# Oracle AI Data Platform Workbench Samples

This repository contains a curated collection of sample notebooks demonstrating how to build data pipelines, run machine learning workloads, and integrate AI capabilities using **Oracle AI Data Platform (AIDP) Workbench** — a unified, governed workspace for data engineering, ML, and AI development powered by Apache Spark.

## What is Oracle AI Data Platform Workbench?

Oracle AI Data Platform Workbench is a unified, governed workspace for building, managing, and deploying AI and data-driven solutions. It brings together notebooks, agent development, orchestration, and catalog management in a single collaborative platform — empowering teams to explore data, fine-tune models, and operationalize AI with trust and speed.

[Learn more about AIDP Workbench →](https://www.oracle.com/ai-data-platform/workbench/)

---

## Repository Structure

```
oracle-aidp-samples/
├── getting-started/          # Foundational notebooks for new users
│   ├── Delta_Lake/           # Delta Lake feature walkthroughs
│   └── migration/            # Migrating workloads to AIDP
├── data-engineering/
│   ├── ingestion/            # Connectors and data loading patterns
│   │   └── landing-zone-auto-ingestion/
│   ├── lineage/              # Reading and visualizing AIDP data lineage
│   └── transformation/       # Pipeline architectures and table formats
│       ├── delta-clone-metadata/
│       ├── liquid-clustering/
│       ├── medallion-lake/
│       ├── scd/
│       └── streaming/
├── ai/
│   ├── agent-hub/            # Agent Hub code-first agent samples
│   │   └── agent-samples/
│   ├── agent-flows/          # Agent orchestration and scheduling
│   ├── ml-datascience/       # ML, LLM, and AI service integrations
│   └── skills/               # Agent Skills (SKILL.md packages) by product domain
│       └── analytics/        # Oracle Analytics skills
└── shared-utils/             # Reusable utilities and data generators
```

---

## Sample Catalog

### Getting Started

Foundational examples to help you get up and running on AIDP Workbench.

| Notebook | Description |
|---|---|
| [Access ALH Data](getting-started/Access_ALH_Data.ipynb) | Write and query data in Oracle Autonomous AI Lakehouse (ALH) using PySpark `insertInto` and SQL `INSERT` statements with external catalogs. |
| [Access Object Storage Data](getting-started/Access_Object_Storage_Data.ipynb) | Read and write data from OCI Object Storage using direct access, external volumes, and external tables. |
| [Analyse Data Using PySpark](getting-started/Analyse_Data_Using_PySpark.ipynb) | PySpark fundamentals: catalog and schema setup, table creation, data insertion, schema exploration, and matplotlib visualizations. |
| [Analyse Data Using SQL](getting-started/Analyse_Data_Using_SQL.ipynb) | Core SQL operations on AIDP including DataFrame creation, transformations, aggregations, and simple visualizations. |
| [ALH External Catalog MERGE](getting-started/ALH_ExternalCatalog_Merge.ipynb) | End-to-end MERGE workflow into an ALH table via an AIDP external catalog: insert/update/delete with merge keys and OOS-staging skip optimization. |
| [Native Apache Iceberg Table](getting-started/Native_Iceberg_Table.ipynb) | Create a native Iceberg table in a Standard catalog, then explore schema and partition evolution, MERGE, snapshots, and time travel. |
| [Parameterize Notebooks with Native Widgets](getting-started/Native_Notebook_Widgets.ipynb) | Native notebook widgets (text, dropdown, combobox, multiselect), job and `notebook.run` parameter overrides, and a fail-fast check for job parameters a widget silently ignores. |

The native Iceberg sample uses an existing AIDP Standard catalog. The Hadoop catalog sample under Data Engineering registers a separate Spark catalog on OCI Object Storage. Delta UniForm samples create Delta tables that publish Iceberg-compatible metadata.

#### Delta Lake

| Notebook | Description |
|---|---|
| [Use Delta Lake Table](getting-started/Delta_Lake/Use_Delta_Lake_Table.ipynb) | Comprehensive guide covering Delta table operations: updates, merges, time travel, liquid clustering, and vacuuming. |
| [Delta Change Data Feed](getting-started/Delta_Lake/Delta_Change_Feed.ipynb) | Capture row-level changes (inserts, updates, deletes) from Delta tables for CDC, incremental processing, and streaming pipelines. |
| [Handle Schema Evolution](getting-started/Delta_Lake/Handle_Schema_Evolution.ipynb) | Add and evolve columns in Delta tables without rewriting existing data, leveraging automatic schema evolution. |
| [Delta UniForm Tables](getting-started/Delta_Lake/DeltaUniformTables.ipynb) | Create Delta UniForm tables that automatically synchronize Apache Iceberg metadata for cross-format interoperability. |

#### Migration

| Notebook | Description |
|---|---|
| [Migrate Files from Databricks to AIDP](getting-started/migration/databricks_to_aidp/recursive-files-to-aidp.ipynb) | Recursively export notebooks and files from a Databricks workspace to AIDP using the `databricks-sdk` library. |
| [Download from Git to AIDP](getting-started/migration/git_download_and_extract_to_aidp.ipynb) | Download notebooks and files from a Git repository as a ZIP archive and extract them directly into an AIDP workspace volume. |

---

### Data Engineering — Ingestion

Patterns for connecting to and loading data from a wide range of sources.

| Notebook | Description |
|---|---|
| [Read/Write Oracle Ecosystem Connectors](data-engineering/ingestion/Read_Write_Oracle_Ecosystem_Connectors.ipynb) | Connect to Oracle Database, Oracle Exadata, ALH, and ATP with external catalog support and SQL pushdown. |
| [Read/Write External Ecosystem Connectors](data-engineering/ingestion/Read_Write_External_Ecosystem_Connectors/) | Per-database read/write ingestion notebooks — Apache Hive Metastore, Microsoft SQL Server, Azure SQL, PostgreSQL, MySQL, and IBM Db2 (4.1) — each with SQL pushdown and a connector-options reference. |
| [Read-Only Ingestion Connectors](data-engineering/ingestion/Read_Only_Ingestion_Connectors/) | Use read-only connectors for Google BigQuery, MySQL HeatWave, REST APIs, Oracle Fusion BICC, Apache Kafka, and other sources. |
| [Google BigQuery](data-engineering/ingestion/Read_Only_Ingestion_Connectors/Google_BigQuery.ipynb) | Read BigQuery tables and views using service-account authentication, SQL pushdown, partitioned reads, and external catalogs. |
| [Connect Using Custom JDBC Driver](data-engineering/ingestion/Connect_Using_Custom_JDBC_Driver.ipynb) | Integrate custom JDBC drivers (e.g., SQLite, Snowflake) with Spark for connecting to databases not bundled by default. |
| [Execute Oracle ALH SQL](data-engineering/ingestion/Execute%20Oracle%20ALH%20SQL.ipynb) | Execute SQL statements directly against Oracle ALH using the `oracledb` Python package. |
| [Ingest Data Using YAML](data-engineering/ingestion/Ingest_data_using_yaml/Ingest_data_using_YAML.ipynb) | Config-driven ingestion from cloud storage (CSV, JSON) and JDBC sources with schema validation and data quality checks. |
| [Ingest from Multi-Cloud](data-engineering/ingestion/Ingest_from_Multi_Cloud.ipynb) | Ingest data from Azure Data Lake Storage (ADLS) and Amazon S3 with proper JAR configuration and credential management. |
| [Apache Iceberg with an OCI Hadoop Catalog](data-engineering/ingestion/Ingest_into_iceberg_hadoop_catalog_oci_native.ipynb) | Register a Spark Hadoop catalog on OCI Object Storage, then create, query, and evolve an Iceberg table. |
| [Landing Zone Auto-Ingestion](data-engineering/ingestion/landing-zone-auto-ingestion/README.md) | Turn every folder of Parquet files in an Object Storage landing zone into an external table plus a managed Delta table, and load new files incrementally with two rerunnable workflows - no table list to maintain. |
| [Pipe-Delimited File Ingestion](data-engineering/ingestion/PipeDelimited.ipynb) | Read pipe-delimited (`\|`) files from OCI Object Storage and register them as external tables. |
| [Read Excel Files](data-engineering/ingestion/Read_excel_data/read_excel.ipynb) | Read Excel (`.xlsx`) files using the Spark Excel connector and convert them to Spark DataFrames or CSV. |
| [Streaming from OCI Streaming Service](data-engineering/ingestion/Streaming/StreamingFromOCIStreamingService.ipynb) | Consume messages from OCI Streaming (Kafka-compatible) using Spark Structured Streaming with SASL/OAUTHBearer authentication. |
| [Streaming from Volume Path](data-engineering/ingestion/Streaming/StreamingFromVolumePath.ipynb) | Process CSV files from a workspace volume using one-time micro-batch streaming with `Trigger.Once()`. |

---

### Data Engineering — Lineage

Working with the lineage AIDP records automatically for every notebook and workflow run: which tables fed which, through which job, and how each column was derived.

| Notebook | Description |
|---|---|
| [Visualize AIDP Lineage](data-engineering/lineage/Visualize_AIDP_Lineage.ipynb) | Fetch a table's upstream and downstream lineage through the DataLineage API, draw the table and column graphs inline in the notebook, and hand the lineage to other tools as DataFrames or OpenLineage events. |

---

### Data Engineering — Transformation

Architectural patterns and pipeline templates for data transformation at scale.

#### Medallion Architecture

Implements the Bronze → Silver → Gold lakehouse pattern with data quality checks and aggregations. Industry variants available:

| Notebook | Industry |
|---|---|
| [Education](data-engineering/transformation/medallion-lake/education_medallion_architecture_demo.ipynb) | Education analytics pipeline |
| [Energy](data-engineering/transformation/medallion-lake/energy_medallion_architecture_demo.ipynb) | Energy consumption and reporting |
| [Financial Services](data-engineering/transformation/medallion-lake/financial_services_medallion_architecture_demo.ipynb) | Financial transactions and risk |
| [Healthcare](data-engineering/transformation/medallion-lake/healthcare_medallion_architecture_demo.ipynb) | Patient records and clinical data |
| [Hospitality](data-engineering/transformation/medallion-lake/hospitality_medallion_architecture_demo.ipynb) | Hotel bookings and guest analytics |
| [Insurance](data-engineering/transformation/medallion-lake/insurance_medallion_architecture_demo.ipynb) | Policy and claims processing |
| [Manufacturing](data-engineering/transformation/medallion-lake/manufacturing_medallion_architecture_demo.ipynb) | Production line and quality data |
| [Media](data-engineering/transformation/medallion-lake/media_medallion_architecture_demo.ipynb) | Content engagement and subscriptions |
| [Real Estate](data-engineering/transformation/medallion-lake/real_estate_medallion_architecture_demo.ipynb) | Property listings and transactions |
| [Retail](data-engineering/transformation/medallion-lake/retail_medallion_architecture_demo.ipynb) | Sales, inventory, and customer data |
| [Telecommunications](data-engineering/transformation/medallion-lake/telecommunications_medallion_architecture_demo.ipynb) | Network usage and customer churn |
| [Transportation](data-engineering/transformation/medallion-lake/transportation_medallion_architecture_demo.ipynb) | Logistics and fleet tracking |

#### Delta Liquid Clustering

Demonstrates Delta Lake liquid clustering for automatic query optimization and data layout management. Industry variants available:

| Notebook | Industry |
|---|---|
| [Education](data-engineering/transformation/liquid-clustering/education_delta_liquid_clustering_demo.ipynb) | Student performance analytics with ML prediction |
| [Energy](data-engineering/transformation/liquid-clustering/energy_delta_liquid_clustering_demo.ipynb) | Smart grid monitoring and anomaly detection |
| [Financial Services](data-engineering/transformation/liquid-clustering/financial_services_delta_liquid_clustering_demo.ipynb) | Transaction analytics and reporting |
| [Healthcare](data-engineering/transformation/l