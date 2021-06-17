# 检测指定版本的docker 镜像是否存在
if [[ "$(docker images -q docker.elastic.co/elasticsearch/elasticsearch:7.3.2 2> /dev/null)" == "" ]]; then
        docker pull docker.elastic.co/elasticsearch/elasticsearch:7.3.2
fi
# 启动es镜像，加上--rm，可以在推出镜像的时候，自动关闭容器
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.3.2;
