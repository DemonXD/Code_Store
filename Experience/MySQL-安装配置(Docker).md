**新建数据库文件夹及配置文件：**

`mkdir -p /path/to/mysql/mysql-data`

`mkdir -p /path/to/mysql/conf`

`mkdir -p /path/to/mysql/logs`

**拉取镜像：**

`docker pull mysql:5.7`

**配置文件：**

```ini
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
#log-error      = /var/log/mysql/error.log
# By default we only accept connections from localhost
#bind-address   = 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
```

**运行：**

```shell
docker run -d \
    -p 3306:3306 \
    --name mysql \
    -v /path/to/mysql/conf:/etc/mysql/conf.d \
    -v /path/to/mysql/logs:/var/log/mysql \
    -v /path/to/mysql/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=123456 \
    mysql:5.7 \
    --character-set-server=utf8mb4 \
    --collation-server=utf8mb4_unicode_ci
```

默认登录账号密码：root/123456

**备份数据：**

```shell
docker exec mysql sh -c ' exec mysqldump --all-databases -uroot -p"123456" ' > /mydocker/mysql/all-databases.sql
```