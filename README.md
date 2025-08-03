# Log File Analysis & Reporting System

This is a CLI-based Python project that simulates a real-world data engineering task — parsing and analyzing web server log files (e.g., Apache logs), storing structured data in MySQL, and generating traffic and behavior reports.

---

## Project Features

-  Parses large Apache-style log files line-by-line using regular expressions
-  Extracts key fields: IP address, timestamp, HTTP method, URL, status code, bytes sent, referrer, and user agent
-  Normalizes user agent data into a separate table (`user_agents`)
-  Stores log entries in a well-indexed MySQL schema (`log_entries`)
-  Efficient batch loading using `executemany`
-  CLI interface with reporting commands for traffic insights

---

## Project Structure

log_analyzer_cli/
├── main.py # CLI entry point
├── log_parser.py # Log parsing using regex
├── mysql_handler.py # MySQL DB operations
├── config.ini # DB credentials/config
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── sample_logs/
│ └── access.log # Sample Apache log file
└── sql/
└── create_tables.sql # MySQL schema DDL

# Install Python dependencies:-

pip install -r requirements.txt

# Setup MySQL Database
Create a MySQL database (e.g., weblogs_db)
Run the provided SQL script:

mysql -u root -p

# Configure database credentials
Edit the config.ini file:

[mysql]
host = localhost
user = root
password = @badhri2728D@
database = log_analysis_db

# Log Format Assumed
Apache Common Log Format (with referrer and user agent):

127.0.0.1 - - [10/Jul/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Regex Pattern Used
The log line is parsed using this pattern:

r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+) "(.*?)" "(.*?)"'

Group mapping:

1: IP address
2: Timestamp
3: Request method/path
4: Status code
5: Bytes sent
6: Referrer
7: User Agent

# CLI Usage
View help

python main.py --help

# Process log file

python main.py process_logs sample_logs/access.log --batch_size 500

# Generate reports
# Top N requesting IPs

python main.py generate_report top_ips --n 5

# HTTP status code distribution

python main.py generate_report status_code_distribution

# Hourly traffic

python main.py generate_report hourly_traffic

# Top N requested pages

python main.py generate_report top_pages --n 5

# Traffic by Operating System

python main.py generate_report traffic_by_os

# Error logs for a specific date

python main.py generate_report error_logs_by_date --date 2023-08-01


# Database Schema:

# log_entries Table:

| Column          | Type          | Description                 |
| --------------- | ------------- | --------------------------- |
| id              | INT           | Primary Key                 |
| ip_address      | VARCHAR(45)   | IPv4 or IPv6 address        |
| timestamp       | DATETIME      | Timestamp of request        |
| method          | VARCHAR(10)   | HTTP method (GET, POST)     |
| path            | VARCHAR(2048) | Requested URL path          |
| status_code     | SMALLINT      | HTTP status code            |
| bytes_sent      | INT           | Size of response in bytes   |
| referrer        | VARCHAR(2048) | Referring URL (nullable)    |
| user_agent_id   | INT           | FK to `user_agents.id`      |
| created_at      | TIMESTAMP     | Default: CURRENT_TIMESTAMP  |

# user_agents Table:

| Column              | Type         | Description                 |
| ------------------- | ------------ | --------------------------- |
| id                  | INT          | Primary Key                 |
| user_agent_string   | VARCHAR(512) | Raw user agent string       |
| os                  | VARCHAR(100) | Operating System parsed     |
| browser             | VARCHAR(100) | Browser parsed              |
| device_type         | VARCHAR(50)  | Desktop / Mobile / Tablet   |
| created_at          | TIMESTAMP    | Default: CURRENT_TIMESTAMP  |


# Known Limitations

Currently assumes logs follow the Apache Common Log Format exactly
Simple regex parsing — may fail on exotic formats
User-Agent parsing is basic (optional upgrade: use user-agents library)
No real-time log tailing (bonus feature)
No dashboard integration (can be added with Metabase + MySQL)

# Future Enhancements

Tail log file in real time (tail_logs)
Add geolocation using IP → Country/City APIs
User-agent parsing using user-agents Python library
Export reports to CSV/JSON
Build web dashboard (Metabase, Flask, etc.)

# Requirements
Install all dependencies with:

pip install -r requirements.txt


# requirements.txt

mysql-connector-python==8.0.30
tabulate==0.8.9

(Optionally add user-agents and click for bonus features)

#  Sample Output

python main.py generate_report top_ips --n 5
+----------------+------------------+
| IP Address     | Request Count    |
+----------------+------------------+
| 192.168.1.100  | 250              |
| 203.0.113.45   | 180              |
| 172.16.0.2     | 120              |
| 10.0.0.5       | 90               |
| 198.51.100.1   | 75               |
+----------------+------------------+

