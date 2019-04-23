# 简单RPC框架

### 项目介绍

通过rabbitmq实现一个简单的远程过程调用框架

### 整体结构


* control_multi_rpc：客户端的包装入口,场景中使用到远程调用则用此模块的包装方法即可；

* multi_rpc_client：客户端主要逻辑src；

* multi_rpc_server：服务端的主要逻辑 其中调用函数请使用者自行封装到单独模块并引入到服务端中。



### 使用

```
>>> python multi_rpc_server.py
```

启动服务端  同时在调用端引入control_multi_rpc里面的方法即可
注意要部署rabbitMQ到任意位置的服务器都可以 配好参数  并使rpc服务端、客户端正确配置mq主机地址



###  小小demo enjoy it~
