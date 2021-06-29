**创建挂载目录**

`mkdir -p /mydata/elasticsearch/config`

`mkdir -p /mydata/elasticsearch/data`

**创建配置文件**

`echo "http.host: 0.0.0.0" >> /mydata/elasticsearch/config/elasticsearch.yml`

**配置跨域**

`echo "http.cors.enabled: true" >> /mydata/elasticsearch/config/elasticsearch.yml`

`echo 'http.cors.allow-origin: "*"' >> /mydata/elasticsearch/config/elasticsearch.yml`

```shell
docker run \
	--name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
    -v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
    -v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
    -v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
    -d elasticsearch:6.7.2
```

其中elasticsearch.yml是挂载的配置文件，data是挂载的数据，plugins是es的插件，如ik，而数据挂载需要权限，需要设置data文件的权限为可读可写,需要下边的指令。

chmod -R 777 要修改的路径 -e &quot;discovery.type=single-node&quot; 设置为单节点

特别注意： -e ES\_JAVA\_OPTS=&quot;-Xms256m -Xmx256m&quot; \\ 测试环境下，设置ES的初始内存和最大内存，否则导致过大启动不了ES

  

### 配置Kibana

kibana需要匹配对应版本的elasticsearch，6.7.x &lt;-&gt; 6.7.x

`docker run --name kibana --link=elasticsearch:test -p 5601:5601 -d kibana:6.7.2`

**注意：**

如果elasticsearch的--name 名称不是elasticsearch 的话，需要进入kimanba的config/kibana.yml将：

`elasticsearch.hosts: [ "http://{--name 名称}:9200" ]`