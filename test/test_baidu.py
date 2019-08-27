"""
轻量级自动化测试框架
2019.7.20：完成test_baidu测试流程
2019.7.22更新：添加utils-file_reader的yml配置模块;utils-log日志模块
2019.7.24更新：添加util-file_reader的excel配置模块;untils-HTMLTestRunner测试报告模块;utils-mail邮件发送模块
2019.7.25更新：添加utils-client接口层；utils-generator数据生成器
"""
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email

import json

class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL_BaiDu')
    excel = DATA_PATH + r'\baidu.xlsx'
    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//*[@id="content_left"]')
    #不要用unittest自带的setup，不然会在最开始多启动一次浏览器
    def sub_setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)

    def sub_tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        datas = ExcelReader(self.excel).data
        print(datas)
        for d in datas:
            with self.subTest(data=d):
                self.sub_setup()
                driver = self.driver
                driver.find_element(*self.locator_kw).send_keys(d['search'])
                driver.find_element(*self.locator_su).click()
                time.sleep(2)
                links = driver.find_element(*self.locator_result).text
                logger.info(links)
                self.sub_tearDown()


if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    print(report)
    with open(report,'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='轻量级测试框架-百度测试',description='百度用例')
        #必须用unittest.main   否则无法生成报告
        runner.run(TestBaiDu('test_search_0'))
        e = Email(title='百度搜索测试报告',
                  message='这是今天的测试报告，请查收！',
                  receiver='773858927@qq.com',
                  server='smtp.qq.com',
                  sender='773858927@qq.com',
                  password='hxmsxbafdhdqbceg',
                  path=report
                  )
        e.send()
        unittest.main(runner)