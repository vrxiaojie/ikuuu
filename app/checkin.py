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

def open_url(url):
    driver.set_page_load_timeout(2) # 设置页面超时2秒
    try:
        # 打开网页
        driver.get(url)  # 替换为目标网页的URL
    except TimeoutException:
        driver.execute_script("window.stop()")


def get_usage() -> float:
    time.sleep(3)
    traffic = driver.find_element(By.CSS_SELECTOR, '#app > div > div.main-content > section > div:nth-child(3) > div:nth-child(2) > div > div.card-wrap > div.card-body > span')
    return float(traffic.text)


def login():
    print(f"账户{username}正在登录中...")
    open_url('https://ikuuu.one/auth/login')
    WebDriverWait(driver, 10, poll_frequency=0.2).until(EC.presence_of_element_located((By.ID, 'email')))
    # 输入用户名
    username_field = driver.find_element(By.ID, 'email')
    username_field.send_keys(username)

    # 输入密码
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    # 提交登录表单
    password_field.send_keys(Keys.RETURN)  # 按下回车键提交

    # 获取流量值
    global traffic_before_signin
    traffic_before_signin = get_usage()
    print(f"登录成功，当前流量:{traffic_before_signin}GB")


def sign_in():
    WebDriverWait(driver, 10, poll_frequency=0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#checkin-div')))
    # 点击签到按钮
    sign_in_button = driver.find_element(By.CSS_SELECTOR, '#checkin-div')
    if '签到' in sign_in_button.text:
        sign_in_button.click()
        driver.execute_script("location.reload()")
        gain_traffic = get_usage() - traffic_before_signin
        print(f"签到成功!签到获得流量:{gain_traffic} GB，")
    else:
        print(f"今日已签到")


def run():
    global driver
    retry = 0
    while True:
        try:
            driver = webdriver.Edge(service=service, options=options)
            login()
            sign_in()
            break

        except Exception as e:
            if retry == 3:
                print(f"出现错误: {e}")
                break
            retry += 1
            print(f"出现错误:{e} \n第{retry}次重试")
            driver.quit()
            time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    run()
