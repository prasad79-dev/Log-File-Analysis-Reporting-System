# Log File Analysis & Reporting System

The **Log File Analysis & Reporting System** is a Python-based command-line tool designed to process Apache-style web server logs.  
It reads raw log files and extracts structured information such as IP addresses, timestamps, HTTP methods, URLs, status codes, 
and user-agent details.  
The parsed data is stored in a MySQL database for efficient querying.  
Users can generate detailed reports, including top visitors, traffic patterns, error occurrences, and device usage statistics, 
enabling quick and clear insights into web server activity.

## Table of Contents
1. [Introduction / Overview](#introduction--overview)
2. [Objectives / Goals](#objectives--goals)
3. [Features](#features)
4. [System Architecture](#system-architecture)
5. [Technologies Used](#technologies-used)
6. [Prerequisites](#prerequisites)
7. [Usage](#usage)
8. [Database Schema](#database-schema)
9. [Future Enhancements](#future-enhancements)

## Introduction / Overview

The **Log File Analysis & Reporting System** is a Python-based command-line application designed to process and analyze Apache-style web server logs.  
It extracts meaningful data such as IP addresses, timestamps, HTTP methods, URLs, status codes, and user-agent details, and stores this structured information in a MySQL database for efficient querying and reporting.

This project is needed because raw web server logs are often large, unstructured, and difficult to interpret manually.  
By automating the parsing, storage, and reporting process, this tool helps developers, system administrators, and analysts quickly identify traffic patterns, detect errors, and gain insights into website usage.

**Intended Users:**
- Web administrators who need to monitor server activity.
- Data analysts looking for trends in website traffic.
- Developers who want to debug website issues based on log data.

## Objectives / Goals

The main objectives of the **Log File Analysis & Reporting System** are:

1. **Automate Log Parsing**  
   - Read and process large Apache-style log files without manual intervention.

2. **Structure and Store Data Efficiently**  
   - Organize extracted data into a normalized MySQL database for fast and easy querying.

3. **Generate Meaningful Reports**  
   - Provide insights such as top visitors, popular pages, traffic patterns, and error statistics.

4. **Support Decision-Making**  
   - Help administrators and analysts make informed decisions based on accurate traffic and error data.

5. **Improve Monitoring and Maintenance**  
   - Enable quick identification of server issues and unusual access patterns.

## Features

- **Log File Parsing** – Extracts IP address, timestamp, HTTP method, URL path, status code, bytes sent, referrer, and user-agent from Apache-style logs.
- **User-Agent Normalization** – Separates browser, operating system, and device type into a dedicated lookup table.
- **Batch Data Insertion** – Loads log data into MySQL in batches for better performance.
- **Multiple Report Types** – Generates reports for:
  - Top IP addresses
  - HTTP status code distribution
  - Hourly traffic
  - Most visited pages
  - Traffic by operating system
  - Error logs by date
- **Configurable Settings** – Allows changing batch size and database connection through a `config.ini` file.
- **Error Handling** – Skips malformed log entries and logs issues for review.
- **Command-Line Interface (CLI)** – Simple commands for processing logs and generating reports.

## System Architecture

The **Log File Analysis & Reporting System** follows a straightforward workflow that moves from raw log files to meaningful reports.

**Workflow Steps:**
1. **Input (Raw Log Files)**  
   - Apache-style access logs are provided as input to the system.

2. **Log Parsing (Regex-based)**  
   - Each log line is processed using regular expressions to extract key fields like IP, timestamp, method, URL, status code, bytes sent, referrer, and user-agent.

3. **Data Normalization**  
   - User-agent strings are analyzed and split into operating system, browser, and device type, which are stored in a separate lookup table.

4. **Database Storage (MySQL)**  
   - Structured data is batch-inserted into MySQL tables (`log_entries` and `user_agents`) for efficient storage and retrieval.

5. **Report Generation (SQL Queries)**  
   - Predefined SQL queries fetch aggregated results, such as top IP addresses, traffic by hour, error logs, and status code distributions.

6. **Output (CLI Reports)**  
   - Results are displayed in the terminal in tabular format using the `tabulate` library.

---

**Architecture Diagram:**

### **Architecture Diagram**

```plaintext
          ┌────────────────────┐
          │  Raw Log Files      │
          │ (Apache Access Logs)│
          └─────────┬───────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ Log Parser (Regex) │
          │  Extract Fields    │
          └─────────┬───────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ Data Normalization │
          │ Split User-Agent   │
          └─────────┬───────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ MySQL Database     │
          │ log_entries &      │
          │ user_agents tables │
          └─────────┬───────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ Report Generation  │
          │  (SQL Queries)     │
          └─────────┬───────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ CLI Output         │
          │ Tabular Reports    │
          └────────────────────┘
```
## Technologies Used

- **Programming Language:**  
  - Python 3.8+

- **Database:**  
  - MySQL (for structured storage and efficient querying)

- **Python Libraries:**  
  - **mysql-connector-python** – For connecting and interacting with MySQL databases.
  - **tabulate** – For displaying reports in well-formatted tables.
  - **configparser** – For reading configuration settings from the `config.ini` file.
  - **logging** – For capturing and recording logs during execution.
  - **re** – For using regular expressions to parse log files.
  - **datetime** – For handling and formatting timestamps.

- **Frameworks:**  
  - None (CLI-based project using core Python and libraries)

- **Tools:**  
  - Command-Line Interface (CLI)
  - Git for version control
  - Virtual environments for package management

## Prerequisites

Before running the **Log File Analysis & Reporting System**, ensure the following are installed and set up on your system:

- **Python**  
  - Version: Python 3.8 or newer  
  - Verify installation:  
    ```bash
    python --version
    ```

- **MySQL Database Server**  
  - Ensure MySQL is installed and running.  
  - Verify installation:  
    ```bash
    mysql --version
    ```

- **pip (Python package manager)**  
  - Comes pre-installed with Python 3.4+  
  - Verify installation:  
    ```bash
    pip --version
    ```

- **Required Python Packages**  
  - Listed in the `requirements.txt` file.  
  - Install them using:  
    ```bash
    pip install -r requirements.txt
    ```

- **Git** *(optional but recommended)*  
  - For cloning the repository.  
  - Verify installation:  
    ```bash
    git --version
    ```

- **Access to Apache-style Log Files**  
  - The tool is designed to parse standard Apache/Nginx access logs.

## Usage

Once the environment is set up and the configuration is complete, you can run the **Log File Analysis & Reporting System** from the command line.

---

### 1. View Available Options and Usage Help
```bash
python main.py process_logs - help
```

### **2. Process a Log File**
This command reads an Apache-style log file, parses it, and stores the structured data in the MySQL database.

```bash
python main.py process_logs sample_logs/access.log - batch_size 500
```
### **3. Generate Reports**
You can generate various analytical reports using different sub commands.

## a. Top IP Addresses
Shows the most frequent visitors to the site.
```bash
python main.py generate_report top_n_ips 5
```

## b. Status Code Distribution
Displays the breakdown of HTTP status codes (e.g., 200, 404, 500).
```bash
python main.py generate_report status_code_distribution
```

## c. Hourly Traffic
Shows traffic volume for each hour of the day.
```bash
python main.py generate_report hourly_traffic
```
# Database Schema

## Overview
This schema consists of two main tables designed to store parsed log data efficiently with normalized user agent information.

---

## Tables

### 1. `log_entries`

| Column Name   | Data Type     | Constraints                     | Description                          |
|---------------|---------------|---------------------------------|--------------------------------------|
| id            | INT           | PRIMARY KEY, AUTO_INCREMENT     | Unique log entry identifier          |
| ip_address    | VARCHAR(45)   | NOT NULL                        | Client IP address (IPv4 or IPv6)     |
| timestamp     | DATETIME      | NOT NULL                        | Exact time when the request was made |
| method        | VARCHAR(10)   | NOT NULL                        | HTTP method (GET, POST, etc.)        |
| path          | VARCHAR(2048) | NOT NULL                        | Requested URL path                   |
| status_code   | SMALLINT      | NOT NULL                        | HTTP response status code            |
| bytes_sent    | INT           | NOT NULL                        | Number of bytes sent (0 if missing)  |
| referrer      | VARCHAR(2048) | NULLABLE                        | Referrer URL                         |
| user_agent_id | INT           | FOREIGN KEY (`user_agents.id`)  | Link to user agent details           |
| created_at    | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP       | Timestamp when record was loaded     |

---

### 2. `user_agents`

| Column Name       | Data Type    | Constraints                  | Description                          |
|-------------------|--------------|------------------------------|--------------------------------------|
| id                | INT          | PRIMARY KEY, AUTO_INCREMENT  | Unique user agent identifier         |
| user_agent_string | VARCHAR(512) | UNIQUE, NOT NULL             | Full user agent string               |
| os                | VARCHAR(100) | NULLABLE                     | Operating System (e.g., Windows)     |
| browser           | VARCHAR(100) | NULLABLE                     | Browser name (e.g., Chrome, Firefox) |
| device_type       | VARCHAR(50)  | NULLABLE                     | Device type (Desktop, Mobile, Tablet)|
| created_at        | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP    | Timestamp when record was added      |

---

## Relationships

- The `log_entries` table has a **many-to-one** relationship with `user_agents` via the `user_agent_id` foreign key.
- Each log entry references one user agent, allowing normalization and avoiding redundant storage of repeated user agent strings.

---

## Indexing Suggestions (Optional)

- Index on `ip_address` in `log_entries` for fast IP-based queries.
- Index on `timestamp` in `log_entries` to optimize time-range searches.
- Index on `status_code` in `log_entries` to speed up status code reports.
- Unique index on `user_agent_string` in `user_agents` to prevent duplicates.

---

*Prepared for Log File Analysis & Reporting System*

# Future Enhancements

This section outlines planned or possible improvements to enhance the functionality, performance, and usability of the Log File Analysis & Reporting System.

---

## 1. Real-Time Log Processing
- Implement streaming log ingestion for near real-time analytics.
- Integrate with tools like Apache Kafka or AWS Kinesis for scalable log collection.

## 2. Advanced Reporting & Visualization
- Add graphical dashboards using libraries like Plotly, Grafana, or Power BI.
- Support customizable reports with filters by date, IP, status codes, etc.
- Export reports to PDF, Excel, or interactive HTML formats.

## 3. Enhanced User Agent Parsing
- Improve user agent string parsing to detect more detailed OS, browser versions, and device models.
- Support automated updates for user agent parsing rules.

## 4. Alerting & Anomaly Detection
- Set up automated alerts for abnormal traffic patterns (e.g., spikes, DDOS attempts).
- Use ML models to detect anomalies or suspicious behaviors.

## 5. Multi-Format Log Support
- Extend support beyond Apache logs to include Nginx, IIS, and custom log formats.
- Add a configuration interface to specify log parsing rules dynamically.

## 6. Scalability and Performance Optimization
- Optimize batch inserts with bulk loading techniques.
- Add caching layers to reduce database query load.
- Implement horizontal scaling for database and processing components.

## 7. Security Improvements
- Implement role-based access control (RBAC) for report generation and data access.
- Encrypt sensitive data both in transit and at rest.

## 8. Cloud and Containerization Support
- Provide Docker images for easy deployment.
- Integrate with cloud databases and storage solutions for better availability.

## 9. API Access
- Develop RESTful APIs for programmatic access to log data and reports.
- Enable integration with external monitoring and alerting tools.

## 10. User Interface
- Build a web-based UI for easier interaction, report viewing, and configuration.

---

*These enhancements aim to make the system more robust, scalable, user-friendly, and suitable for enterprise-grade deployments.*
