import pika
import json


class Feibinacci_client(object):

    def __init__(self, user, passwd, virtualhost, host="localhost"):
        self.connection = pika.BlockingConnection(
            pika.URLParameters('amqp://{u}:{p}@{h}:5672{v}'.format(u=user, p=passwd, v=virtualhost, h=host)))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.callback_queue, self.on_response, auto_ack=False)
        # 请求id结果映射表
        self._req_id_result_map = {}
        # 请求id列表
        self.req_id_list = []

    # 根据请求id获取结果的方法
    def get_request_result(self, req_id):
        rst = self._req_id_result_map.get(req_id, None)
        del self._req_id_result_map[req_id]
        return rst

    def on_response(self, chan, method, props, body):
        for corr_id in self.req_id_list:
            if corr_id == props.correlation_id:
                self._req_id_result_map[corr_id] = body.decode()

    def call(self, req_id, fn, param):
        """
        :param req_id:str 远程调用请求id  要求唯一
        :param fn:str  远程调用函数名 要求远端必须有同名函数
        :param param:list 远程调用参数 限制列表长度为2  第一个元素代表位置参数的列表 无参数传空列表 第二个元素为具名参数的字典
                      没有则传空字典   远端调用类似  fn(*param[0], **param[1])
        :return:
        """
        self.req_id_list.append(req_id)
        # self.corr_id = str(uuid.uuid4())
        # eval("self.{} = None".format(self.corr_id))
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=req_id),
                                   body=json.dumps([fn, param]))
        while not self._req_id_result_map.get(req_id, None):
            self.connection.process_data_events()
        return self.get_request_result(req_id)


febonacci_rpc = Feibinacci_client("user", "passwd", virtualhost="/vertualhost")

