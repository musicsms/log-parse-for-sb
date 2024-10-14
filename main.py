import streamlit as st
import pandas as pd
import os
from modules.parse_logs import parse_all_logs as parse_logs
from modules.generate_rule import generate_server_rule as gen_rule
import json

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit UI
st.title('Security Log Management')

# Create tabs
tab1, tab2 = st.tabs(["Security Logs", "Windows Event Logs"])

with tab1:
    # File uploader for security logs
    log_file = st.file_uploader('Upload Security Log File', type=['log', 'txt', 'csv', 'json'])

    if log_file:
        # Save the uploaded file to the logs directory
        log_file_path = os.path.join('logs', log_file.name)
        with open(log_file_path, 'wb') as f:
            f.write(log_file.getbuffer())

        # Detect log type
        with open(log_file_path, 'r') as f:
            first_line = f.readline().strip()

        if 'nginx' in first_line.lower() or 'nginx' in log_file.name.lower():
            log_type = 'nginx'
        elif 'apache' in first_line.lower() or 'apache' in log_file.name.lower():
            log_type = 'apache'
        else:
            st.error('Unsupported log type')
            st.stop()

        with open(log_file_path, 'rb') as f:
            logs = parse_logs(f, log_type)
        df = pd.DataFrame(logs, columns=['timestamp', 'client', 'endpoint', 'status_code', 'method', 'message'])

        # Count requests from each IP
        ip_counts = df['client'].value_counts().reset_index()
        ip_counts.columns = ['client', 'Request Count']

        # Merge the counts with the original dataframe
        df = df.merge(ip_counts, on='client')

        st.write('Parsed Security Logs:')
        st.dataframe(df)  # Use st.dataframe for sortable and filterable table

        st.write('---')

        # Input for client IP and endpoint selection from logs
        client_ip = st.selectbox('Client IP to Block (optional)', options=[''] + df['client'].unique().tolist())
        endpoint = st.selectbox('Endpoint to Block/Unblock', options=df['endpoint'].unique().tolist())
        action = st.selectbox('Action', ['block', 'unblock'])
        server_type = st.selectbox('Server Type', ['nginx', 'apache'])
        payload = st.text_input('Payload to Block (optional)')

        if st.button('Generate Configuration'):
            rule = gen_rule(server_type, action, endpoint, client_ip)
            st.code(rule, language=server_type)
            st.success(f'Successfully generated configuration for action: {action} on endpoint: {endpoint} for server: {server_type}')

with tab2:
    # File uploader for Windows Event Logger files
    event_log_file = st.file_uploader('Upload Windows Event Log File', type=['evtx'])

    if event_log_file:
        # Save the uploaded file to the logs directory
        event_log_file_path = os.path.join('logs', event_log_file.name)
        with open(event_log_file_path, 'wb') as f:
            f.write(event_log_file.getbuffer())

        # Parse the Windows Event Log file
        json_logs = parse_logs(event_log_file_path, 'windows')

        # Convert JSON logs to DataFrame and add a column for the whole JSON event log
        df = pd.json_normalize([json.loads(log) for log in json_logs])
        df['json_event_log'] = json_logs

        st.write('Parsed Windows Event Logs:')
        st.dataframe(df)