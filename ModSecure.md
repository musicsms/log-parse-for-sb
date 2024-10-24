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

Incase there are `nginx` already
add `deb-src` to `ubuntu.sources` at `/etc/apt/sources.list.d`
```sh
root@public-service:/etc/apt/sources.list.d# cat ubuntu.sources
###
###
Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

## Ubuntu security updates. Aside from URIs and Suites,
## this should mirror your choices in the previous section.
Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

2. **Download Nginx Source**:
```sh
cd /usr/local/src/
sudo apt-get source nginx
```

3. **Install Nginx Development Tools**:
```sh
sudo apt install nginx-core nginx-dev
```


4. **Build the Nginx ModSecurity Module**:
```
cd /usr/local/src/nginx-<version>  # Replace with the version downloaded by apt-get source

sudo ./configure --with-compat --add-dynamic-module=/usr/local/src/ModSecurity-nginx

sudo make modules
```

5. **Install the Module**:

Copy the compiled module to `Nginx`’s module directory:

```sh
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/
```


```sh
load_module modules/ngx_http_modsecurity_module.so;
```

## ModSecure

**1. Install Required Dependencies**

Make sure to install all the required libraries for full ModSecurity functionality. These dependencies include libraries for **PCRE**, **libjansson** (JSON support), **GeoIP**, **libxml2**, **libyajl**, **liblua**, and **libcurl**.

**For Ubuntu/Debian:**

```sh
sudo apt-get update
sudo apt-get install build-essential autoconf automake libtool pkg-config \
libpcre3-dev libyajl-dev libgeoip-dev libxml2-dev libcurl4-openssl-dev \
liblua5.3-dev libjansson-dev libssl-dev libfuzzy-dev libmaxminddb-dev

sudo apt install libcurl4-openssl-dev -y
```

**For CentOS/RHEL:**

```sh
sudo yum groupinstall "Development Tools"
sudo yum install pcre-devel curl-devel yajl-devel lua-devel jansson-devel \
openssl-devel libxml2-devel geoip-devel yajl-devel libmaxminddb-devel \
fuzzy-devel
```

**2. Download ModSecurity Source Code**

Clone the latest version of ModSecurity from GitHub:

```sh
cd /usr/local/src
sudo git clone --depth 1 -b v3/master https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
sudo git submodule init
sudo git submodule update
```

**3. Prepare the Build Environment**

Before building ModSecurity, you need to prepare the build environment. This step involves running the **build.sh** script and initializing the Git submodules.

```sh
./build.sh
```

**4. Configure ModSecurity with Full Functionality**

Run the configuration tool with options to enable all features, including JSON, Lua, GeoIP, XML, and more. Here’s the complete list of flags to enable full functionality:

```sh
./configure --enable-geoip --enable-luajit --enable-yajl --enable-jansson \
            --enable-pcre2 --with-lua --enable-ip2location --enable-lmdb \
            --enable-fuzzy --with-libxml 
```

**5. Compile and Install ModSecurity**

Once configured, compile ModSecurity by running:

```sh
sudo make
```

After the compilation is complete, install it:
```sh
sudo make install
```

**6. Verify the Build**

After installation, you can verify that ModSecurity has been compiled with full functionality by checking the features in the logs and ensuring the presence of all necessary modules:

```sh
ldd /usr/local/modsecurity/bin/modsec-rules-check
```

**Enable JSON Logging** (Optional):

You can enable **JSON logging** by adding this to your ModSecurity configuration:
```sh
SecAuditLogFormat JSON
```

1. Install **Nginx** with **ModSecurity** module enabled. If not installed, you can use the following:
```sh
sudo apt-get install libnginx-mod-security
```

2. Add the following to your Nginx configuration file to enable ModSecurity:
```nginx
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/modsecurity.conf;
```

**For Apache:**

```sh
sudo apt-get install libapache2-mod-security2
```

2. Add the following to the Apache configuration file:
```apache
<IfModule security2_module>

    Include /usr/local/modsecurity/etc/modsecurity.conf

</IfModule>
```


## Build `Nginx` with ModeSec

**Clone the `Nginx` ModSecurity connector repository**:
```sh
cd /usr/local/src
git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
```

add `deb-src` to `ubuntu.sources` at `/etc/apt/sources.list.d`
```sh
root@public-service:/etc/apt/sources.list.d# cat ubuntu.sources
###
###
Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

## Ubuntu security updates. Aside from URIs and Suites,
## this should mirror your choices in the previous section.
Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```


**Download `Nginx` Source**:

```sh
cd /usr/local/src/
sudo apt-get update
sudo apt-get source nginx
```

3. **Install `Nginx` Development Tools**:
```sh
sudo apt install nginx-core nginx-dev
```


4. **Build the `Nginx` ModSecurity Module**:
```
cd /usr/local/src/nginx-<version>  # Replace with the version downloaded by apt-get source

sudo ./configure --with-compat --add-dynamic-module=/usr/local/src/ModSecurity-nginx

cd .
```

Copy the module build to `nginx` module path at:
1. **Default Installation Path**:

If you installed NGINX using a package manager (like apt on Ubuntu/Debian or yum on CentOS/RHEL), the module might be located in:

```
• /usr/lib/nginx/modules/

• /usr/lib64/nginx/modules/ (on 64-bit systems)

• /usr/local/nginx/modules/ (if you compiled from source)
```

```sh
cp objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/

```

Create module config in `/etc/nginx/modules-enabled`

```sh
root@smartbanking:/usr/local/src/nginx-1.24.0# cd /etc/nginx/modules-enabled/
root@smartbanking:/etc/nginx/modules-enabled# ls
50-mod-http-geoip2.conf        50-mod-http-xslt-filter.conf  50-mod-stream.conf
50-mod-http-image-filter.conf  50-mod-mail.conf              70-mod-stream-geoip2.conf
root@smartbanking:/etc/nginx/modules-enabled# cp 50-mod-mail.conf modsec.conf
root@smartbanking:/etc/nginx/modules-enabled# nano modsec.conf
root@smartbanking:/etc/nginx/modules-enabled#
root@smartbanking:/etc/nginx/modules-enabled# cat modsec.conf
load_module modules/ngx_http_modsecurity_module.so;
root@smartbanking:/etc/nginx/modules-enabled#
```

Create `modesec` folder for `modsecurity` config
```sh
sudo mkdir /etc/nginx/modsec
```
**Copy the Default ModSecurity Configuration**:

ModSecurity comes with a default configuration file that you can use as a starting point. Copy it:
```sh
sudo cp /usr/local/src/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf
```

Download OWASP rule:
```sh
cd /etc/nginx/modsec
sudo git clone https://github.com/coreruleset/coreruleset.git
sudo mv coreruleset/crs-setup.conf.example coreruleset/crs-setup.conf
sudo cp /usr/local/src/ModSecurity/unicode.mapping /etc/nginx/modsec/

```

Update ModSec config
```sh

sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf
sed -i 's/SecAuditLogParts ABIJDEFHZ/SecAuditLogParts ABCEFHJKZ/' /etc/nginx/modsec/modsecurity.conf
sed -i 's/SecAuditEngine RelevantOnly/SecAuditEngine On/' /etc/nginx/modsec/modsecurity.conf
sed -i 's/SecAuditLogType Serial/#SecAuditLogType Serial/' /etc/nginx/modsec/modsecurity.conf
sed -i 's#^SecAuditLog /var/log/modsec_audit.log#SecAuditLogFormat JSON\nSecAuditLogType Concurrent\nSecAuditLogStorageDir /var/log/modsec/\nSecAuditLogFileMode 0777\nSecAuditLogDirMode 0777#' /etc/nginx/modsec/modsecurity.conf
echo "Include /etc/nginx/modsec/modsecurity.conf" > /etc/nginx/modsec/modsec-config.conf
```

```

add modsecurity on `service.conf` in `server` block

```sh
server {

listen 80;

server_name _;

modsecurity on;

modsecurity_rules_file /etc/nginx/modsec/modsec-config.conf;

  

# Please do not modify this configuration. It may cause your service to stop working / dead

# -------------------------------------------- #

location / {

proxy_pass http://service;

proxy_set_header Host $http_host;

# -------------------------------------------- #

# You can modify configuration below.

# if ($request_uri ~* "/flag/flag") { return 404; }

# if ($request_uri ~* "L2ZsYQ") { return 404; }

# if ($request_uri ~* "ZmxhZw") { return 404; }

# if ($request_uri ~* "bGFnLw") { return 404; }

# if ($request_uri ~* "/image-sharing/?f=L2ZsYWcvZmxhZw") { return 404; }

# if ($http_user_agent ~* "Mozilla/5.0 (Linux; Android 4.2.2; SGH-M919 Build/JDQ39) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.169 Mobile Safari/537.22") { return 404; }

# if ($request_uri ~* "cmd") { return 404; }

}

}
```