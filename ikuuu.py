from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import argparse

# 解析命令行传参
description = "Usage: python ikuuu.py -u <username> -p <password>"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-u", "--username", type=str, required=True, help="")
parser.add_argument("-p", "--password", type=str, required=True, help="Password")
args = parser.parse_args()
username = args.username
password = args.password

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # 禁用日志打印输出
options.add_argument("--headless")  # 无界面模式
options.add_argument("--disable-gpu")

service = Service()
# 启动Edge浏览器
driver = webdriver.Edge(service=service, options=options)
traffic_before_signin = ""

def open_url(url):
    driver.set_page_load_timeout(2) # 设置页面超时2秒
    try:
        # 打开网页
        driver.get(url)  # 替换为目标网页的URL
    except TimeoutException:
        driver.execute_script("window.stop()")


def get_usage() -> str:
    time.sleep(3)
    elements = driver.find_elements(By.CLASS_NAME, 'card-body')
    for item in elements:
        if "GB" in item.text:
            return item.text


def login():
    print(f"账户{username}正在登录中...")
    open_url('https://ikuuu.one/auth/login')
    WebDriverWait(driver, 10, poll_frequency=0.2).until(EC.presence_of_element_located((By.ID, 'email')))
    # 输入用户名
    username_field = driver.find_element(By.ID, 'email')  # 假设用户名输入框的name属性是username
    username_field.send_keys(username)  # 替换为你的用户名

    # 输入密码
    password_field = driver.find_element(By.ID, 'password')  # 假设密码输入框的name属性是password
    password_field.send_keys(password)  # 替换为你的密码

    # 提交登录表单
    password_field.send_keys(Keys.RETURN)  # 按下回车键提交

    # 获取流量值
    global traffic_before_signin
    traffic_before_signin = get_usage()
    print(f"登录成功，当前流量:{traffic_before_signin}")


def sign_in():
    WebDriverWait(driver, 10, poll_frequency=0.2).until(EC.presence_of_element_located((By.ID, 'checkin-div')))
    # 点击签到按钮
    sign_in_button = driver.find_element(By.ID, 'checkin-div')
    if '签到' in sign_in_button.text:
        sign_in_button.click()
        driver.execute_script("location.reload()")
        gain_traffic = float(get_usage().split(' ')[0]) - float(traffic_before_signin.split(' ')[0])
        print(f"签到成功!签到获得流量:{gain_traffic} GB，")
    else:
        print(f"今日已签到")


def run():
    try:
        login()
        sign_in()

    except Exception as e:
        print("出现错误: {}".format(e))

    finally:
        driver.quit()


if __name__ == '__main__':
    run()
