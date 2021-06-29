if \[\[ &quot;$(docker images -q docker.elastic.co/elasticsearch/elasticsearch:7.3.2 2&gt; /dev/null)&quot; == &quot;&quot; \]\]; then  
       docker pull docker.elastic.co/elasticsearch/elasticsearch:7.3.2  
fi  
docker run -p 9200:9200 -p 9300:9300 -e &quot;discovery.type=single-node&quot; docker.elastic.co/elasticsearch/elasticsearch:7.3.2;