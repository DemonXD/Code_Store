## **系统环境**

*   至少需要三台虚拟机或者物理机，这里使用虚拟机
*   每台虚拟机至少需要两块硬盘（一块系统盘，一块OSD），本例中有三块硬盘

### **1\. 部署流程**

博客使用的markdown解析器不支持流程图使用图片代替

<figure class="image op-uc-figure" style="width:50%;"><div class="op-uc-figure--content"><img class="op-uc-image" src="/api/v3/attachments/75/content"></div></figure>

### **2\. 主机规划**

<figure class="image op-uc-figure" style="width:50%;"><div class="op-uc-figure--content"><img class="op-uc-image" src="/api/v3/attachments/76/content"></div></figure>

## **启动 MON**

### **1\. 下载 ceph daemon 镜像**

`docker pull ceph/daemon`

### **2\. 启动第一个 mon**

在 node1 上启动第一个 mon,注意修改 MON\_IP

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -e MON_IP=192.168.3.123 \
    -e CEPH_PUBLIC_NETWORK=192.168.3.0/24 \
    ceph/daemon mon
```

查看容器

`docker ps`

查看集群状态

`docker exec img-id ceph -s`

### **2\. 复制配置文件**

将 node1 上的配置文件复制到 node02 和 node03,复制的路径包含/etc/ceph和/var/lib/ceph/bootstrap-\*下的所有内容。

```shell
# ssh root@node2 mkdir -p /var/lib/ceph
# scp -r /etc/ceph root@node2:/etc
# scp -r /var/lib/ceph/bootstrap* root@node2:/var/lib/ceph

# ssh root@node3 mkdir -p /var/lib/ceph
# scp -r /etc/ceph root@node3:/etc
# scp -r /var/lib/ceph/bootstrap* root@node3:/var/lib/ceph
```

### **3\. 启动第二个和第三个 mon**

在 node02 上执行以下命令启动 mon,注意修改 MON\_IP

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -e MON_IP=192.168.3.124 \
    -e CEPH_PUBLIC_NETWORK=192.168.3.0/24 \
    ceph/daemon mon
```

在 node03 上执行以下命令启动 mon,注意修改 MON\_IP

复制

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -e MON_IP=192.168.3.125 \
    -e CEPH_PUBLIC_NETWORK=192.168.3.0/24 \
    ceph/daemon mon
```

查看在 node01 上集群状态

`docker exec img-id ceph -s`

可以看到三个 mon 已经正确启动

## **启动 OSD**

每台虚拟机准备了两块磁盘作为 osd,分别加入到集群,注意修改磁盘

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -v /dev/:/dev/ \
    --privileged=true \
    -e OSD_FORCE_ZAP=1 \
    -e OSD_DEVICE=/dev/sdb \
    ceph/daemon osd_ceph_disk
```

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -v /dev/:/dev/ \
    --privileged=true \
    -e OSD_FORCE_ZAP=1 \
    -e OSD_DEVICE=/dev/sdc \
    ceph/daemon osd_ceph_disk
```

按照同样方法将 node02 和 node03 的 sdb、sdc 都加入集群

查看集群状态

`docker exec img-id ceph -s`

可以看到 mon 和 osd 都已经正确配置，切集群状态为 HEALTH\_OK

## **创建 MDS**

使用以下命令在 node01 上启动 mds

```shell
docker run -d \
    --net=host \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    -e CEPHFS_CREATE=1 \
    ceph/daemon mds
```

## **启动 RGW ,并且映射 80 端口**

使用以下命令在 node01 上启动 rgw，并绑定 80 端口

```shell
docker run -d \
    -p 80:80 \
    -v /etc/ceph:/etc/ceph \
    -v /var/lib/ceph/:/var/lib/ceph/ \
    ceph/daemon rgw
```

## **集群的最终状态**

`docker exec img-id ceph -s`