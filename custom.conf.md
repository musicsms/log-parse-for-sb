```conf
SecRule ARGS "L2ZsYQ" "id:1001,phase:1,deny,msg:"Block encode base64 /flag/"

SecRule ARGS "ZmxhZw" "id:1002,phase:1,deny,msg:"Block encode base64 /flag/"

SecRule ARGS "bGFnLw" "id:1003,phase:1,deny,msg:"Block encode base64 /flag/"

SecRule ARGS "/flag" "id:1004,phase:2,t:base64Decode,t:lowercase,deny,msg:'Request contains /flag'"

SecRule REQUEST_HEADERS:X-File-Name ".*\.php" "id:1005,phase:2,t:lowercase,deny,status:403,log,msg:'PHP extension in X-File-Name header'"

SecRule REQUEST_BODY "(?i:(<\?php|eval\(|base64_decode\(|shell_exec\(|system\(|passthru\(|popen\(|proc_open\()" "id:1011,phase:2,deny,status:403,log,msg:'Blocked potential PHP web shell upload'"

  
  

## New Rule

# Detect /flag in various locations: URI, headers, body

SecRule REQUEST_URI|REQUEST_HEADERS|REQUEST_BODY "@contains /flag" "id:1006,phase:2,deny,msg:'Block direct /flag in URI, headers, or body'"

  

# Detect encoded and obfuscated versions of /flag

SecRule ARGS "@rx (\/|%2f|%5c|%252f|\\\\|\\\/)f(l|%6c|%4c)ag" \

"id:1007,phase:2,t:urlDecodeUni,t:lowercase,deny,msg:'Block URL encoded or obfuscated /flag'"

  
  

# # Detect /flag split across multiple arguments

# SecRule ARGS_NAMES|ARGS|REQUEST_BODY "@rx f.{0,3}l.{0,3}a.{0,3}g" \

# "id:1008,phase:2,t:lowercase,t:compressWhitespace,deny,msg:'Block fragmented /flag in parameters or body'"

  
  

# Detect /flag in base64 encoded form using broader transformations

SecRule ARGS "@rx (L2ZsYQ|ZmxhZw|bGFnLw)" \

"id:1009,phase:2,t:base64Decode,t:urlDecodeUni,t:lowercase,t:compressWhitespace,deny,msg:'Detect obfuscated /flag in base64 and other encodings'"

  

# Generic catch-all rule for any encoded variants of /flag

SecRule ARGS|REQUEST_BODY "@contains ZmxhZw==" "id:1010,phase:2,t:base64Decode,t:lowercase,deny,msg:'Base64 encoded /flag'"

  
  

# Block /flag in URI, headers, and body with multiple transformations

SecRule REQUEST_URI|REQUEST_HEADERS|REQUEST_BODY "@contains /flag" \

"id:10060,phase:2,t:base64Decode,t:lowercase,t:urlDecodeUni,t:htmlEntityDecode,t:jsDecode,deny,msg:'Request contains /flag'"

  
  

# Additional rules to catch obfuscations and fragments

SecRule ARGS "@contains /flag" "id:1000,phase:2,t:lowercase,t:urlDecodeUni,t:htmlEntityDecode,t:jsDecode,deny,msg:'Request contains /flag'"

SecRule ARGS "@contains /f/l/a/g" "id:10080,phase:2,t:lowercase,t:urlDecodeUni,t:htmlEntityDecode,t:jsDecode,deny,msg:'Request contains fragmented /flag'"

SecRule ARGS "@contains /f%2Fl%2Fa%2Fg" "id:10090,phase:2,t:lowercase,t:urlDecodeUni,t:htmlEntityDecode,t:jsDecode,deny,msg:'Request contains encoded /flag'"

  
  
  

# Detect and block XSS attacks

SecRule ARGS "@rx <script>" "id:10011,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx onerror=" "id:10021,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx javascript:" "id:10031,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx alert\(" "id:10041,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx eval\(" "id:10051,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx document\.cookie" "id:10061,phase:2,deny,status:403,msg:'XSS attack detected',log"

SecRule ARGS "@rx window\.location" "id:10071,phase:2,deny,status:403,msg:'XSS attack detected',log"

  

# Detect and block SQL injection attacks

SecRule ARGS "@rx (select|union|insert|update|delete|drop|alter|create|exec|execute|--|#|;|')" \

"id:10012,phase:2,deny,status:403,msg:'SQL Injection detected',log"

  

SecRule REQUEST_URI "@rx (select|union|insert|update|delete|drop|alter|create|exec|execute|--|#|;|')" \

"id:10022,phase:2,deny,status:403,msg:'SQL Injection detected in URI',log"

  

SecRule REQUEST_HEADERS:User-Agent "@rx (sqlmap|nmap|nikto|nessus)" \

"id:10032,phase:1,deny,status:403,msg:'SQL Injection tool detected',log"
```