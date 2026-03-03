# 宇树机器狗遥控仿真 Demo

## 简介

基于PyBullet的机器狗仿真，支持WebSocket实时控制。

## 启动方式

### 1. 安装依赖

```bash
pip install pybullet websockets
```

### 2. 启动仿真服务器

```bash
cd demo1/py
python server.py
```

服务器默认：
- 端口: 8765
- 令牌: `ai-robotics-course-2026`

### 3. 访问控制界面

打开浏览器访问：`http://localhost:8888/demo1/`

或使用课程网站：`https://course.a-real.me/demo1/`

> 注意：网站版本需要服务器支持WebSocket

## 功能

### 控制方式

| 输入 | 功能 |
|------|------|
| W/S | 前进/后退 |
| A/D | 左移/右移 |
| ←/→ | 左转/右转 |
| 空格 | 跳跃 |
| Esc | 紧急停止 |

### 遥控器功能

- 摇杆控制移动
- 模式切换（低速/trot/奔跑）
- 站立/坐下/跳跃
- 身体高度调节
- 翻滚角度调节

## 令牌

默认令牌: `ai-robotics-course-2026`

可在启动时通过 `--token` 参数修改。

## 文件结构

```
demo1/
├── py/
│   └── server.py      # PyBullet仿真服务器
├── static/
│   └── index.html     # 遥控器前端
└── README.md
```
