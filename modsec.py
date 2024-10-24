import streamlit as st
import paramiko

def ssh_connect(host, port, username, password=None, key_path=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if key_path:
        client.connect(hostname=host, port=port, username=username, key_filename=key_path)
    else:
        client.connect(hostname=host, port=port, username=username, password=password)
    return client

def execute_commands(client, commands):
    output = []
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()
        output.append(stdout.read().decode() + stderr.read().decode())
    return output

def install_modsecurity(client):
    commands = [
        "sudo apt update",
        "sudo apt install -y git build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev libxml2 libxml2-dev libyajl-dev libgeoip-dev libtool automake autoconf",
        "cd /usr/local/src && git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity",
        "cd /usr/local/src/ModSecurity && git submodule init && git submodule update && ./build.sh && ./configure && make && sudo make install",
        "cd /usr/local/src && git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git",
        "cd /usr/local/src && wget http://nginx.org/download/nginx-1.20.1.tar.gz && tar -xzvf nginx-1.20.1.tar.gz && cd nginx-1.20.1 && ./configure --with-compat --add-module=/usr/local/src/ModSecurity-nginx && make && sudo make install",
        "sudo mkdir /etc/nginx/modsec && sudo cp /usr/local/src/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf",
        "sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf",
        "sudo service nginx restart"
    ]
    return execute_commands(client, commands)

st.title('ModSecurity Installer')

with st.form('install_form'):
    host = st.text_input('Host')
    port = st.number_input('Port', min_value=1, max_value=65535, value=22)
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    key_path = st.text_input('Path to SSH Key File')
    submit_button = st.form_submit_button('Install ModSecurity')

if submit_button:
    client = ssh_connect(host, port, username, password=password, key_path=key_path)
    output = install_modsecurity(client)
    for line in output:
        st.text(line)
    client.close()