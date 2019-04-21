# IP代理池

### 项目介绍

本项目通过芝麻接口获取长效代理并维护到mongo中做持久化

### 代理池设计


* Mongodb：Mongodb数据库存放抓取并且有效的代理，如需扩展，结合对应数据库api；

* Schedule：计划任务，芝麻接口调用的启动，添加代理，测试代理，定时检测代理；

* Api：代理池的外部接口，利用`flask`简单实现。



### 使用

```
>>> python run.py
```

启动成功，打开浏览器，127.0.0.1:5000查看。

爬虫中获取代理：

```Python
import requests

def get_proxy():
    resp = requests.get('http://127.0.0.1:5000/get')
    proxy = resp.text
    ip = 'http://' + proxy
    return ip
```

### 付费代理异步持久化可以参考一下
