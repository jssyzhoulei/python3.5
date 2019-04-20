import asyncio
import time
import aiohttp
import random
import requests
from config import HTTP_TEST_URL, HTTPS_TEST_URL
from db import MongodbClient


class ProxyTester(object):

    def __init__(self):
        self._raw_proxies = None

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = MongodbClient()

    async def test_single_proxy(self, proxy):
        """
        测试一个代理，如果有效，将他放入usable-proxies
        """
        scheme = 'http://'
        test_url = HTTPS_TEST_URL
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        real_proxy = scheme + proxy
        async def test_proxy(https=True):
            name = 'https' if https else 'http'
            async with session.get(test_url, proxy=real_proxy, timeout=10) as response:
                if response.status == 200 or response.status == 429:
                    self._conn.put(proxy, https)
                    print('Valid {} proxy'.format(name), proxy)
                else:
                    print('Invalid {} status'.format(name), response.status, proxy)
                    self._conn.delete(proxy)

        try:
            async with aiohttp.ClientSession() as session:
                try:
                    await test_proxy()
                except:
                    try:
                        test_url = HTTP_TEST_URL
                        await test_proxy(False)
                    except Exception as e:
                        self._conn.delete(proxy)
                        print('Invalid proxy', proxy, e)
                        # print('session error', e)
        except Exception as e:
            print(e)

    def test(self):
        """
        异步测试所有代理
        """
        print('Tester is working...')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError as e:
            time_format = '%Y-%m-%d %H:%M:%S'
            format_t = time.strftime(time_format)
            print(format_t, 'Async Error:', e)
