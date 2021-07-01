## 快速入门

本文介绍如何快速使用OSS Python SDK完成常见操作，如创建存储空间（Bucket）、上传和下载文件（Object）等。

### 创建存储空间
存储空间是OSS的全局命名空间，相当于数据的容器，可以存储若干文件。 以下代码用于创建存储空间：
```Python
# -*- coding: utf-8 -*-
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')

# 设置存储空间为私有读写权限。
bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
```    
存储空间的命名规范详情请参见基本概念中的命名规范。创建存储空间详情请参见创建存储空间。

获取endpoint详情请参见访问域名和数据中心文档。

### 上传文件
以下代码用于上传文件至OSS：
```Python
# -*- coding: utf-8 -*-
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')

# <yourObjectName>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
# <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
bucket.put_object_from_file('<yourObjectName>', '<yourLocalFile>')
```
### 下载文件
以下代码用于将指定的OSS文件下载到本地文件：
```Python
# -*- coding: utf-8 -*-
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
# <yourObjectName>从OSS下载文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
# <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
bucket.get_object_to_file('<yourObjectName>', '<yourLocalFile>')
```
### 列举文件
以下代码用于列举指定存储空间下的10个文件：
```Python
# -*- coding: utf-8 -*-
import oss2
from itertools import islice

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')

# oss2.ObjectIterator用于遍历文件。
for b in islice(oss2.ObjectIterator(bucket), 10):
    print(b.key)
```
### 删除文件
以下代码用于删除指定文件：
```Python
# -*- coding: utf-8 -*-
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')

# <yourObjectName>表示删除OSS文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
bucket.delete_object('<yourObjectName>')
```