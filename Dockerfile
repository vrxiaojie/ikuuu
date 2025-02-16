FROM hub.rat.dev/library/python:3.9-slim-bullseye

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime

COPY sources.list /etc/apt

# 安装Edge浏览器
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    cron \
    unzip \
    libatomic1 \
    libglib2.0-0 \
    && wget -O edge.deb "https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_124.0.2478.109-1_amd64.deb" \
    && apt-get install -y ./edge.deb \
    && rm -rf \
        edge.deb \
        /var/lib/apt/lists/* \
        /usr/share/man \
        /usr/share/doc

# 下载EdgeDriver
RUN wget "https://msedgedriver.azureedge.net/124.0.2478.109/edgedriver_linux64.zip" \
    && unzip edgedriver_linux64.zip -d /usr/bin/ \
    && rm edgedriver_linux64.zip && rm -rf /usr/bin/Driver_Notes

# 安装Python依赖
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用文件
COPY app/checkin.py .
COPY setup.sh /usr/local/bin/

# 最终清理
RUN apt-get clean && \
    rm -rf /tmp/* /var/tmp/* && \
    chmod +x /usr/local/bin/setup.sh && \
    touch /var/log/cron.log

CMD ["sh", "/usr/local/bin/setup.sh"]