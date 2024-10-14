def generate_server_rule(server_type, action, endpoint, client_ip=None, payload=None):
    """
    Generate server configuration rule based on server type, action, endpoint, client IP, and payload.

    Parameters:
    server_type (str): The type of server (nginx, apache, caddy2).
    action (str): The action to perform (block, unblock).
    endpoint (str): The endpoint to apply the rule to.
    client_ip (str, optional): The client IP to block. Defaults to None.
    payload (str, optional): The payload to block. Defaults to None.

    Returns:
    str: The generated server configuration rule.
    """
    if server_type == 'nginx':
        if action == 'block':
            if client_ip and payload:
                rule = f"location {endpoint} {{\n    if ($request_body ~* \"{payload}\") {{\n        deny {client_ip};\n    }}\n}}"
            elif client_ip:
                rule = f"location {endpoint} {{\n    deny {client_ip};\n}}"
            elif payload:
                rule = f"location {endpoint} {{\n    if ($request_body ~* \"{payload}\") {{\n        deny all;\n    }}\n}}"
            else:
                rule = f"location {endpoint} {{ deny all; }}"
        elif action == 'unblock':
            rule = f"# location {endpoint} {{ deny all; }}"
    elif server_type == 'apache':
        if action == 'block':
            if client_ip and payload:
                rule = f"<Location {endpoint}>\n    SetEnvIf Request_URI \"{payload}\" block\n    Require not ip {client_ip}\n</Location>"
            elif client_ip:
                rule = f"<Location {endpoint}>\n    Require not ip {client_ip}\n</Location>"
            elif payload:
                rule = f"<Location {endpoint}>\n    SetEnvIf Request_URI \"{payload}\" block\n    Require all denied\n</Location>"
            else:
                rule = f"<Location {endpoint}>\n    Require all denied\n</Location>"
        elif action == 'unblock':
            rule = f"# <Location {endpoint}>\n#     Require all denied\n# </Location>"
    else:
        raise ValueError("Unsupported server type")

    return rule