**默认拉的是latest的版本**

`docker pull mongo`

**启动：**

```shell
docker run -d \
    --name mongodb 
    -p 27037:27037 \
    mongo:latest
```

`mongodb.conf:`

```shell
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
storage:
  dbPath: /data/db
net:
  port: 27037
  bindIp: 0.0.0.0
#security:
  #authorization: enabled
```

**指定MongoDB配置文件**

当我们需要修改配置文件时，我们只需要在宿主机上创建一个mongodb.conf文件，并将该文件所在的文件夹映射到容器的/data/configdb文件夹中，同时，在容器的启动命令中添加--configsvr参数即可。

```shell
docker run -d \
    --name some-mongo \
    -v /path/to/mongodb.conf:/data/configdb/mongodb.conf
    mongo --configsvr
```

**使用如下命令进入mongo的admin用户**

`docker exec -it mongodb mongo admin`

**进入容器添加用户：**

```shell
docker exec -it ly-mongo mongo admin

db.createUser({user:"root",pwd:"root",roles:[{role:'root',db:'admin'}]})   //创建用户,此用户创建成功,则后续操作都需要用户认证
exit
```

**使用认证进行mongo的登录：**

`docker run --name mongodb -d mongo:latest --auth`

**挂载数据：**

`docker run --name mongodb -v /my/own/datadir:/data/db -d mongo:latest`

**备份数据：**

```shell
docker exec mongo sh -c \
	'exec var=`date +%Y%m%d%H%M` && mongodump -h localhost --port 27017 -u test -p test1 -d dbname -o /data/backup/$var_test1.dat'
```

**挂载备份数据：**

`docker run --name mongodb -v /mnt/mongo/backup:/data/backup -d mongo:latest`

**推荐用法及过程：**

```shell
docker pull mongo
创建Mongo专用的文件夹：

cd /mnt
mkdir mongodb
cd ./mongodb
mkdir data
mkdir backup
执行如下命令启动MongoDB：

docker run --name mongodb -p 27017:27017 -v /mnt/mongodb/data:/data/db -v /mnt/mongodb/backup:/data/backup -d mongo:latest --auth
接下来，我们需要进入容器的命令行去创建用户名和密码：

docker exec -it mongo mongo admin
db.createUser({ user: 'jsmith', pwd: 'password', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
use test;
db.createUser({user:"testuser",pwd:"testpass",roles:["readWrite"]});
db.auth("testuser","testpass")
在运行一段时间以后，我们可以执行如下命令进行数据库备份：

docker exec mongo sh -c 'exec var=`date +%Y%m%d%H%M` && mongodump -h localhost --port 27017 -u jsmith -p password -d dbname -o /data/backup/$var_test1.dat'
```