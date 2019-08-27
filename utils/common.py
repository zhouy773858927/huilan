from selenium import webdriver
from utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
import time
from utils.log import logger
from selenium.webdriver.common.action_chains import ActionChains
import xlwt


# 登录
def login(self):
    driver = self.driver
    driver.find_element_by_id("userName").send_keys("zhouyang")
    driver.find_element_by_id("password").send_keys("787201")
    driver.find_element_by_id("captcha").send_keys("88")
    driver.find_element_by_xpath('//*[@id="loginForm"]/button').submit()
    time.sleep(2)


def achieve(self):
    pass









