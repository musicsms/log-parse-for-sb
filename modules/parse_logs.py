import re
from datetime import datetime
from Evtx.Evtx import Evtx
import xmltodict
import json

def parse_all_logs(log_file, log_type):
    logs = []

    if log_type in ['nginx', 'apache']:
        if log_type == 'nginx':
            access_log_pattern = re.compile(
                r'(?P<client>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<endpoint>[^ ]+) HTTP/[^"]+" (?P<status_code>\d+) [^ ]+ "[^"]*" "[^"]*"'
            )
            error_log_pattern = re.compile(
                r'(?P<timestamp>\d+/\d+/\d+ \d+:\d+:\d+) \[error\] \d+#\d+: \*\d+ (?P<message>[^,]+), client: (?P<client>[^,]+), server: [^,]+, request: "(?P<method>\w+) (?P<endpoint>[^ ]+) HTTP/[^"]+"'
            )
        elif log_type == 'apache':
            access_log_pattern = re.compile(
                r'(?P<client>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<endpoint>[^ ]+) HTTP/[^"]+" (?P<status_code>\d+) [^ ]+ "[^"]*" "[^"]*"'
            )
            error_log_pattern = re.compile(
                r'\[(?P<timestamp>[^\]]+)\] \[error\] \[client (?P<client>[^\]]+)\] (?P<message>.+), referer: (?P<referer>[^\]]+)'
            )

        for line in log_file:
            line = line.decode('utf-8').strip()
            access_match = access_log_pattern.match(line)
            error_match = error_log_pattern.match(line)

            if access_match:
                log_entry = access_match.groupdict()
                log_entry['timestamp'] = datetime.strptime(log_entry['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
                log_entry['message'] = ''
                logs.append(log_entry)
            elif error_match:
                log_entry = error_match.groupdict()
                log_entry['timestamp'] = datetime.strptime(log_entry['timestamp'], '%d/%b/%Y:%H:%M:%S')
                log_entry['status_code'] = 'error'
                logs.append(log_entry)

    elif log_type == 'windows':
        with Evtx(log_file) as evtx_log:
            for record in evtx_log.records():
                try:
                    event_data = xmltodict.parse(record.xml())
                    logs.append(event_data)
                except Exception as e:
                    print(f"Error parsing record: {e}")

        logs = [json.dumps(log, indent=4) for log in logs]

    return logs