import pika
import json


# from  依赖 import *   <---  把服务端要执行的函数引入到当前模块以供调用

def fib(n):
    n = int(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fib2(n, k=3):
    return "sadasdsasdadsa"+str(n)+str(k)


def on_request(ch, method, props, body):
    fn, param = json.loads(body.decode())
    print(" [.] fib(%s)" % (param,))
    if not (isinstance(param, list) and len(param) == 2 and isinstance(param[0], list) and isinstance(param[1], dict)):
        response = "error params please use like this fn(*param[0], **param[1])"
    else:
        try:
            fn = eval(fn)
            response = fn(*param[0], **param[1])
        except:
            response = "remote has not function like {}".format(fn)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def rabbit_rpc_server(user, passwd, virtualhost, host="localhost"):

    parameters = pika.URLParameters('amqp://{u}:{p}@{h}:5672{v}'.format(u=user, p=passwd, v=virtualhost, h=host))
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('rpc_queue', on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
    connection.close()


if __name__ == '__main__':
    print("rpc server start...")
    rabbit_rpc_server("user", "passwd", virtualhost="/vertualhost")
