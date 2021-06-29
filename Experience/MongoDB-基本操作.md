查询指定字段，并按照创建时间降序排列(column: 1,为需要匹配，column: 0 为不需要匹配)  
db.collections.find({}, {column\_1:1, column\_2:1, ..., \_id:0}).sort({createtime:-1});

命令行登录

`mongo -u[uname] -p --authenticationDatabase`  
`mongo -u[uname] -p[pwd] --authenticationDatabase`

查询所有库  
`show dbs;`

查询库中的连接  
`show collecitons;`

创建数据库/切换数据库  
`use test1;`

如果没有test1这个库，会创建

删除数据库  
`db.dropDatabase();`

获取数据库名称  
`db.getName();`

获取数据库状态  
`db.stats();`

当前db版本  
`db.version();`

查看当前db的链接机器地址  
`db.getMongo();`

从指定主机上克隆数据库  
`db.cloneDatabase("127.0.0.1");`

从指定的机器上复制指定数据库数据到某个数据库  
`db.copyDatabase("yhb", "test1", "127.0.0.1");`

修复数据库  
`db.repairDatabase();`

在MongoDB中频繁的进行数据增删改时，如果记录变了，例如数据大小发生了变化，这时候容易产生一些数据碎片，出现碎片引发的结果，  
一个是索引会出现性能问题，另外一个就是在一定的时间后，所占空间会莫明其妙地增大，所以要定期把数据库做修复，定期重新做索引，这样会提升MongoDB的稳定性和效率

**MongoDB集合操作**

1、创建一个聚集集合（table）  
//指定数据库大小size，最大存放100个文档，满了，就会mongodb 会删除旧文档。  
db.createCollection(&quot;human&quot;,{&quot;size&quot;:1024,capped:true,max:100});  
db.createCollection(&quot;people&quot;);

2、查看集合状态  
db.people.stats();

3、获取指定集合  
db.getCollection(&quot;human&quot;);

4、获取当前db中的所有集合  
db.getCollectionNames();

和show collections类似  
5、显示当前db所有聚集索引的状态  
db.printCollectionStats();

**MongoBD用户操作**

1、添加一个用户  
db.createUser({user:&quot;zs&quot;,pwd:&quot;111&quot;,roles:\[&quot;read&quot;\]})  
添加用户、设置密码、是否只读

2、数据库认证、安全模式  
db.auth(“zs”, “111”);

3、显示当前所有用户，角色  
show people;  
show roles;

4、删除用户  
db.removeUser(&quot;zs&quot;);

**集合数据操作**

1、添加  
db.people.save({name: &#39;zhangsan&#39;, age: 18, sex: true});  
添加的数据的数据列，没有固定，根据添加的数据为准

2、修改  
db.people.update({age: 18}, {$set: {name: &#39;changeName&#39;}}, false, true);  
相当于：update people set name = &#39;changeName&#39; where age = 18;  
db.people.update({name: &#39;zhangs&#39;}, {$inc: {age: 12}}, false, true);  
相当于：update people set age = age + 12 where name = &#39;zhangs&#39;;  
db.people.update({name: &#39;zhangs&#39;}, {$inc: {age: 12}, $set: {name: &#39;hoho&#39;}}, false, true);  
相当于：update people set age = age + 12, name = &#39;hoho&#39; where name = &#39;zhangs&#39;;

3、删除  
db.people.remove({age: 12});