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

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

options = Options()
options.add_argument("--headless")  # 无界面模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")  # 容器必须的沙盒限制
options.add_argument("--disable-dev-shm-usage")  # 防止内存不足
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")

service = Service(executable_path='/usr/bin/msedgedriver')
# 启动Edge浏览器
driver = webdriver.Edge(service=service, options=options)
traffic_before_signin = ""


def open_url(url):
    driver.set_page_load_timeout(5)
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

    # 等待页面跳转
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
        print(f"今日已签到。当前流量{traffic_before_signin}")


def run():
    retry = 0
    while True:
        try:
            login()
            sign_in()
            break

        except Exception as e:
            if retry == 3:
                print("出现错误: {}".format(e))
                break
            retry += 1
            print(f"等待10s，第{retry}次重试")
            time.sleep(10)

    driver.quit()


if __name__ == '__main__':
    run()
