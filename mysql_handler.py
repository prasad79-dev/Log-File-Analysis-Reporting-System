import mysql.connector
import logging
from datetime import datetime

class MySQLHandler:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_agents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_agent_string VARCHAR(512) UNIQUE NOT NULL,
                os VARCHAR(100),
                browser VARCHAR(100),
                device_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_address VARCHAR(45) NOT NULL,
                timestamp DATETIME NOT NULL,
                method VARCHAR(10) NOT NULL,
                path VARCHAR(2048) NOT NULL,
                status_code SMALLINT NOT NULL,
                bytes_sent INT NOT NULL,
                referrer VARCHAR(2048),
                user_agent_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_agent_id) REFERENCES user_agents(id)
            )
        """)

        self.conn.commit()
        cursor.close()

    def insert_batch_log_entries(self, entries):
        if not entries:
            return

        cursor = self.conn.cursor()
        query = """
            INSERT INTO log_entries (
                ip_address, timestamp, method, path,
                status_code, bytes_sent, referrer, user_agent_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            values = [
                (
                    entry["ip_address"],
                    entry["timestamp"],
                    entry["method"],
                    entry["path"],
                    entry["status_code"],
                    entry["bytes_sent"],
                    entry.get("referrer"),
                    entry.get("user_agent_id", None)
                )
                for entry in entries
            ]
            cursor.executemany(query, values)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Batch insert failed: {e}")
        finally:
            cursor.close()

    def get_top_n_ips(self, n=5):
        cursor = self.conn.cursor()
        query = """
            SELECT ip_address, COUNT(*) AS request_count
            FROM log_entries
            GROUP BY ip_address
            ORDER BY request_count DESC
            LIMIT %s
        """
        cursor.execute(query, (n,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_status_code_distribution(self):
        cursor = self.conn.cursor()
        query = """
            SELECT status_code, COUNT(*) AS count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM log_entries), 2) AS percentage
            FROM log_entries
            GROUP BY status_code
            ORDER BY count DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_hourly_traffic(self):
        cursor = self.conn.cursor()
        query = """
            SELECT HOUR(timestamp) AS hour, COUNT(*) AS request_count
            FROM log_entries
            GROUP BY hour
            ORDER BY hour
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_top_n_pages(self, n=5):
        cursor = self.conn.cursor()
        query = """
            SELECT path, COUNT(*) AS hits
            FROM log_entries
            GROUP BY path
            ORDER BY hits DESC
            LIMIT %s
        """
        cursor.execute(query, (n,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_traffic_by_os(self):
        cursor = self.conn.cursor()
        query = """
            SELECT ua.os, COUNT(le.id) AS request_count
            FROM log_entries le
            JOIN user_agents ua ON le.user_agent_id = ua.id
            GROUP BY ua.os
            ORDER BY request_count DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_error_logs_by_date(self, date):
        cursor = self.conn.cursor()
        query = """
            SELECT le.ip_address, le.timestamp, le.path, le.status_code, ua.user_agent_string
            FROM log_entries le
            JOIN user_agents ua ON le.user_agent_id = ua.id
            WHERE DATE(le.timestamp) = %s AND le.status_code >= 400
            ORDER BY le.timestamp
        """
        cursor.execute(query, (date,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def close(self):
        self.conn.close()
