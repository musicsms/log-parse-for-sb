import streamlit as st
import pandas as pd
from parse_logs import parse_logs
from generate_rule import generate_server_rule

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit UI
st.title('Security Log Management')

# File uploader for security logs
log_file = st.file_uploader('Upload Security Log File', type=['log', 'txt', 'csv', 'json'])

if log_file:
    # Detect log type
    first_line = log_file.readline().decode('utf-8').strip()
    log_file.seek(0)  # Reset file pointer to the beginning

    if 'nginx' in first_line.lower() or 'nginx' in log_file.name.lower():
        log_type = 'nginx'
    elif 'apache' in first_line.lower() or 'apache' in log_file.name.lower():
        log_type = 'apache'
    else:
        st.error('Unsupported log type')
        st.stop()

    logs = parse_logs(log_file, log_type)
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
        rule = generate_server_rule(server_type, action, endpoint, client_ip)
        st.code(rule, language=server_type)
        st.success(f'Successfully generated configuration for action: {action} on endpoint: {endpoint} for server: {server_type}')