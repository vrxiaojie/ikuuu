<p align="center">
<a href="https://hub.docker.com/r/vrxiaojie/ikuuu-checkin"><img src="/images/docker-logo-blue.png" alt="Docker"></a>
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/image-ikuuu--checkin-blue">
<img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/vrxiaojie/ikuuu-checkin?cacheSeconds=https%3A%2F%2Fhub.docker.com%2Fr%2Fvrxiaojie%2Fikuuu-checkin">
<img alt="Docker Image Size" src="https://img.shields.io/docker/image-size/vrxiaojie/ikuuu-checkin?cacheSeconds=https%3A%2F%2Fhub.docker.com%2Fr%2Fvrxiaojie%2Fikuuu-checkin">
<img alt="Docker Image Version" src="https://img.shields.io/docker/v/vrxiaojie/ikuuu-checkin?link=https%3A%2F%2Fhub.docker.com%2Fr%2Fvrxiaojie%2Fikuuu-checkin">
</p>

# 简介
本项目为ikuuu每日签到脚本，支持本地Python运行及Docker定时运行。

本仓库中的`ikuuu.py`为本地Python运行脚本，`requirements.txt`为python包需求文件，其他文件为构建Docker镜像所用。

# 如何使用
## 1 本地运行Python脚本
克隆本仓库
```bash
git clone https://github.com/vrxiaojie/ikuuu.git
```

安装python所需包
```bash
pip install -r requirements.txt
```

运行程序
```bash
python ikuuu.py -u <用户名> -p <密码>
```

## 2 使用Docker容器以定时运行
先拉取镜像
```bash
docker pull vrxiaojie/ikuuu-checkin
```

创建并运行docker容器
```bash
docker run -itd \
-e CRON_TIME="15 7 * * *" \
-e USERNAME=email@email.com \
-e PASSWORD=password \
--name ikuuu \
vrxiaojie/ikuuu-checkin
```

环境变量:
| 变量名    | 解释             |
| --------- | ---------------- |
| CRON_TIME | 5位cron表达式    |
| USERNAME  | 登录用户名(邮箱) |
| PASSWORD  | 密码             |

注:
1. 程序不会去存储你的用户名密码，是通过环境变量获取到用户名和密码的。具体登录逻辑可查看app/checkin.py文件。
2. 5位cron表达式是 **分时日月年** 格式，例如`15 7 * * *`表示每天7点15分执行一次程序。
3. 请为docker容器预留至少**1GB内存**，以防内存不足程序运行异常。

## 3 自行构建
先克隆本仓库
```bash
git clone https://github.com/vrxiaojie/ikuuu.git
```

进入仓库文件夹并开始构建
```bash
cd ikuuu && docker build -t ikuuu-checkin .
```

