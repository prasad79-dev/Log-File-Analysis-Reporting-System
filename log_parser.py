import re
from datetime import datetime
import logging

class LogParser:
    LOG_PATTERN = re.compile(
        r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+|-) "(.*?)" "(.*?)"'
    )

    def parse_line(self, line):
        match = self.LOG_PATTERN.match(line)
        if not match:
            logging.warning(f"Malformed line skipped: {line.strip()}")
            return None

        ip = match.group(1)
        timestamp = datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S %z")
        request = match.group(3).split()
        method = request[0] if len(request) > 0 else None
        path = request[1] if len(request) > 1 else None
        status = int(match.group(4))
        bytes_sent = int(match.group(5)) if match.group(5).isdigit() else 0
        referrer = match.group(6) if match.group(6) != "-" else None
        user_agent = match.group(7)

        return {
            "ip_address": ip,
            "timestamp": timestamp,
            "method": method,
            "path": path,
            "status_code": status,
            "bytes_sent": bytes_sent,
            "referrer": referrer,
            "user_agent": user_agent
        }
