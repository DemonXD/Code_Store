指定域名：gitlab.test.com
1. 拉取镜像
```Shell
sudo docker pull gitlab/gitlab-ce
```
2. 配置本地持久化目录，分别存储配置文件，日志以及数据
```Shell
mkdir -p /path/to/gitlab/{conf,logs,data}
```
3. 启动：
```Shell
sudo docker run -d \
	-p 5001:80 \
	-p 9022:22 \
	-p 9443:443\
	--name gitlab \
	--restart always \
	--volume /path/to/gitlab/conf:/etc/gitlab \
	--volume /path/to/gitlab/logs:/var/log/gitlab \
	--volume /path/to/gitlab/data:/var/opt/gitlab \
	gitlab/gitlab-ce:latest

# 这里指定本地5001端口代理docker的80端口
```
Tips: 可以使用`sudo docker ps`查看gitlab启动情况，如果看到health：healthy表示启动完成
4. 修改配置文件  
使用如下命令进入docker镜像内：`sudo docker exec -it gitlab /bin/bash`  
然后`vi /etc/gitlab/gitlab.rb`打开配置文件，修改如下配置项
```Shell
# external_url 为对外展示的 HTTP 地址，包括 HTTP 方式的克隆地址和仓库文件的跳转链接中的域名。
# 这个地址可以携带端口，可以使用 IP 也可以使用域名，无论你 GitLab 服务前端还有没有设置反向代理来做域名解析，这里只需要是你最终需要展示在 GitLab 页面里的 HTTP 链接即可。
# 因为我们这里 GitLab 是部署在公司本地局域网的，所以直接写这台机器的局域网 IP 和 端口号就可以了。
external_url 'http://192.168.31.43:9080'
# 更改为上海时区，按照自己的时区可以进行相关更改
gitlab_rails['time_zone'] = 'Asia/Shanghai'
# 禁止用户创建项目组
gitlab_rails['gitlab_default_can_create_group'] = false
```
更改完成后使用`gitlab-ctl reconfigure`命令重新加载配置

5. 关闭公开注册
点击左上角标签，依次进入`Admin->Settings->General`，在右侧`Sign-up restrictions`中取消勾选`Sign-up enabled`点击保存

