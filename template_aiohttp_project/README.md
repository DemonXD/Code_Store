### 一个基于SQLite、aiohttp和Sqlanchemy的简单webserver
Features：
- 简单的restful api接口
- 简单的首页内容展示
- 基于websocket的后段持续推送信息
- 数据库连接(SQLite/PostgreSQL)
- 自动创建数据库表(暂不支持migrate)
    - models中不要创建和数据库表无关的类(后期优化自动识别的条件)
- Shell 功能，所有app下的model模型导入目前还有问题
- startapp命令(创建新的app)
- aiohttp_session 支持session

TODO:
- 完善Shell功能
- 支持migrate，表字段结构更改，自动同步到数据库

项目结构：
```
.
├── README.md
├── aiohttp_example
│   ├── web_ws.py
│   └── websocket.html
├── apps
│   ├── __init__.py
│   ├── baseapp
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   └── secondapp
│       ├── __init__.py
│       └── models.py
├── db.py
├── manager.py                  # 项目主入口
├── migrations                  # 迁移功能未完成
├── requirements.txt
├── settings.py                 # 配置文件
├── templates
│   └── index.html              # example主页
└── utils
    ├── __init__.py
    ├── ackdict.py
    ├── async_sqlite.py
    ├── mqtt_subscriber.py
    ├── normal_utils.py
    └── signalSlotPattern.py

```

### 使用说明
- 配置`settings.py`中的`DB_BACKEND`，目前支持`sqlite/PostgreSQL`
- 配置`INSTALL_APPS`中加上创建的app包路径,例如`apps.baseapp`
- 执行项目前初始化db，`python manager.py init db`
- 执行`python manager.py shell`，进入shell模式，并自动导入model模型(待完善)
- 执行`python manager.py runserver` 开启服务
- 打开浏览器，输入http://127.0.0.1:10086

