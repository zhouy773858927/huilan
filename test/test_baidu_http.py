import unittest
from utils.config import Config,REPORT_PATH
from utils.client import HttpClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner

class TestBaiDuHTTP(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.client = HttpClient(url=self.URL, method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        self.assertIn('百度一下，你就知道',res.text)

if __name__ == '__main__':
    report = REPORT_PATH+r'\report_http.html'
    with open(report,'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='轻量级自动化框架接口层',description='百度接口报告')
        runner.run(TestBaiDuHTTP("test_baidu_http"))
        unittest.main(runner)