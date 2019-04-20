# Mongodb数据库
NAME = 'proxy'
TABLE = 'proxy'
HOST = 'localhost'
PORT = 27017

# 供测试的url
HTTP_TEST_URL = 'http://mini.eastday.com/assets/v1/js/search_word.js'
HTTPS_TEST_URL = 'https://t1.chei.com.cn/common/wap/js/wap.min.js'

# Pool 的低阈值和高阈值
POOL_LOWER_THRESHOLD = 3
POOL_UPPER_THRESHOLD = 5

# 两个调度进程的周期
VALID_CHECK_CYCLE = 300
POOL_LEN_CHECK_CYCLE = 10
