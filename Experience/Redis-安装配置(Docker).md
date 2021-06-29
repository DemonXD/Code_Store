**新建本地配置文件、数据目录**

`mkdir -p /path/to/redis/conf`

`mkdir -p /path/to/redis/data`

**新建配置文件 touch /path/to/redis/conf/redis.conf**

```shell
#bind 127.0.0.1 
protected-mode no
appendonly yes 
requirepass 123456 
```

> *   将bind 127.0.0.1注释掉，保证可以从远程访问到该Redis，不单单是从本地
> *   appendonly：开启数据持久化到磁盘，由于开启了磁盘映射，数据最终将落到`/path/to/redis/data`目录下
> *   requirepass：设置访问密码为123456

**启动**

```shell
docker run -d \
    --name myredis \
    -p 6379:6379 \
    -v /path/to/redis/data:/data \
    -v /path/to/redis/conf/redis.conf:/etc/redis/redis.conf \
    redis:latest \
    redis-server /etc/redis/redis.conf 
```