聚集集合查询

1、查询所有记录  
引用块内容  
db.people.find();  
相当于：select\* from people;

2、查询去掉后的当前聚集集合中的某列的重复数据  
db.people.distinct(&quot;name&quot;);  
相当于：select distict name from people;

3、查询age = 18的记录  
db.people.find({&quot;age&quot;: 18});  
相当于： select \* from people where age = 18;

4、查询age &gt; 18的记录  
db.people.find({age: {$gt: 18}});  
相当于：select \* from people where age &gt;18;

5、查询age &lt; 18的记录  
db.people.find({age: {$lt: 18}});  
相当于：select \* from people where age &lt;18;

6、查询age &gt;= 18的记录  
db.people.find({age: {$gte: 18}});  
相当于：select \* from people where age &gt;= 18;

7、查询age &lt;= 18的记录  
db.people.find({age: {$lte: 18}});

8、查询age &gt;= 23 并且 age &lt;= 26  
db.people.find({age: {$gte: 23, $lte: 26}});

9、查询name中包含 mongo的数据  
db.people.find({name: /mongo/});  
相当于：select \* from people where name like &#39;%mongo%&#39;;

10、查询name中以mongo开头的  
db.people.find({name: /^mongo/});

相当于：select \* from people where name like ‘mongo%’;  
11、查询指定列name、age数据  
db.people.find({}, {name: 1, age: 1});

相当于：select name, age from people;  
当然name也可以用true或false,当用ture的情况下河name:1效果一样，如果用false就是排除name，显示name以外的列信息。  
12、查询指定列name、age数据, age &gt; 18  
db.people.find({age: {$gt: 18}}, {name: 1, age: 1});  
相当于：select name, age from people where age &gt;18;

13、按照年龄排序  
升序：db.people.find().sort({age: 1});  
降序：db.people.find().sort({age: -1});

14、查询name = zhangsan, age = 18的数据  
db.people.find({name: &#39;zhangsan&#39;, age: 18});  
相当于：select \* from people where name = &#39;zhangsan&#39; and age = &#39;18&#39;;

15、查询前5条数据  
db.people.find().limit(5);  
相当于：select \* from people Limit 5;

16、查询10条以后的数据  
db.people.find().skip(10);  
相当于：select \* from people where id not in (select id from people limit 10);

17、查询在5-10之间的数据  
db.people.find().limit(10).skip(5);  
可用于分页，limit是pageSize，skip是第几页\*pageSize

18、or与查询  
db.people.find({$or: \[{age: 18}, {age: 18}\]});  
相当于：select \* from people where age = 18 or age = 18;

19、查询第一条数据  
db.people.findOne();  
相当于：select \* from people limit 1;  
db.people.find().limit(1);

20、查询某个结果集的记录条数  
db.people.find({age: {$gte: 18}}).count();  
相当于：select count(\*) from people where age &gt;= 20;

21、求总数  
db.people.find({sex: {$exists: true}}).count();  
相当于：select count(sex) from people;

###