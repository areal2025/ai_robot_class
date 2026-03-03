#!/bin/bash

# 启动虚拟显示
Xvfb :0 -screen 0 1024x768x24 &
export DISPLAY=:0

# 启动WebSocket服务器（后台）
cd /app
python3 server.py &

# 等待服务器启动
sleep 2

# 保持容器运行
echo "PyBullet服务器运行中..."
wait
