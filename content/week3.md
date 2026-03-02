# 第3周：Python编程与机器人控制入门

![Python Logo](https://www.python.org/static/community_logos/python-logo-master-v3-TM.png)

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | Python基础与节点 | Python、第一个基础ROS2节点 |
| 第2次 | 3小时 | 机器人控制 | 速度控制、走正方形 |

---

## 第一次课：Python基础与节点（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 讲解 | 40分钟 | Python基础回顾 |
| 讲解 | 50分钟 | ROS2 Python库介绍 |
| 演示 | 30分钟 | 第一个Hello World节点 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 40分钟 | 编写第一个节点 |
| 总结 | 10分钟 | 本次课小结 |

---

## 1.1 Python基础回顾（40分钟）

### 1.1.1 变量和数据类型

```python
# 整数
age = 25

# 浮点数（小数）
speed = 1.5

# 字符串
name = "turtle"

# 布尔值
is_moving = True

# 列表
colors = ["red", "green", "blue"]

# 字典
robot = {
    "name": "TurtleBot",
    "speed": 1.0,
    "battery": 80
}
```

### 1.1.2 函数

```python
def say_hello():
    """这是一个简单的函数"""
    print("Hello, Robot!")

# 带参数的函数
def move_robot(speed, direction):
    """移动机器人"""
    print(f"Moving at {speed} m/s, direction: {direction}")

# 调用
say_hello()
move_robot(1.0, "forward")
```

### 1.1.3 类（面向对象）

```python
class Robot:
    """机器人小类"""
    
    # 初始化方法（构造函数）
    def __init__(self, name):
        self.name = name  # 实例属性
        self.speed = 0   # 初始速度为0
    
    # 方法
    def move(self, speed):
        """移动方法"""
        self.speed = speed
        print(f"{self.name} is moving at {speed} m/s")
    
    def stop(self):
        """停止"""
        self.speed = 0
        print(f"{self.name} stopped")

# 创建实例
my_robot = Robot("TurtleBot")
my_robot.move(1.0)  # 输出：TurtleBot is moving at 1.0 m/s
my_robot.stop()     # 输出：TurtleBot stopped
```

---

## 1.2 ROS2 Python库（50分钟）

### 1.2.1 rclpy简介

> **rclpy** = ROS2 Client Library for Python
> 
> ROS2的Python客户端库，让我们能用Python写ROS2程序

```
rclpy 结构：

┌─────────────────────────────────────────────┐
│              应用程序                        │
├─────────────────────────────────────────────┤
│                                             │
│   ┌─────────────────────────────────────┐  │
│   │          rclpy (Python库)            │  │
│   │  • Node         • Publisher         │  │
│   │  • Subscription  • Timer             │  │
│   │  • Service      • Action             │  │
│   └─────────────────────────────────────┘  │
│                     │                        │
│                     ▼                        │
│   ┌─────────────────────────────────────┐  │
│   │        rcl (C库)                    │  │
│   └─────────────────────────────────────┘  │
│                     │                        │
│                     ▼                        │
│   ┌─────────────────────────────────────┐  │
│   │         DDS 中间件                   │  │
│   └─────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.2.2 常用模块

```python
# 导入ROS2 Python库
import rclpy
from rclpy.node import Node

# 导入消息类型
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry

# 导入时间
from rclpy.duration import Duration
import time
```

---

## 1.3 第一个ROS2 Python节点（30分钟）

### 代码模板

```python
#!/usr/bin/env python3
"""
第一个ROS2 Python节点：Hello World
"""

import rclpy
from rclpy.node import Node


class HelloNode(Node):
    """最简单的ROS2节点"""
    
    def __init__(self):
        # 调用父类初始化，节点名为 'hello_node'
        super().__init__('hello_node')
        
        # 打印日志（ROS2的print）
        self.get_logger().info('🎉 Hello ROS2! 我是第一个Python节点！')


def main(args=None):
    """主函数：入口点"""
    
    # 1. 初始化ROS2（必须的第一步）
    rclpy.init(args=args)
    
    # 2. 创建节点
    node = HelloNode()
    
    # 3. 让节点保持运行（spin = 保持监听回调）
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C 优雅退出
        pass
    finally:
        # 4. 清理资源
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 运行

```bash
# 保存文件为 hello_node.py
# 添加执行权限
chmod +x hello_node.py

# 运行
python3 hello_node.py

# 应该看到输出：
# [INFO] [hello_node]: 🎉 Hello ROS2! 我是第一个Python节点！
```

---

## 1.4 发布速度命令（40分钟）

### 完整代码

```python
#!/usr/bin/env python3
"""
让小乌龟直行的Python节点
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class StraightMover(Node):
    """控制小乌龟直行的节点"""
    
    def __init__(self):
        # 节点名
        super().__init__('straight_mover')
        
        # 创建发布者：发布到 /turtle1/cmd_vel
        # Twist 是速度消息类型
        # 10 是队列大小
        self.cmd_vel_pub = self.create_publisher(
            Twist, 
            '/turtle1/cmd_vel', 
            10
        )
        
        # 创建定时器：每0.1秒调用一次 callback
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.get_logger().info('🚀 直行控制节点已启动！')
    
    def timer_callback(self):
        """定时器回调函数：每0.1秒执行一次"""
        
        # 创建速度消息
        msg = Twist()
        msg.linear.x = 1.0    # 前进 1 m/s
        msg.angular.z = 0.0   # 不旋转
        
        # 发布消息
        self.cmd_vel_pub.publish(msg)
        
        # 打印日志
        self.get_logger().info('Published: linear.x=1.0')


def main(args=None):
    rclpy.init(args=args)
    node = StraightMover()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 代码详解

```python
# ┌─────────────────────────────────────────────────────────────┐
# │                   代码结构解析                              │
# ├─────────────────────────────────────────────────────────────┤
# │                                                             │
# │  1. 导入库                                                  │
# │     import rclpy              # ROS2 Python库               │
# │     from rclpy.node import Node  # 节点基类                 │
# │     from geometry_msgs.msg import Twist  # 速度消息         │
# │                                                             │
# │  2. 定义节点类                                              │
# │     class StraightMover(Node):      # 继承Node类           │
# │         def __init__(self):         # 初始化               │
# │             self.create_publisher() # 创建发布者            │
# │             self.create_timer()     # 创建定时器            │
# │         def timer_callback(self):   # 回调函数             │
# │                                                             │
# │  3. 主函数                                                  │
# │     rclpy.init()             # 初始化ROS2                  │
# │     rclpy.spin(node)        # 保持运行                    │
# │     rclpy.shutdown()        # 关闭ROS2                    │
# │                                                             │
# └─────────────────────────────────────────────────────────────┘
```

---

## 第二次课：机器人控制（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 提问巩固 |
| 讲解 | 40分钟 | 走正方形原理 |
| 演示 | 20分钟 | 完整代码演示 |
| 实践 | 60分钟 | 走正方形实验 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 挑战任务 |

---

## 2.1 走正方形原理（40分钟）

### 2.1.1 运动分解

```
走正方形 = 4条直线 + 4次90°转弯

         ┌───────────┐
         │           │
    ③    │    ②      │    ①
         │           │
         │           │
         │    ④      │
         └───────────┘
              ↑
           起点/终点

步骤分解：
1. 直行 → 右转90°
2. 直行 → 右转90°  
3. 直行 → 右转90°
4. 直行 → 右转90°（回到起点）
```

### 2.1.2 参数计算

```python
# ┌─────────────────────────────────────────────────────────────┐
# │                    参数计算                                  │
# ├─────────────────────────────────────────────────────────────┤
# │                                                             │
# │  设定参数：                                                  │
# │  • 边长 SIDE_LENGTH = 2.0 米                               │
# │  • 线速度 SPEED = 1.0 m/s                                 │
# │  • 角速度 TURN_SPEED = 1.0 rad/s                          │
# │                                                             │
# │  计算：                                                     │
# │  ┌─────────────────────────────────────────────────────┐   │
# │  │ 直行时间 = 距离 / 速度                               │   │
# │  │ MOVE_TIME = SIDE_LENGTH / SPEED                     │   │
# │  │           = 2.0 / 1.0 = 2.0 秒                       │   │
# │  └─────────────────────────────────────────────────────┘   │
# │                                                             │
# │  ┌─────────────────────────────────────────────────────┐   │
# │  │ 转弯时间 = 角度(弧度) / 角速度                       │   │
# │  │ 90° = π/2 ≈ 1.5708 弧度                             │   │
# │  │ TURN_TIME = (π/2) / TURN_SPEED                      │   │
# │  │           = 1.5708 / 1.0 = 1.5708 秒                 │   │
# │  └─────────────────────────────────────────────────────┘   │
# │                                                             │
# │  总时间 = 4 × (2.0 + 1.5708) = 14.28 秒                   │
# │                                                             │
# └─────────────────────────────────────────────────────────────┘
```

### 2.1.3 常用多边形参数

| 图形 | 边数 | 外角 | 外角(弧度) | 转弯时间(rad/s=1) |
|------|------|------|-----------|------------------|
| 三角形 | 3 | 120° | 2.094 | 2.094秒 |
| 正方形 | 4 | 90° | 1.571 | 1.571秒 |
| 五边形 | 5 | 72° | 1.257 | 1.257秒 |
| 六边形 | 6 | 60° | 1.047 | 1.047秒 |
| 八边形 | 8 | 45° | 0.785 | 0.785秒 |

---

## 2.2 完整代码（20分钟）

```python
#!/usr/bin/env python3
"""
让小乌龟走正方形的控制脚本
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class SquareMover(Node):
    """走正方形的控制节点"""
    
    def __init__(self):
        super().__init__('square_mover')
        
        # 创建发布者
        self.cmd_vel_pub = self.create_publisher(
            Twist, 
            '/turtle1/cmd_vel', 
            10
        )
        
        # ============ 参数设置 ============
        self.SPEED = 1.0              # 线速度 m/s
        self.TURN_SPEED = 1.0          # 角速度 rad/s
        self.SIDE_LENGTH = 2.0         # 边长 m
        
        # 计算运动时间
        self.MOVE_TIME = self.SIDE_LENGTH / self.SPEED
        self.TURN_TIME = 1.5708 / self.TURN_SPEED  # 90° = π/2
        
        self.get_logger().info('🎯 正方形控制节点启动！')
        self.get_logger().info(f'📐 边长: {self.SIDE_LENGTH}m, 速度: {self.SPEED}m/s')
    
    def move_straight(self, duration):
        """直行指定时间"""
        self.get_logger().info('→ 直行...')
        
        msg = Twist()
        msg.linear.x = float(self.SPEED)
        msg.angular.z = 0.0
        
        # 记录开始时间
        start_time = self.get_clock().now()
        
        # 持续发布命令
        while (self.get_clock().now() - start_time).nanoseconds < duration * 1e9:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.01)
        
        # 停止
        self.stop()
        self.get_logger().info('✓ 直行完成')
    
    def turn(self, duration):
        """旋转指定时间"""
        self.get_logger().info('↻ 旋转...')
        
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = float(self.TURN_SPEED)
        
        start_time = self.get_clock().now()
        
        while (self.get_clock().now() - start_time).nanoseconds < duration * 1e9:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.01)
        
        self.stop()
        self.get_logger().info('✓ 旋转完成')
    
    def stop(self):
        """停止运动"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        time.sleep(0.1)
    
    def move_square(self):
        """执行走正方形"""
        self.get_logger().info('🏁 开始走正方形！')
        
        for i in range(4):
            self.get_logger().info(f'━━━ 第 {i+1}/4 条边 ━━━')
            self.move_straight(self.MOVE_TIME)
            
            self.get_logger().info(f'━━━ 第 {i+1}/4 次转弯 ━━━')
            self.turn(self.TURN_TIME)
        
        self.get_logger().info('🎉 正方形走完！回到起点！')


def main(args=None):
    rclpy.init(args=args)
    node = SquareMover()
    
    # 给系统一点准备时间
    time.sleep(1)
    
    # 执行走正方形
    node.move_square()
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 2.3 挑战任务（60分钟）

### 任务1：走三角形

```python
# 三角形参数
# 内角 = 60°
# 外角 = 180° - 60° = 120° = 2π/3 ≈ 2.094 rad

TURN_TIME_TRIANGLE = 2.094 / TURN_SPEED
```

### 任务2：走五边形

```python
# 五边形参数
# 内角 = 108°
# 外角 = 180° - 108° = 72° = 0.4π ≈ 1.257 rad

TURN_TIME_PENTAGON = 1.257 / TURN_SPEED
```

### 任务3：可配置边长

```python
def main(args=None):
    rclpy.init(args=args)
    node = SquareMover()
    
    # 让用户输入边长
    side = input("请输入边长(米): ")
    node.SIDE_LENGTH = float(side)
    node.MOVE_TIME = node.SIDE_LENGTH / node.SPEED
    
    node.move_square()
```

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | Hello World | 运行第一个节点 | ☐ |
| 2 | 直行 | 小乌龟前进 | ☐ |
| 3 | 后退 | 小乌龟后退 | ☐ |
| 4 | 旋转 | 原地转圈 | ☐ |
| 5 | 正方形 | 走正方形 | ☐ |
| 6 | 三角形 | 走三角形 | ☐ |
| 7 | 五边形 | 走五边形 | ☐ |

---

## 本周作业

### 📝 理论题

1. 解释 `create_publisher` 和 `create_timer` 的作用
2. 为什么在循环中要持续发布命令？

### 📐 计算题

- 正方形边长3米，速度1m/s，走完需要多少秒？

### 💻 实践题

1. 修改代码，实现走长方形（长3m，宽2m）
2. 尝试让边长可配置

---

## 知识点速查表

```
┌─────────────────────────────────────────────────────────────┐
│                    第3周知识点速查                           │
├─────────────────────────────────────────────────────────────┤
│  概念                                                          │
│  ├── rclpy = ROS2 Python客户端库                            │
│  ├── Node = ROS2节点                                        │
│  ├── Publisher = 发布者                                     │
│  ├── Timer = 定时器                                         │
│  └── Twist = 速度消息类型                                   │
│      ├── linear.x = 线速度 (m/s)                           │
│      └── angular.z = 角速度 (rad/s)                        │
├─────────────────────────────────────────────────────────────┤
│  公式                                                          │
│  ├── 直行时间 = 距离 / 速度                                  │
│  ├── 转弯时间 = 角度(弧度) / 角速度                         │
│  └── 90° = π/2 ≈ 1.57 rad                                 │
├─────────────────────────────────────────────────────────────┤
│  代码结构                                                      │
│  ├── import rclpy, Node, Twist                              │
│  ├── class MyNode(Node):                                    │
│  ├── def __init__(self):                                    │
│  │   ├── self.create_publisher()                          │
│  │   └── self.create_timer()                               │
│  └── def main():                                            │
│      ├── rclpy.init()                                       │
│      ├── rclpy.spin(node)                                   │
│      └── rclpy.shutdown()                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 课后阅读

- [ROS2 Python教程](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [Python官方文档](https://docs.python.org/3/)

---

## 第一阶段完成！

---


---

## 🆕 PyBullet仿真环境介绍

> 除了Turtlesim，我们还可以用**PyBullet**进行更真实的3D机器人仿真！

### 什么是PyBullet？

> **PyBullet** = Python + Bullet物理引擎  
> 一个开源的3D物理仿真库，支持机器人、车辆、物体等

```
PyBullet vs Turtlesim：

┌─────────────────────────────────────────────────────────────┐
│  Turtlesim                    │  PyBullet                   │
├───────────────────────────────┼─────────────────────────────┤
│  2D平面仿真                  │  3D空间仿真                 │
│  简单的小乌龟                │  真实的机器人模型           │
│  入门学习                    │  进阶学习                   │
│  只有一只小乌龟              │  可以有多个机器人           │
└───────────────────────────────┴─────────────────────────────┘
```

### 安装PyBullet

```bash
# 安装PyBullet
pip install pybullet

# 或使用conda
conda install pybullet -c conda-forge
```

### 第一个PyBullet示例：创建地面和球体

```python
#!/usr/bin/env python3
"""
第一个PyBullet示例：创建地面和摆动的球体
"""

import pybullet as p
import pybullet_data
import time

# 连接GUI客户端（显示3D窗口）
client_id = p.connect(p.GUI)

# 添加搜索路径（找到内置模型）
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 加载地面
plane_id = p.loadURDF("plane.urdf")

# 加载球体（使用球体URDF）
sphere_id = p.loadURDF("sphere2.urdf", [0, 0, 2])

# 设置重力
p.setGravity(0, 0, -9.8)

# 渲染器设置
p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_STA_PREVIEW, 0)

print("按Ctrl+C退出")
print("3D窗口显示：地面 + 球体")

# 仿真循环
try:
    while True:
        # 进一步仿真（1/240秒）
        p.stepSimulation()
        time.sleep(1./240.)
        
except KeyboardInterrupt:
    print("退出仿真")

# 断开连接
p.disconnect()
```

### 运行效果

```
┌─────────────────────────────────────────────────────────────┐
│                    PyBullet 3D窗口                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                         ☀ (光源)                            │
│                                                             │
│                    ┌─────────┐                              │
│                    │   球体   │ ← 球体受重力下落             │
│                    │    ○    │                              │
│                    └─────────┘                              │
│                    ───────────────────  ← 地面              │
│                                                             │
│                    [相机控制: 鼠标拖动]                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 机器人仿真示例：移动的小车

```python
#!/usr/bin/env python3
"""
PyBullet机器人示例：差速驱动小车
"""

import pybullet as p
import pybullet_data
import time

# 连接仿真
client_id = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 加载环境
p.loadURDF("plane.urdf")

# 加载机器人（小车）
# 使用内置的kuka或创建简单的盒子机器人
cube_start_pos = [0, 0, 0.5]
cube_start_orientation = p.getQuaternionFromEuler([0, 0, 0])

# 创建一个移动机器人（两个轮子+身体）
robot_id = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=p.createCollisionShape(p.BoxShape, halfExtents=[0.5, 0.3, 0.1]),
    basePosition=[0, 0, 0.1]
)

# 设置参数
max_force = 20
max_velocity = 3

print("机器人仿真开始！")
print("使用applyJointMotor2Control来控制轮子")

# 控制循环
while True:
    # 前进
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=0,  # 左轮
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=max_velocity,
        force=max_force
    )
    
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=1,  # 右轮
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=max_velocity,
        force=max_force
    )
    
    p.stepSimulation()
    time.sleep(1./240.)
```

### PyBullet vs ROS2仿真

| 特性 | PyBullet | ROS2 (Gazebo) |
|------|---------|---------------|
| 编程方式 | 纯Python | C++/Python + ROS2 API |
| 物理精度 | 中等 | 高 |
| 传感器仿真 | 基本 | 完整 |
| 与ROS集成 | 需手动 | 原生支持 |
| 学习曲线 | 简单 | 较难 |
| 适用场景 | 学习/原型 | 产品开发 |

### 何时使用PyBullet？

✅ 当你想快速验证算法时  
✅ 当你学习机器人运动学时  
✅ 当你需要简单的3D可视化时  
✅ 当你不想配置复杂的ROS环境时  

❌ 当你需要精确的传感器仿真时  
❌ 当你需要与真实ROS机器人集成时  
❌ 当你需要高保真物理仿真时  

---

### 🎯 练习：尝试运行PyBullet

```bash
# 1. 安装
pip install pybullet

# 2. 运行示例
python3 -m pybullet_envs.examples.enjoy_TF_AntBulletEnv

# 3. 查看内置示例
python3 -m pybullet_data.gdf_loader
```

## 🆕 进阶：用Python控制ROS2 + 集成OpenClaw

### RosClaw Python节点

```python
#!/usr/bin/env python3
"""
RosClaw Discovery Node - 自动发现ROS2能力
"""

import rclpy
from rclpy.node import Node
from rosclaw_msgs.srv import GetCapabilities, CallService, PublishMessage

class RosClawDiscovery(Node):
    """自动发现机器人能力"""
    
    def __init__(self):
        super().__init__('rosclaw_discovery')
        
        # 创建服务
        self.get_capabilities = self.create_service(
            GetCapabilities, 
            '/rosclaw/get_capabilities',
            self.handle_get_capabilities
        )
        
        self.get_logger().info('RosClaw Discovery Node 已启动')
    
    def handle_get_capabilities(self, request, response):
        """返回机器人能力列表"""
        response.capabilities = [
            'navigation',
            'camera',
            'speak',
            'battery'
        ]
        return response

def main(args=None):
    rclpy.init(args=args)
    node = RosClawDiscovery()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 集成OpenClaw

```bash
# 1. 安装OpenClaw
git clone https://github.com/openclaw/openclaw.git
cd openclaw && pnpm install

# 2. 安装RosClaw插件
pnpm add @rosclaw/openclaw-plugin

# 3. 配置
# openclaw.config.js
export default {
  plugins: [
    ['@rosclaw/openclaw-plugin', {
      wsUrl: 'ws://localhost:9090'
    }]
  ]
}

# 4. 启动
pnpm start
```

### 完整控制流程

```
用户: "让机器人走正方形"
   ↓
OpenClaw AI Agent 理解意图
   ↓
RosClaw 插件调用 ros2_publish
   ↓
Python节点发布 /cmd_vel
   ↓
机器人执行（走正方形）
   ↓
Agent 发送反馈给用户
```


> **第1-3周成就**：
> - ✅ 搭建ROS2开发环境
> - ✅ 理解节点和话题通信机制  
> - ✅ 用命令行控制机器人
> - ✅ 用Python编写机器人控制程序
> - ✅ 实现机器人走正方形

---

*第一阶段（基础与环境搭建）完成！🎊*

---

## 🧩 拓展思考：什么是更复杂的机器人运动？

> 到目前为止，我们学习了2D平面上的简单运动。那么真实的机器人是如何在**三维空间**中工作的呢？

### 从2D到3D

```
┌─────────────────────────────────────────────────────────────┐
│                    运动维度扩展                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2D平面运动                    3D空间运动                  │
│  ────────────────              ────────────────             │
│                                                             │
│     Y                              Z                       │
│     │                             /│                        │
│     │           → X               /│                        │
│     │                          ───┼──→ X                   │
│     │                         Y/                             │
│                                                             │
│  • 位置 (x, y)              • 位置 (x, y, z)              │
│  • 偏航角 θ                 • 偏航 + 俯仰 + 滚转           │
│                                                             │
│     = 3 DOF                   • = 6 DOF                   │
│     (自由度)                   (自由度)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 三维空间的运动

> **思考**：如果机器人要在三维空间中移动，需要考虑什么？

```
3D机器人运动需要考虑：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1️⃣ 位置 (Position)                                        │
│     ├── X轴平移（前后）                                    │
│     ├── Y轴平移（左右）                                    │
│     └── Z轴平移（上下） ← 爬楼梯、飞行                     │
│                                                             │
│  2️⃣ 姿态 (Orientation)                                     │
│     ├── 滚转 (Roll)  - 飞机翻滚                           │
│     ├── 俯仰 (Pitch) - 飞机抬头/低头                       │
│     └── 偏航 (Yaw)   - 船/车转弯                          │
│                                                             │
│  3️⃣ 动力学                                                │
│     ├── 重力                                               │
│     ├── 惯性                                               │
│     └── 摩擦力                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 常见的3D机器人

| 机器人 | 运动特点 | 自由度 |
|--------|---------|--------|
| 四足机器人 | 腿部运动+身体平衡 | 12+ DOF |
| 无人机 | 飞行+悬停 | 6 DOF |
| 机械臂 | 关节运动+末端定位 | 6+ DOF |
| 人形机器人 | 双足行走+全身协调 | 30+ DOF |

### 课后思考题

> 🔥 **挑战**：尝试回答以下问题

1. **四足机器人**：如果想让一只机器狗正常行走，需要控制哪些关节？最少需要几个电机？

2. **无人机**：四旋翼无人机是如何实现前后左右移动的？和车轮机器人有什么区别？

3. **机械臂**：要精确控制机械臂末端到达空间中的某个点，需要知道什么信息？

4. **平衡问题**：为什么双足机器人走路比轮子机器人更难？

---

### 📚 延伸学习

如果你对3D机器人运动感兴趣，可以了解：

- **PyBullet/Gazebo** - 3D物理仿真
- **RobotPy** - Python机器人库
- **MoveIt** - ROS机械臂规划
- **PX4** - 开源无人机软件

> 💡 **提示**：本课程的第6阶段会介绍更复杂的3D运动控制！

