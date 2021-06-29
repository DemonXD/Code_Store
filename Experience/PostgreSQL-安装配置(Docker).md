**新建本地数据存储文件夹**

`mkdir -p /path/to/postgres-data`

**运行：**

```shell
docker run -d \
    --name dev-postgres \
    -e POSTGRES_PASSWORD=Pass2020! \
    -v /path/to/postgres-data/:/var/lib/postgresql/data \
    -p 5432:5432
    postgres:latest
```

登陆的账号密码：

> account: postgres
> 
> password: Pass2020!

**使用带PGAdmin的镜像：**

`docker pull dpage/pgadmin4`

**运行：**

```shell
docker run \ 
    -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=user@domain.local' \
    -e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' \
    --name dev-pgadmin \ 
    -d dpage/pgadmin4
```