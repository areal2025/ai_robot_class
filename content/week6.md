# 第6周：闭环控制初探

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 闭环控制原理 | 什么是闭环控制、反馈原理 |
| 第2次 | 3小时 | 避障逻辑实现 | 简单避障编程、实验 |

---

## 第一次课：闭环控制原理（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 上周内容回顾 |
| 讲解 | 60分钟 | 开环vs闭环 |
| 讲解 | 60分钟 | 反馈控制原理 |
| 茶歇 | 10分钟 | 休息 |
| 演示 | 30分钟 | 演示简单闭环 |

---

## 2.3.1 什么是闭环控制（60分钟）

### 开环控制系统

> **开环** = 只管发送命令，不管结果

```
开环控制：

┌──────────┐      命令       ┌──────────┐
│ 控制器   │ ─────────────► │ 执行器   │ ──────► 机器人
└──────────┘                └──────────┘
        ▲                         │
        │                         │
        │   结果如何？不知道！    │
        │                         │
        └─────────────────────────┘
        
特点：
• 简单
• 不管结果
• 适用于精度要求不高的场景
```

### 闭环控制系统

> **闭环** = 发送命令后，检查结果，根据误差调整

```
闭环控制（反馈控制）：

┌──────────┐      命令       ┌──────────┐
│ 控制器   │ ─────────────► │ 执行器   │ ──────► 机器人
└──────────┘                └──────────┘
        ▲                         │
        │                         ▼
        │                   ┌──────────┐
        │                   │ 传感器   │
        │                   └────┬─────┘
        │                        │
        │                   测量位置/速度
        │                        │
        │                        ▼
        │                   ┌──────────┐
        └─────────────────── │ 比较器   │ ◄── 期望值
                             └──────────┘
                                      ▲
                                      │
                                 设定目标
                                      │
                                      
特点：
• 精确
• 能纠正误差
• 复杂但可靠
```

### 生活中的闭环控制

| 开环例子 | 闭环例子 |
|---------|---------|
| 洗衣机定时洗涤 | 空调恒温 |
| 风扇档位 | 电饭煲保温 |
| 手动灌溉 | 自动驾驶 |

---

## 2.3.2 传感器数据与控制结合（60分钟）

### 机器人闭环控制流程

```
机器人闭环控制流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    设定目标                                                 │
│    (如：前进2米)                                            │
│         │                                                   │
│         ▼                                                   │
│    ┌─────────────┐                                          │
│    │  控制器     │ ← 计算误差                               │
│    │ (PID等)    │   误差 = 目标 - 实际                     │
│    └──────┬──────┘                                          │
│             │                                                │
│             ▼ 命令                                           │
│    ┌─────────────┐                                          │
│    │   执行器    │ → 发送速度命令                           │
│    │ (电机驱动) │                                            │
│    └──────┬──────┘                                          │
│             │                                                │
│             ▼                                               │
│    ┌─────────────┐                                          │
│    │   机器人    │ ← 执行运动                               │
│    └──────┬──────┘                                          │
│             │                                                │
│             ▼ 测量                                          │
│    ┌─────────────┐                                          │
│    │   传感器    │ → 读取里程计/编码器                      │
│    │ (里程计)   │                                            │
│    └─────────────┘                                          │
│             │                                                │
│             └──────► 返回"误差计算" ◄── 反馈              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```



### PID控制器的LaTeX表示

$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de}{dt}$$

其中：
- $u(t)$ = 控制器输出
- $e(t)$ = 误差 (目标值 - 实际值)
- $K_p$ = 比例增益
- $K_i$ = 积分增益
- $K_d$ = 微分增益

### PID控制器简介

> **PID** = Proportional（比例）+ Integral（积分）+ Derivative（微分）

```python
# PID控制公式

# 输出 = Kp * e + Ki * ∫e dt + Kd * de/dt

# 其中：
# e = 误差（目标值 - 实际值）
# Kp = 比例系数（响应速度）
# Ki = 积分系数（消除稳态误差）
# Kd = 微分系数（抑制振荡）

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
    
    def compute(self, target, actual, dt):
        # 计算误差
        self.error = target - actual
        
        # 积分项
        self.integral += self.error * dt
        
        # 微分项
        self.derivative = (self.error - self.last_error) / dt
        self.last_error = self.error
        
        # PID输出
        output = (self.kp * self.error + 
                  self.ki * self.integral + 
                  self.kd * self.derivative)
        
        return output
```

---

## 第二次课：避障逻辑实现（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 闭环控制概念 |
| 讲解 | 40分钟 | 避障逻辑原理 |
| 演示 | 30分钟 | 演示避障 |
| 实践 | 80分钟 | 编程实验 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 综合练习 |

---

## 2.3.3 简单避障逻辑（40分钟）

### 避障原理

```
避障流程：

    ┌─────────────────┐
    │ 开始            │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 读取前方距离    │ ← 传感器测量
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 距离 < 阈值？    │ ← 判断
    └────────┬────────┘
             │
      ┌──────┴──────┐
      │ 是           │ 否
      ▼              ▼
┌───────────┐  ┌───────────┐
│  停止     │  │  继续前进  │
│  后退     │  └───────────┘
│  转向     │
└─────┬─────┘
      │
      ▼
┌───────────┐
│ 重新检测  │
└───────────┘
```

### 伪代码

```
伪代码：简单避障

while True:
    distance = read_sensor()  # 读取传感器
    
    if distance < THRESHOLD:  # 如果距离太近
        stop()                 # 停止
        backward(0.5)         # 后退
        turn(90)              # 转弯
    else:                     # 否则
        forward(1.0)         # 继续前进
    
    sleep(0.1)
```

---

## 2.3.4 实现"撞不到墙"（80分钟）

### 完整避障代码

```python
#!/usr/bin/env python3
"""
简单避障机器人
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class BumperRobot(Node):
    """简单避障机器人"""
    
    def __init__(self):
        super().__init__('bumper_robot')
        
        # 速度发布者
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 激光雷达订阅者
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # 参数
        self.SAFE_DISTANCE = 0.3  # 安全距离 0.3米
        self.FORWARD_SPEED = 0.2   # 前进速度
        self.BACK_SPEED = -0.1     # 后退速度
        self.TURN_SPEED = 0.5      # 转向速度
        
        # 标志位
        self.obstacle_detected = False
        
        # 定时器
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info('避障机器人启动！')
    
    def scan_callback(self, msg):
        """激光雷达回调"""
        # 获取前方距离
        # 激光雷达前方大约在0度附近
        min_distance = min(msg.ranges)
        
        if min_distance < self.SAFE_DISTANCE:
            self.obstacle_detected = True
            self.get_logger().warn(f'检测到障碍物！距离: {min_distance:.2f}m')
        else:
            self.obstacle_detected = False
    
    def control_loop(self):
        """控制循环"""
        msg = Twist()
        
        if self.obstacle_detected:
            # 有障碍物：后退+转向
            msg.linear.x = self.BACK_SPEED
            msg.angular.z = self.TURN_SPEED
            self.get_logger().info('障碍物！后退并转向...')
        else:
            # 无障碍物：前进
            msg.linear.x = self.FORWARD_SPEED
            msg.angular.z = 0.0
        
        self.cmd_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = BumperRobot()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 停止机器人
        msg = Twist()
        node.cmd_pub.publish(msg)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 2.3.5 实验（60分钟）

### 实验1：测试避障

```bash
# 启动Gazebo仿真
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 运行避障节点
python3 bumper_robot.py
```

### 实验2：调整参数

```python
# 调整安全距离
self.SAFE_DISTANCE = 0.5  # 原来是0.3

# 调整速度
self.FORWARD_SPEED = 0.3  # 原来是0.2
```

### 实验3：改进避障

```python
# 改进：区分左转还是右转
def control_loop(self):
    msg = Twist()
    
    # 获取左右方向的距离
    left_dist = min(self.scan_msg.ranges[0:180])
    right_dist = min(self.scan_msg.ranges[180:360])
    
    if self.obstacle_detected:
        # 向障碍物少的方向转
        if left_dist > right_dist:
            msg.angular.z = self.TURN_SPEED  # 左转
        else:
            msg.angular.z = -self.TURN_SPEED # 右转
```

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | 理解开环vs闭环 | 能解释区别 | ☐ |
| 2 | 理解PID控制 | 能说各部分作用 | ☐ |
| 3 | 运行避障代码 | 能看到效果 | ☐ |
| 4 | 调整安全距离 | 观察行为变化 | ☐ |
| 5 | 改进避障逻辑 | 区分左右转 | ☐ |

---

## 本周作业

### 📝 理论题

1. 解释什么是闭环控制
2. PID控制器各部分的作用是什么？

### 💻 实践题

1. 修改代码，实现遇到障碍物时三次后退+左转

---

## 知识点速查表

```
┌─────────────────────────────────────────────────────────────┐
│                    第6周知识点速查                           │
├─────────────────────────────────────────────────────────────┤
│  概念                                                          │
│  ├── 开环 = 发送命令不管结果                                │
│  ├── 闭环 = 反馈控制，根据误差调整                         │
│  ├── PID = 比例+积分+微分                                   │
│  └── 避障 = 检测障碍物 → 停止/转向                        │
├─────────────────────────────────────────────────────────────┤
│  公式                                                          │
│  └── PID输出 = Kp*e + Ki*∫e*dt + Kd*de/dt               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 课后阅读

- [PID控制器原理](https://en.wikipedia.org/wiki/PID_controller)
- [ROS2控制教程](https://docs.ros.org/en/humble/Tutorials/Intermediate/Control/)

---

## 下周预告

> **第7周：复习与实操演练**
> - 前半学期知识总复习
> - 模拟练习

---

*第6周结束！*
