# Security Log Management Tool

## Purpose

The Security Log Management Tool is designed to help administrators and security professionals manage and analyze security logs from various sources, including web servers (Nginx, Apache) and Windows Event Logs. This tool provides a user-friendly interface to upload, parse, and visualize logs, as well as generate server rules for blocking or unblocking specific clients or endpoints.

## Features

- **Log Parsing**: Supports parsing of Nginx, Apache, and Windows Event Logs.
- **Data Visualization**: Displays parsed logs in a sortable and filterable table.
- **Rule Generation**: Generates server configuration rules for blocking or unblocking clients or endpoints.
- **File Upload**: Allows users to upload log files directly through the interface.

## How to Use

### Prerequisites

- Python 3.x
- Required Python packages: `streamlit`, `pandas`, `Evtx`, `xmltodict`

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/security-log-management-tool.git
    cd security-log-management-tool
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. Start the Streamlit application:
    ```sh
    streamlit run main.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

### Using the Tool

1. **Upload Security Logs**:
    - Navigate to the "Security Logs" tab.
    - Upload a log file (supported formats: `.log`, `.txt`, `.csv`, `.json`).
    - The tool will automatically detect the log type (Nginx or Apache) and parse the logs.
    - View the parsed logs in a table format.

2. **Generate Server Rules**:
    - Select a client IP and endpoint from the parsed logs.
    - Choose an action (block or unblock) and server type (Nginx or Apache).
    - Click "Generate Configuration" to create the server rule.
    - The generated rule will be displayed, and you can copy it to your server configuration.

3. **Upload Windows Event Logs**:
    - Navigate to the "Windows Event Logs" tab.
    - Upload a Windows Event Log file (supported format: `.evtx`).
    - The tool will parse the logs and display them in a table format, including the full JSON event log.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any questions or issues, please open an issue on GitHub or contact the repository owner.