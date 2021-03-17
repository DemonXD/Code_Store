### 说明
1. 更改nginx.conf配置文件
2. 检查配置文件 /path/to/openresty -t 
3. 启动 /path/to/openresty -s reload
    - 如果报错 nginx.pid ""，则使用-c参数重启:
        - /path/to/openresty -c /path/to/nginx.conf