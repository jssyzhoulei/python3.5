# coding=utf-8
import asyncio
import aiohttp
import requests
from requests.exceptions import ConnectionError
import smtplib
from email.mime.text import MIMEText


class QQMailClient(object):
    """使用qq邮箱发送邮件"""
    send_adr = 'youremail@yourdomain'
    pas = 'Xhlc@123'

    def __init__(self):
        """
        :param msg_from: 发件人邮箱地址
        :param passwd: 发件人邮箱密码,qq邮箱使用授权码是16个字母，而不是自己的邮箱密码。
        """
        self._msg_from = self.send_adr
        self._passwd = self.pas
        self._smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        self.__login()

    def __login(self):
        self._smtp.login(self._msg_from, self._passwd)

    def send_mail(self, subject, content):
        """
        发送邮件
        :param msg_to: 收件人邮箱地址
        :param subject :邮件主题
        :param content:邮件内容
        :type msg_to:str
        :type subject:str
        :type content:str
        """
        msg = MIMEText(content, _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = self._msg_from
        msg['To'] = self._msg_from
        self._smtp.sendmail(self._msg_from, self._msg_from, msg.as_string())


def parse_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return None
    except ConnectionError:
        print('Error.')
    return None


class Downloader(object):
    """
    python3.5的标准库自带的async和await指令，
    相当于3.5之前的 @asyncio.coroutine和yield from
    提供异步抓取
    """
    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls
