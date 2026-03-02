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


## 1.1 Python基础回顾（60分钟）

> Python是一种高级、解释型、面向对象的编程语言。由Guido van Rossum于1991年首次发布。Python以其简洁的语法和强大的功能而闻名，广泛应用于Web开发、数据科学、人工智能、机器人等领域 [1]。

### 1.1.1 变量和数据类型

#### 1. 数值类型

Python支持多种数值类型：

```python
# 整数 (int) - 没有小数点的数
age = 25
distance = 100
count = -5

# 浮点数 (float) - 带小数点的数
speed = 1.5          # 线速度 m/s
angular_velocity = 0.5  # 角速度 rad/s
temperature = 36.5

# 复数 (complex)
complex_num = 3 + 4j
```

> **注意**：在机器人控制中，浮点数精度对运动精度有重要影响。Python使用IEEE 754双精度浮点数 [2]。

#### 2. 字符串 (str)

```python
# 字符串创建
name = "turtle"              # 双引号
message = 'Hello Robot'       # 单引号
multi_line = """这是
多行字符串"""               # 三引号

# 字符串操作
robot_name = "TurtleBot3"
print(len(robot_name))       # 长度: 10
print(robot_name.upper())     # TURTLEBOT3
print(robot_name[0])          # T (索引)

# 格式化
speed = 1.5
print(f"速度: {speed} m/s")   # f-string格式化
```

#### 3. 布尔值 (bool)

```python
is_moving = True
is_stopped = False

# 布尔运算
result = (speed > 0) and (angular_velocity == 0)
```

#### 4. 列表 (list)

列表是Python中最常用的数据结构，用于存储有序的元素序列：

```python
# 创建列表
colors = ["red", "green", "blue"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 访问元素（索引从0开始）
print(colors[0])     # red
print(colors[-1])   # blue (最后一个)

# 切片操作
print(numbers[1:4])  # [2, 3, 4]
print(numbers[:3])   # [1, 2, 3]
print(numbers[::2])  # [1, 3, 5] (步长为2)

# 修改列表
colors.append("yellow")    # 添加
colors.insert(0, "white")  # 插入
colors.remove("red")       # 删除

# 遍历列表
for color in colors:
    print(color)
```

#### 5. 字典 (dict)

字典是键值对的无序集合：

```python
# 创建字典
robot = {
    "name": "TurtleBot3",
    "speed": 1.0,
    "battery": 80,
    "sensors": ["camera", "lidar"]
}

# 访问值
print(robot["name"])           # TurtleBot3
print(robot.get("battery"))    # 80

# 修改
robot["battery"] = 75
robot["status"] = "moving"

# 遍历
for key, value in robot.items():
    print(f"{key}: {value}")
```

### 1.1.2 函数

函数是组织代码的基本单元，可以提高代码的可重用性和可读性 [3]。

#### 函数定义与调用

```python
def function_name(parameters):
    """函数文档字符串
    
    描述函数的功能、参数和返回值
    
    Args:
        param1: 参数1的说明
        param2: 参数2的说明
    
    Returns:
        返回值的说明
    """
    # 函数体
    return value  # 返回值（可选）
```

#### 参数类型

```python
# 位置参数
def move_robot(speed, duration):
    """移动机器人指定时间"""
    distance = speed * duration
    return distance

# 关键字参数
result = move_robot(speed=1.0, duration=2.0)

# 默认参数
def create_robot(name, speed=1.0, battery=100):
    """创建机器人"""
    return {"name": name, "speed": speed, "battery": battery}

# 可变参数
def sum_all(*args):
    """求和"""
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3, 4, 5))  # 15
```

#### Lambda函数（匿名函数）

```python
# Lambda函数 - 简单的单行函数
square = lambda x: x ** 2
print(square(5))  # 25

# 在列表排序中使用
robots = [{"name": "A", "speed": 1.0}, {"name": "B", "speed": 2.0}]
sorted_robots = sorted(robots, key=lambda x: x["speed"])
```

### 1.1.3 类（面向对象编程）

面向对象编程(OOP)是一种将数据和操作数据的方法封装在一起的编程范式 [4]。在ROS2中，所有节点都是类。

#### 类的定义与实例化

```python
class Robot:
    """机器人基类
    
    用于表示具有基本运动能力的机器人设备。
    
    Attributes:
        name: 机器人名称
        speed: 当前速度 (m/s)
        battery: 电池电量 (0-100)
    """
    
    # 类属性（所有实例共享）
    robot_type = "differential_drive"
    
    # 构造函数（初始化方法）
    def __init__(self, name, battery=100):
        """初始化机器人
        
        Args:
            name: 机器人名称
            battery: 初始电量，默认为100
        """
        # 实例属性
        self.name = name
        self.battery = battery
        self.speed = 0.0
        self.is_moving = False
        
        print(f"机器人 {name} 已创建")
    
    # 实例方法
    def move(self, speed):
        """移动机器人
        
        Args:
            speed: 线速度 (m/s)，正值向前，负值向后
        """
        if self.battery <= 0:
            print("电量不足，无法移动")
            return
        
        self.speed = speed
        self.is_moving = speed != 0
        print(f"{self.name} 以 {speed} m/s 移动")
    
    def stop(self):
        """停止机器人"""
        self.speed = 0
        self.is_moving = False
        print(f"{self.name} 已停止")
    
    def get_status(self):
        """获取机器人状态
        
        Returns:
            dict: 包含名称、速度、电量、状态的字典
        """
        return {
            "name": self.name,
            "speed": self.speed,
            "battery": self.battery,
            "is_moving": self.is_moving
        }
    
    # 析构函数
    def __del__(self):
        """对象销毁时调用"""
        print(f"机器人 {self.name} 已销毁")


# 创建实例
my_robot = Robot("TurtleBot", battery=80)

# 调用方法
my_robot.move(1.0)
my_robot.stop()

# 获取状态
status = my_robot.get_status()
print(status)
```

#### 继承

```python
class AdvancedRobot(Robot):
    """高级机器人，继承自Robot基类"""
    
    def __init__(self, name, battery=100, sensors=None):
        """初始化高级机器人"""
        super().__init__(name, battery)  # 调用父类构造函数
        self.sensors = sensors if sensors else []
    
    def detect_obstacle(self):
        """障碍物检测"""
        print(f"{self.name} 正在检测障碍物")
        return True
    
    # 方法重写
    def move(self, speed):
        """重写移动方法，添加电池检查"""
        if self.battery < 10:
            print("电量过低，进入节能模式")
            speed = speed * 0.5
        super().move(speed)  # 调用父类方法
```

### 1.1.4 控制流

#### 条件语句

```python
speed = 1.5

if speed > 0:
    print("前进")
elif speed < 0:
    print("后退")
else:
    print("停止")

# 三元表达式
direction = "forward" if speed > 0 else "backward"
```

#### 循环

```python
# for循环 - 遍历列表
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

# 遍历字典
robot = {"name": "Bot", "speed": 1.0}
for key, value in robot.items():
    print(f"{key}: {value}")

# while循环
count = 0
while count < 5:
    print(count)
    count += 1

# 循环控制
for i in range(10):
    if i == 3:
        continue  # 跳过本次循环
    if i == 7:
        break     # 退出循环
    print(i)
```

### 1.1.5 模块与导入

Python的强大之处在于其丰富的模块生态系统 [5]：

```python
# 导入模块
import math
import time
import random

# 导入特定函数
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# 使用别名
import numpy as np
import rospy as rp
```

### 1.1.6 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    print("总是执行")
```

### 参考文献

[1] Van Rossum, G. (1995). *Python tutorial*. Centrum Wiskunde & Informatica. Available: https://www.python.org/

[2] IEEE Computer Society. (2008). *IEEE Standard for Floating-Point Arithmetic*. IEEE Std 754-2008. doi:10.1109/IEEESTD.2008.4610935

[3] Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media. ISBN: 978-1449355722

[4] Martin, R.C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. ISBN: 978-0132350884

[5] Python Software Foundation. (2024). *Python Standard Library*. Available: https://docs.python.org/3/library/




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

## 1.4 PyBullet仿真环境介绍

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



---

### 参考文献

[1] Coumans, E. (2024). *Bullet Physics Simulation*. Available: https://pybullet.org/

[2] Fei, Y. (2022). PyBullet: A Python Module for Physics Simulation. *Journal of Open Source Software*. doi:10.21105/joss.04362

[3]松井藤太. (2023). *PyBullet Robotics Tutorial*. Available: https://github.com/jefflesser/pybullet-ros



## 1.5 Python + OpenClaw集成控制

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

## 1.6 复杂机器人运动简介

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

