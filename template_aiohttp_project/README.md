### 一个基于SQLite、aiohttp和Sqlanchemy的简单webserver
Features：
- 简单的restful api接口
- 简单的首页内容展示
- 基于websocket的后段持续推送信息

项目结构：
```
├── README.md
├── aiohttp_example
│   ├── web_ws.py
│   └── websocket.html
├── db.py                   # 数据库连接
├── main.py                 # 项目主入口
├── models.py               # ORM模型
├── requirements.txt
├── signalSlotPattern.py
├── templates
│   └── index.html          # 主页html文件
├── test.db                 # SQLite数据库文件
├── urls.py                 # 路由注册
├── utils.py                # 工具库
└── views.py                # 视图逻辑
```

### 使用说明
- `pip install -r requirements.txt`
- `python main.py`
- 打开浏览器，输入http://127.0.0.1:10086