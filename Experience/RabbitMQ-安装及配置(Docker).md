**Docker 拉取镜像**

**带有web管理界面的镜像**

`docker pull docker.io/rabbitmq:3.8-management`

**运行：**

```shell
docker run -d \
    --name rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    -v /mq/data:/var/lib/rabbitmq \
    --hostname myRabbit \
    -e RABBITMQ_DEFAULT_VHOST=my_vhost  \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=admin \
    rabbitmq:3.8-management
```

> \-d 后台运行容器；  
> –name 指定容器名；  
> \-p 指定服务运行的端口（5672：应用访问端口；15672：控制台Web端口号）；  
> \-v 映射目录或文件；  
> –hostname 主机名（RabbitMQ的一个重要注意事项是它根据所谓的 “节点名称” 存储数据，默认为主机名）；  
> \-e 指定环境变量；（RABBITMQ\_DEFAULT\_VHOST：默认虚拟机名；RABBITMQ\_DEFAULT\_USER：默认的用户名；RABBITMQ\_DEFAULT\_PASS：默认用户名的密码）