
## **Step 1: Install Dependencies**


Before compiling ModSecurity, install the required dependencies:

```sh
sudo apt update
sudo apt install git build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev libxml2 libxml2-dev libyajl-dev libgeoip-dev libtool automake autoconf
```
## **Step 2: Clone and Install ModSecurity (v3)**

  
ModSecurity is available as a standalone library (v3) and can be compiled separately from Nginx.

1. **Clone the ModSecurity repository**:

```
cd /usr/local/src
git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity
```

2. **Build ModSecurity**:
```sh
cd ModSecurity
git submodule init
git submodule update
./build.sh
./configure
make
sudo make install
```
This will install ModSecurity v3, which is the recommended version for modern `Nginx` setups.
**Step 3: Clone and Compile the `Nginx` ModSecurity Connector**

The `Nginx` ModSecurity module acts as a connector between `Nginx` and the ModSecurity library.

1. **Clone the `Nginx` ModSecurity connector repository**:
```sh
cd /usr/local/src
git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
```
2. **Download Nginx Source**:

Download the version of `Nginx` you want to compile with the ModSecurity module. Here’s how to download and extract `Nginx`:
```sh
cd /usr/local/src
wget http://nginx.org/download/nginx-<version>.tar.gz
tar -xzvf nginx-<version>.tar.gz
cd nginx-<version>
```
Replace `<version>` with the Nginx version you wish to use (e.g., 1.20.1).

3. **Configure `Nginx` with ModSecurity**:

In this step, you compile `Nginx` along with the ModSecurity module:
```sh
./configure --with-compat --add-module=/usr/local/src/ModSecurity-nginx
```

This tells Nginx to include the ModSecurity connector module.

4. **Compile and Install Nginx**:
```sh
make
sudo make install
```

This will build Nginx with the ModSecurity module.
**Step 4: Configure Nginx with ModSecurity**

Once both ModSecurity and Nginx are compiled and installed, you need to enable ModSecurity in Nginx’s configuration.

1. **Edit the Nginx configuration file** (e.g., `/usr/local/nginx/conf/nginx.conf`):
```nginx-config
http {
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/modsecurity.conf;

    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://backend;
        }
    }
}
```

2. **Create a ModSecurity Configuration File**:
```sh
sudo mkdir /etc/nginx/modsec
sudo cp /usr/local/src/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf
```
Then, edit the `modsecurity.conf`file to enable the rules:
```sh
sudo nano /etc/nginx/modsec/modsecurity.conf
```

Change the `SecRuleEngine` setting to "On":
```sh
SecRuleEngine On
```

**Step 5: Restart `Nginx`**
After configuring Nginx, restart the service to apply the changes:
```sh
service nginx restart
```