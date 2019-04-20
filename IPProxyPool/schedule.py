import time
from multiprocessing import Process
from config import *
from db import MongodbClient
from adder import PoolAdder
from tester import ProxyTester


class Schedule(object):

    def valid_proxy(self, cycle=VALID_CHECK_CYCLE):
        """
        从数据库中拿到2/3半代理进行检查
        """
        conn = MongodbClient()
        tester = ProxyTester()
        while True:
            print('Refreshing ip...')
            count = int(5 * conn.get_nums/6)
            if count == 0:
                print('Waiting for adding...')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    def check_pool(self, lower_threshold=POOL_LOWER_THRESHOLD,
                upper_threshold=POOL_UPPER_THRESHOLD,
                cycle=POOL_LEN_CHECK_CYCLE):
        """
        如果代理数量少于最低阈值，添加代理
        """
        conn = MongodbClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if max(conn.get_count) <= lower_threshold:
                adder.add_to_pool()
            time.sleep(cycle)

    def run(self):
        print('Ip Processing running...')
        valid_thread = Process(target=self.valid_proxy)
        check_thread = Process(target=self.check_pool)
        valid_thread.start()
        check_thread.start()
