import requests


url = 'http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=&city=0&yys=0&port=1&pack=19337&ts=0&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions='
resp = requests.get(url)
print(resp.content.decode())
