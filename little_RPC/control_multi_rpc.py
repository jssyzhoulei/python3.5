from multi_rpc_client import febonacci_rpc
import time
import uuid


def test_rpc():
    print("[x] Requesting funtion(param)")
    response = febonacci_rpc.call(str(123456), "fib", [[str(30)], {}])
    print("[.] Got %r" % (response,))
    time.sleep(3)
    response = febonacci_rpc.call(str(123459), "fib2", [[str(32)], {"k": 999}])
    print("[.] Got %r" % (response,))


def call_single(fn, param):
    # 单个远程过程调用
    _id = str(uuid.uuid4())
    print("[x] Requesting {}(*{}, **{})".format(fn, param[0], param[1]))
    response = febonacci_rpc.call(_id, fn, param)
    print("[.] Got %r" % (response,))


def call_many(fn_param_list):
    # 多个远程过程调用
    for fn, param in fn_param_list:
        call_single(fn, param)


if __name__ == '__main__':
    call_many([("fib", [[str(30)], {}]), ("fib2", [[str(32)], {"k": 999}])])