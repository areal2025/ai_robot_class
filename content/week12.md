# 第12周：Sim2Real - 从仿真到现实

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 仿真环境 | Gazebo仿真环境 |
| 第2次 | 3小时 | 真机连接 | ROS2网络配置与真机控制 |

---

## 第一次课：仿真环境（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 视觉追踪回顾 |
| 讲解 | 60分钟 | Gazebo仿真 |
| 讲解 | 60分钟 | TurtleBot3仿真 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.4.1 Gazebo仿真环境

> **Gazebo** = 开源机器人仿真器 [1]。

```
Gazebo特点：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✓ 物理引擎支持（ODE, Bullet, Dart, Simbody）            │
│  ✓ 3D渲染引擎（OGRE）                                  │
│  ✓ 传感器仿真（相机, 激光雷达, IMU）                  │
│  ✓ 丰富的机器人模型库                                  │
│  ✓ 与ROS完美集成                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 安装Gazebo

```bash
# 安装Gazebo
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs

# 验证安装
gz --version

# 启动仿真世界
ros2 launch gazebo_ros gazebo.launch.py world:=empty.world
```

### 常用仿真世界

| 世界 | 命令 | 说明 |
|------|------|------|
| 空世界 | empty.world | 基础测试 |
| 小屋 | house.world | 室内导航 |
| 机器人竞赛 | roboticschool.world | 竞赛环境 |

---

## 3.4.2 TurtleBot3仿真

> **TurtleBot3** = 小型移动机器人平台 [2]。

### 安装TurtleBot3

```bash
# 安装TurtleBot3包
sudo apt update
sudo apt install ros-humble-turtlebot3
sudo apt install ros-humble-turtlebot3-simulations

# 设置环境变量
export TURTLEBOT3_MODEL=burger
source /opt/ros/humble/setup.bash
```

### 启动TurtleBot3仿真

```bash
# 启动TurtleBot3 Gazebo世界
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 或启动空世界
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

### 控制TurtleBot3

```bash
# 键盘控制
ros2 run turtlebot3_teleop teleop_keyboard

# 自主导航
ros2 launch turtlebot3_navigation2 navigation.launch.py map:=/map.yaml
```

---

## 第二次课：真机连接（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 仿真回顾 |
| 讲解 | 60分钟 | 网络配置 |
| 讲解 | 60分钟 | 真机控制 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.4.3 ROS2网络配置

### 多机通信架构

```
ROS2多机通信：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   开发电脑 (192.168.1.100)          机器人 (192.168.1.200)  │
│   ┌─────────────────┐              ┌─────────────────┐        │
│   │  RViz可视化    │ ◄───────► │  传感器节点     │        │
│   │  规划节点     │   网络    │  运动控制     │        │
│   │  决策节点     │              │  底盘驱动     │        │
│   └─────────────────┘              └─────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 网络配置步骤

```bash
# 1. 确保在同一网络
ping 192.168.1.200

# 2. 设置ROS_DOMAIN_ID（可选）
export ROS_DOMAIN_ID=42

# 3. 配置主机名
sudo nano /etc/hosts

# 添加：
# 192.168.1.200 robot

# 4. 测试话题通信
ros2 topic list  # 在开发电脑上查看机器人话题

# 5. 转发话题
ros2 topic echo /scan  # 确认能收到激光数据
```

---

## 3.4.4 机器人控制节点

```python
#!/usr/bin/env python3
"""
机器人控制节点
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RobotController(Node):
    """机器人控制器"""
    
    def __init__(self):
        super().__init__('robot_controller')
        
        # 订阅目标位置
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info('机器人控制器已启动')
    
    def move(self, linear, angular):
        """移动机器人"""
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)
    
    def stop(self):
        """停止"""
        self.move(0.0, 0.0)


def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()
    
    try:
        # 前进
        controller.move(0.2, 0.0)
        rclpy.sleep(5)
        
        # 停止
        controller.stop()
        
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 3.4.5 从仿真到真机

### 代码适配

| 仿真 | 真机 | 说明 |
|------|------|------|
| `/cmd_vel` | `/cmd_vel` | 相同 |
| `/scan` | `/scan` | 可能不同话题名 |
| 仿真时间 | 系统时间 | 使用真机时间 |
| 无延迟 | 网络延迟 | 考虑延迟补偿 |

### 常用转换

```python
# 仿真参数
SIM_PARAMS = {
    'wheel_radius': 0.033,      # 轮子半径
    'wheel_base': 0.16,         # 轮间距
    'max_linear': 0.22,         # 最大线速度
    'max_angular': 2.84,       # 最大角速度
}

# 真机参数
REAL_PARAMS = {
    'wheel_radius': 0.033,
    'wheel_base': 0.16,
    'max_linear': 0.26,
    'max_angular': 1.82,
}
```

---

## 3.4.6 常用机器人平台

### 室内移动机器人

| 平台 | 特点 | 价格 |
|------|------|------|
| TurtleBot3 | 开源教育 | $500+ |
| LoCoBot | 抓取研究 | $2000+ |
| Fetch | 机械臂+移动 | $5000+ |
| DBR10 | 国产开源 | ¥2000 |

### 轮式机器人

```
常见运动模型：

1. 差速驱动 (Differential Drive)
   - 两个独立驱动轮
   - 简单可靠
   
2. 全向驱动 (Omni Drive)
   - 麦克纳姆轮
   - 可任意方向移动

3. 阿克曼转向 (Ackermann)
   - 汽车模型
   - 需要转向机构
```

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | 启动Gazebo | 能显示仿真环境 | ☐ |
| 2 | 启动TurtleBot3 | 机器人模型显示 | ☐ |
| 3 | 控制机器人 | 键盘控制移动 | ☐ |
| 4 | 网络配置 | 多机通信 | ☐ |
| 5 | 真机控制 | 控制真实机器人 | ☐ |

---

## 参考文献

[1] Koenig, N., & Howard, A. (2004). Design and Use Paradigms for Gazebo. *IEEE/RSJ International Conference on Intelligent Robots and Systems*.

[2] Robotis. (2024). *TurtleBot3 Documentation*. Available: https://emanual.robotis.com/

---

## 期末项目预告

> **第13-15周：期末项目**
> - 选题与设计
> - 实现与调试
> - Demo Day展示

---

*第12周结束！第一学期完成！*
