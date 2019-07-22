import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config,DRIVER_PATH
from utils.log import logger
import json

class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//*[@id="content_left"]')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        driver = self.driver
        driver.find_element(*self.locator_kw).send_keys('selenium灰蓝')
        driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = driver.find_element(*self.locator_result).text
        logger.info(links)



if __name__ == '__main__':
    unittest.main()