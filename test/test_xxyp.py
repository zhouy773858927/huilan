"""
轻量级自动化测试框架
2019.8.14：  1.已经将登录模块化
            2.未解决common方法中wares_name值引入用例的问题
2019.8.27： 1.基本完善两个流程
            2.对于公共模块进行了参数化
"""
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from utils.common import login
from utils.common import achieve
from selenium.webdriver.common.action_chains import ActionChains
import random
import pyautogui
import json

class TestXxYP(unittest.TestCase):
    URL = Config().get('URL_YSTEST')
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def sub_tearDown(self):
        self.driver.quit()

    def common(self):
        left = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/h2').click()
        # 鼠标左键点击无效，只能用双击
        # ActionChains(driver).double_click(left).perform()
        self.driver.find_element_by_link_text("订单管理").click()
        self.driver.find_element_by_xpath(
            '//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/ul').find_element_by_link_text(
            '订单查询').click()
        self.driver.find_element_by_id('userMobile').send_keys('17315053551')
        self.driver.find_element_by_id('submitBtn').click()
        # 获取列表1的订单编号
        number = self.driver.find_element_by_xpath('//*[@id="code"]').text
        # 获取列表1的审核状态
        status = self.driver.find_element_by_xpath('//*[@id="orderlistbody"]/tr[1]/td[11]').text
        #logger.info('当前订单状态：' + status)
        return number,status

    #借款流程
    def test_xxyp_jk(self):
        logger.info("当前处于借款流程")
        driver = self.driver
        print(self.URL)
        driver.get(self.URL)
        logger.info("当前网址为%s" % self.URL)
        login(self)
        #获取common方法中的status和number值
        number,status = self.common()
        logger.info('当前订单状态：' + status)
        logger.info('当前订单号：' + number)
        # 测试数据
        if status == '审核通过，待认证':
        #if status == '审核中':
            driver.find_element_by_xpath('//*[@id="orderlistbody"]/tr[1]/td[14]/button').click()
            time.sleep(1)
            # 获取商品名称
            menu_name = driver.find_element_by_xpath('//*[@id="goodDetail"]/tr/td[8]/button')
            ActionChains(driver).double_click(menu_name).perform()
            time.sleep(1)
            wares_name = driver.find_element_by_id('shangPinMingChen').text
            logger.info('当前商品名称：' + wares_name)
        # 借款流程
        if wares_name == '小象钱包':
            driver.find_element_by_xpath('//*[@id="wuliuxiangqing"]/div/div/div[1]/button').click()
            time.sleep(2)
            # 审核管理---自动化审核---钱包机审通过确认
            driver.find_element_by_link_text('审核管理').click()
            menu_shen = driver.find_element_by_xpath(
                '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/ul').find_element_by_link_text('自动化审核')
            ActionChains(driver).move_to_element(menu_shen).perform()
            driver.find_element_by_link_text('钱包机审通过确认').click()
            print('进入' + driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div/div/div/ol/li[3]').text + '界面')
            driver.find_element_by_id('orderCode').send_keys(number)
            driver.find_element_by_id('formselectsubmit').click()
            driver.find_element_by_xpath('//*[@id="purseReviewtbody"]/tr/td[1]/input').click()
            driver.find_element_by_id('zhuandanButton').click()
            time.sleep(1)
            # 确认按钮
            driver.find_element_by_xpath('/html/body/div[4]/div[7]/div/button').click()
            time.sleep(3)
            # 弹出框处理
            driver.switch_to.alert.accept()
            time.sleep(2)
            # 键盘回车
            # ActionChains(driver).send_keys(Keys.ENTER).perform()
            # 测试取消按钮
            # driver.find_element_by_xpath('/html/body/div[4]/div[7]/button').click()
            # 小象钱包---资产组包
            driver.find_element_by_link_text('小象钱包').click()
            driver.find_element_by_xpath(
                '//*[@id="bs-example-navbar-collapse-1"]/ul/li[10]/ul').find_element_by_link_text('资产组包').click()
            print('进入' + driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div[1]/div/div/ol/li[2]').text + '页面')
            driver.find_element_by_id('orderCode').send_keys(number)
            driver.find_element_by_xpath('//*[@id="AssetbagForm"]/button[2]').click()
            # 打印资产归属
            menu_gs = driver.find_element_by_xpath('//*[@id="Assetbagtbody"]/tr[1]/td[16]').text
            print("资产归属：" + menu_gs)
            driver.find_element_by_xpath('//*[@id="Assetbagtbody"]/tr/td[1]/input').click()
            driver.find_element_by_id('tiJiaoRenModalBtn').click()
            time.sleep(1)
            # 生成随机数
            driver.find_element_by_id('zubao_title').send_keys('测试' + str(random.randint(30, 150)))
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="tiJiaoRenModal"]/div/div/form/div[2]/button[2]').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[9]/div[7]/div/button').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[9]/div[7]/div/button').click()
            # if menu_gs == '云信普惠2022号单一颜值卡B':
            if menu_gs == '小象聚宝-美颜卡借款2':
                # 记录当前窗口句柄
                onehandle = driver.current_window_handle
                print("当前后台窗口句柄：" + onehandle)
                # 新建标签页;聚宝后端
                ##web.get("chrome").open('http://47.97.26.155:8088/xiaoxiang-jubao/page/admins/other/login.html',new=0,autoraise=True)
                driver.get('http://47.97.26.155:8088/xiaoxiang-jubao/page/admins/other/login.html')
                twohandle = driver.current_window_handle
                print("当前聚宝后台窗口句柄：" + twohandle)
                # 登录
                username_hou = driver.find_element_by_id('username')
                username_hou.send_keys(Keys.CONTROL, 'a')
                username_hou.send_keys('admin')
                password_hou = driver.find_element_by_id('password')
                password_hou.send_keys(Keys.CONTROL, 'a')
                password_hou.send_keys('1qaz2wsx')
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="exampleInputEmail1"]').click()
                # 发标
                driver.find_element_by_xpath('//*[@id="invest"]').click()
                time.sleep(2)
                driver.switch_to.alert.accept()
                time.sleep(2)
                driver.switch_to.alert.accept()
                # 编辑借款订单
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="leftmenu"]/ul/ul[1]/li[2]/a').click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="tjb-result"]/table/tbody/tr[2]/td[12]/input[2]').click()
                driver.find_element_by_xpath('//*[@id="earlyRepaymentRate"]').send_keys('0')
                driver.find_element_by_xpath('//*[@id="form1"]/fieldset/table/tbody/tr[43]/td[2]/input').click()
                time.sleep(2)
                driver.switch_to.alert.accept()
                time.sleep(2)
                driver.switch_to.alert.accept()
                time.sleep(1)
                # 聚宝前端
                driver.get('http://47.97.26.155:8088/xiaoxiang-jubao/page/index.html')
                # web.get("chrome").open('http://47.97.26.155:8088/xiaoxiang-jubao/page/index.html', new=0,autoraise=True)
                driver.find_element_by_xpath('//*[@id="deng"]/div[1]/a').click()
                time.sleep(1)
                # 登录
                username_qian = driver.find_element_by_id('username')
                username_qian.send_keys(Keys.CONTROL, 'a')
                username_qian.send_keys('15995295109')
                password_qian = driver.find_element_by_id('password')
                password_qian.send_keys(Keys.CONTROL, 'a')
                password_qian.send_keys('123456a')
                driver.find_element_by_xpath('//*[@id="loginForm"]/p[5]/input').click()
                # 定向标
                driver.find_element_by_id('Investstatus7').click()
                time.sleep(2)
                # 全包了    运用pyautogui方法点击全包了，但是目前在弹出确认投标界面的alert弹出框无法点击处理
                pyautogui.PAUSE = True
                pyautogui.moveTo(x=1569, y=625, duration=0)
                pyautogui.click()

                # driver.find_element_by_xpath('//*[@id="investbutton"]').click()
                # 立即投资
                pyautogui.moveTo(x=1428, y=805, duration=0)
                pyautogui.click()
                # 验证码
                pyautogui.moveTo(x=511, y=880, duration=0)
                pyautogui.click()
                time.sleep(1)
                pyautogui.press('Enter')
                # 休眠填验证码
                time.sleep(10)
                pyautogui.moveTo(x=963, y=1009, duration=0)
                pyautogui.click()
                time.sleep(1)
                pyautogui.press('Enter')
                # 点击验证码
                time.sleep(1)
                # 审核放款
                driver.get('http://47.97.26.155:8088/xiaoxiang-jubao/page/admins/other/login.html')
                driver.switch_to_window(twohandle)
                username_hou = driver.find_element_by_id('username')
                username_hou.send_keys(Keys.CONTROL, 'a')
                username_hou.send_keys('admin')
                password_hou = driver.find_element_by_id('password')
                password_hou.send_keys(Keys.CONTROL, 'a')
                password_hou.send_keys('1qaz2wsx')
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="exampleInputEmail1"]').click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="leftmenu"]/ul/ul[1]/li[3]/a').click()
                driver.find_element_by_id('fangkuang').click()
                time.sleep(2)
                driver.switch_to.alert.accept()
                time.sleep(2)
                driver.switch_to.alert.accept()
            # 目前只考虑了小象聚宝与云信两种情况
            else:
                pass
    #商品流程
    def test_xxyp_sp(self):
        logger.info("当前处于商品流程")
        driver = self.driver
        print(self.URL)
        driver.get(self.URL)
        logger.info("当前网址为%s" % self.URL)
        login(self)
        # 获取common方法中的status和number值
        number, status = self.common()
        logger.info('当前订单状态：' + status)
        logger.info('当前订单号：' + number)
        #if status == '审核通过，待认证':
        if status == '审核中':
            driver.find_element_by_xpath('//*[@id="orderlistbody"]/tr[1]/td[14]/button').click()
            time.sleep(1)
            # driver.find_element_by_xpath('//*[@id="wuliuxiangqing"]/div/div/div[1]/button/span').click()
            # time.sleep(1)
            # 获取商品名称
            menu_name = driver.find_element_by_xpath('//*[@id="goodDetail"]/tr/td[8]/button')
            ActionChains(driver).double_click(menu_name).perform()
            time.sleep(1)
            wares_name = driver.find_element_by_id('shangPinMingChen').text
            logger.info('当前商品名称：' + wares_name +'走审核管理---自动化审核---商品机审通过确认步骤')
            time.sleep(2)
            if wares_name != '小象钱包':
                driver.find_element_by_xpath('//*[@id="wuliuxiangqing"]/div/div/div[4]/button').click()
                # 审核管理---自动化审核---商品机审通过确认
                time.sleep(1)
                driver.find_element_by_link_text('审核管理').click()
                menu_shen2 = driver.find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/ul').find_element_by_link_text('自动化审核')
                ActionChains(driver).move_to_element(menu_shen2).perform()
                driver.find_element_by_link_text('商品机审通过确认').click()
                logger.info('进入' + driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/ol/li[3]').text + '页面')
                driver.find_element_by_id('orderCode').send_keys(number)
                driver.find_element_by_id('formselectsubmit').click()
                driver.find_element_by_xpath('//*[@id="goodsReviewtbody"]/tr/td[1]/input').click()
                time.sleep(1)
                driver.find_element_by_id('zhuandanButton').click()
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/div[6]/div[7]/div/button').click()
                time.sleep(3)
                driver.switch_to.alert.accept()
                time.sleep(2)
                logger.info("走物流管理---采购分单---待采购---待发货步骤")
                # 物流管理---采购分单---待采购---待发货
                driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/a').click()
                menu_wu = driver.find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/ul/li[1]').find_element_by_link_text('发货管理')
                ActionChains(driver).move_to_element(menu_wu).perform()
                driver.find_element_by_link_text('采购分单').click()
                logger.info('进入' + driver.find_element_by_xpath('/html/body/div[2]/div/div/ol/li[2]').text + '页面')
                time.sleep(1)
                # 采购分单
                driver.find_element_by_id('orderCode').send_keys(number)
                driver.find_element_by_id('formSubmit').click()
                driver.find_element_by_xpath('//*[@id="waitbuytbody"]/tr/td[1]/input').click()
                driver.find_element_by_xpath('//*[@id="home"]/div[2]/div/table/tfoot/tr/td[1]/button').click()
                # 定位到下拉框
                ss = driver.find_element_by_xpath('//*[@id="caigouAssignForm"]/div/span')
                # 下拉框+输入框组合解决输入数据方法
                ActionChains(driver).double_click(ss).send_keys('周炀').perform()
                time.sleep(1)
                driver.find_element_by_id('fendansubmit').click()
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/div[12]/div[7]/div/button').click()
                time.sleep(2)
                # 待采购
                driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul').find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/a').click()
                menu_wu2 = driver.find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/ul/li[1]').find_element_by_link_text('发货管理')
                ActionChains(driver).move_to_element(menu_wu2).perform()
                driver.find_element_by_link_text('待采购').click()
                logger.info('进入' + driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/ol/li[3]').text + '页面')
                driver.find_element_by_xpath('//*[@id="waitbuytbody"]/tr/td[20]/button[1]').click()
                time.sleep(1)
                driver.find_element_by_id('caiGouSubBtn').click()
                driver.find_element_by_id('formPurchaseChannel').click()
                driver.find_element_by_xpath('//*[@id="formPurchaseChannel"]/option[2]').click()
                driver.find_element_by_id('formPurchaseAccount').send_keys('12345')
                driver.find_element_by_id('formPurchaseChannelOrdercode').send_keys('121111')
                driver.find_element_by_xpath('//*[@id="caiGouSubForm"]/div[2]/div[4]/input').send_keys('1')
                driver.find_element_by_id('formPurchaseFee').send_keys('1')
                driver.find_element_by_id('formPurchasePayNum').send_keys('112233')
                driver.find_element_by_id('presellTag').click()
                driver.find_element_by_xpath('//*[@id="presellTag"]/option[2]').click()
                now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                driver.find_element_by_id('formPurchasePayTime').send_keys(now_time)
                driver.find_element_by_id('caiGouSubFormOutSubmit').click()
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/div[7]/div[7]/div/button').click()
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/div[7]/div[7]/div/button').click()
                time.sleep(2)
                # 待发货(不能用)
                driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul').find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/a').click()
                menu_wu3 = driver.find_element_by_xpath(
                    '//*[@id="bs-example-navbar-collapse-1"]/ul/li[4]/ul/li[1]').find_element_by_link_text('发货管理')
                ActionChains(driver).move_to_element(menu_wu3).perform()
                driver.find_element_by_link_text('待发货').click()
                logger.info('进入' + driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/ol/li[3]').text + '页面')
                driver.find_element_by_id('orderCode').send_keys(number)
                driver.find_element_by_id('waitselectsubmit').click()
                driver.find_element_by_xpath('//*[@id="waitsendtbody"]/tr/td[16]/button[1]').click()
                time.sleep(1)
                driver.find_element_by_id('orderFaHuoBtn').click()
                time.sleep(2)
                pyautogui.PAUSE = True
                pyautogui.moveTo(x=124, y=455, duration=0)
                pyautogui.click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="faHuoSub"]/div/div/button[2]').click()
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="faHuoSub"]/div/div/button[1]').click()
                time.sleep(1)
                driver.find_element_by_id('logisticsChannel').click()
                driver.find_element_by_xpath('//*[@id="logisticsChannel"]/option[2]').click()
                driver.find_element_by_id('logisticsNum1').send_keys('11223')
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="confirmfahuoform"]/div[3]/button[2]').click()
                time.sleep(1)
                pyautogui.moveTo(x=946, y=720, duration=0)
                pyautogui.click()
                time.sleep(3)


if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    print(report)
    with open(report,'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='轻量级测试框架-小象优品测试',description='调试用例')
        #必须用unittest.main   否则无法生成报告
        runner.run(TestXxYP('test_xxyp_sp'))
        e = Email(title='小象优品后台调试测试报告',
                  message='这是今天的测试报告，请查收！',
                  receiver='773858927@qq.com',
                  server='smtp.qq.com',
                  sender='773858927@qq.com',
                  password='hxmsxbafdhdqbceg',
                  path=report
                  )
        e.send()
        unittest.main(runner)