from configparser import ConfigParser
from log_parser import LogParser
from mysql_handler import MySQLHandler
from tabulate import tabulate
import argparse
import logging
import os

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_config():
    config = ConfigParser()
    config.read("config.ini")
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
        "database": config["mysql"]["database"]
    }

def main():
    parser = argparse.ArgumentParser(description="Log File Analyzer CLI")
    subparsers = parser.add_subparsers(dest="command")

    # process_logs command
    process_parser = subparsers.add_parser("process_logs", help="Parse and load logs from a file.")
    process_parser.add_argument('file_path', type=str, help='Path to the log file.')
    process_parser.add_argument('--batch_size', type=int, default=1000, help='Batch size for DB inserts.')

    # generate_report command
    report_parser = subparsers.add_parser("generate_report", help="Generate analytical reports.")
    report_parser.add_argument("report_type", choices=[
        "top_ips", "status_distribution", "hourly_traffic", "top_pages", "traffic_by_os", "error_logs"
    ])
    report_parser.add_argument("--n", type=int, help="Top N items (for top_ips or top_pages)")
    report_parser.add_argument("--date", help="Filter by date (YYYY-MM-DD) for error_logs")

    args = parser.parse_args()
    config = load_config()
    db = MySQLHandler(**config)
    parser = LogParser()

    if args.command == "process_logs":
        if not os.path.exists(args.file_path):
            logging.error("Log file does not exist.")
            return

        print(f"Processing log file: {args.file_path}")
        db.create_tables()
        batch = []
        count = 0

        with open(args.file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parsed = parser.parse_line(line)
                if parsed:
                    batch.append(parsed)
                    count += 1
                    if len(batch) >= args.batch_size:
                        db.insert_batch_log_entries(batch)
                        if count % 500 == 0:
                            logging.info(f"Processed {count} lines.")
                        batch = []
                else:
                    logging.warning(f"Malformed line skipped: {line.strip()}")

        if batch:
            db.insert_batch_log_entries(batch)

        logging.info(f"Finished processing log file. Total lines loaded: {count}")

    elif args.command == "generate_report":
        if args.report_type == "top_ips":
            data = db.get_top_n_ips(args.n or 5)
            print(tabulate(data, headers=["IP Address", "Requests"]))
        elif args.report_type == "status_distribution":
            data = db.get_status_code_distribution()
            print(tabulate(data, headers=["Status Code", "Count", "Percentage"]))
        elif args.report_type == "hourly_traffic":
            data = db.get_hourly_traffic()
            print(tabulate(data, headers=["Hour", "Request Count"]))
        elif args.report_type == "top_pages":
            data = db.get_top_n_pages(args.n or 5)
            print(tabulate(data, headers=["Page", "Hits"]))
        elif args.report_type == "traffic_by_os":
            data = db.get_traffic_by_os()
            print(tabulate(data, headers=["OS", "Requests"]))
        elif args.report_type == "error_logs":
            if not args.date:
                print("Please provide --date in YYYY-MM-DD format.")
            else:
                data = db.get_error_logs_by_date(args.date)
                print(tabulate(data, headers=["IP", "Timestamp", "Path", "Status", "User-Agent"]))
    else:
        parser.print_help()

    db.close()

if __name__ == "__main__":
    main()

