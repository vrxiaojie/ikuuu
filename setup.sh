#!/bin/bash

# 生成cron配置文件
cat <<EOF > /etc/cron.d/checkin-cron
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
USERNAME=${USERNAME}
PASSWORD=${PASSWORD}
${CRON_TIME} python3 /app/checkin.py >> /var/log/cron.log 2>&1

EOF

# 设置权限
chmod 0644 /etc/cron.d/checkin-cron
chmod +x /app/checkin.py

# 设置定时任务
crontab /etc/cron.d/checkin-cron

# 启动服务
service cron reload
cron && tail -f /var/log/cron.log

