# 第4周：机器人运动学基础（二维）

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 坐标系与里程计 | 坐标系概念、世界坐标vs机器人坐标、里程计 |
| 第2次 | 3小时 | 运动学演示实验 | 简单二维运动学演示、实验练习 |

---

## 第一次课：坐标系与里程计（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 上周内容回顾 |
| 讲解 | 60分钟 | 坐标系概念 |
| 讲解 | 50分钟 | 里程计原理 |
| 茶歇 | 10分钟 | 休息 |
| 演示 | 30分钟 | 实际演示 |
| 总结 | 10分钟 | 本周小结 |

---

## 2.1.1 坐标系概念（60分钟）

### 什么是坐标系？

> **坐标系** = 用来描述物体**位置和方向**的系统

```
二维平面坐标系：

         +Y (北/上)
          │
          │
          │
          │
   ───────┼─────── +X (东/右)
          │
          │
          │
```

#### 常用的坐标系

| 坐标系 | 英文 | 说明 |
|--------|------|------|
| 世界坐标系 | World Frame | 固定不变的参考系 |
| 机器人坐标系 | Robot Frame | 随机器人移动 |
| 里程计坐标系 | Odom Frame | 机器人自己计算的位置 |

### 机器人的位置表示

```
机器人在世界坐标系中的位置：

         +Y
          │
    ┌─────┼─────┐
    │  ┌──┴──┐  │
    │  │ 🤖  │  │  ← 机器人位置 (x=2, y=1)
    │  └──┬──┘  │
    └─────┼─────┘
          │
         +X

坐标表示：
• x = 2 (向右2米)
• y = 1 (向上1米)  
• θ = 30° (朝向西北方向)
```

---

## 2.1.2 世界坐标vs机器人坐标（50分钟）

### 世界坐标系（固定不变）

```
世界坐标系 = 房间里的GPS

┌─────────────────────────────────────┐
│                                      │
│         +Y (北)                      │
│          │                          │
│          │    ┌───┐                 │
│          │    │ 🤖 │ ← 机器人       │
│          │    └───┘                 │
│          │                          │
│    ──────┼───────── +X (东)         │
│          │                          │
└─────────────────────────────────────┘

特点：
• 原点固定（房间角落）
• X轴Y轴固定
• 用于标记绝对位置
```

### 机器人坐标系（相对运动）

```
机器人坐标系 = 机器人身上的指南针

机器人坐标系始终以机器人为中心：
• +X = 机器人正前方
• +Y = 机器人正左方
• +θ = 机器人逆时针方向

┌─────────────────────────────────────┐
│                                      │
│    机器人视角：                      │
│                                      │
│         +Y_robot                    │
│          │                          │
│    ────►│────── +X_robot            │
│   机器人                          │
│                                      │
└─────────────────────────────────────┘
```

### 坐标变换

```
世界坐标 → 机器人坐标

公式：
x_robot = (x_world - x_robot) * cos(θ) + (y_world - y_robot) * sin(θ)
y_robot = -(x_world - x_robot) * sin(θ) + (y_world - y_robot) * cos(θ)

其中θ是机器人的朝向角
```

---

## 2.1.3 里程计(odom)简介（30分钟）

### 什么是里程计？

> **里程计** = 机器人通过**传感器估算**自己移动了多远

```
里程计原理：

初始位置: (0, 0)
    ↓
左轮移动: 1.0米
右轮移动: 1.0米
    ↓
计算位置: (1.0, 0)
    ↓
左轮移动: 1.0米
右轮移动: 0.8米 (转左弯)
    ↓
计算位置: (1.9, 0.1)
```

### 里程计数据类型

```python
# nav_msgs/Odometry 消息
std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id  # "odom"

string child_frame_id  # "base_link"

geometry_msgs/PoseWithCovariance pose
    geometry_msgs/Pose pose
        geometry_msgs/Point position
            float64 x
            float64 y
            float64 z
        geometry_msgs/Quaternion orientation
            float64 x
            float64 y
            float64 z
            float64 w

geometry_msgs/TwistWithCovariance twist
    geometry_msgs/Twist twist
        geometry_msgs/Vector3 linear
            float64 x
            float64 y
            float64 z
        geometry_msgs/Vector3 angular
            float64 x
            float64 y
            float64 z
```

### ROS2中的里程计话题

```bash
# 查看里程计话题
ros2 topic list | grep odom

# 监听里程计
ros2 topic echo /odom

# 输出示例：
# pose:
#   pose:
#     position:
#       x: 1.234
#       y: 0.567
#       z: 0.0
#     orientation:
#       x: 0.0
#       y: 0.0
#       z: 0.123
#       w: 0.992
```

---

## 第二次课：运动学演示实验（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 提问巩固 |
| 演示 | 40分钟 | Turtlesim里程计演示 |
| 实践 | 80分钟 | 学生动手实验 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 综合练习 |

---

## 2.1.4 简单二维运动学演示（40分钟）

### 实验1：查看Turtlesim里程计

```bash
# 启动Turtlesim
ros2 run turtlesim turtlesim_node

# 监听里程计话题
ros2 topic echo /turtle1/pose
```

### 实验2：观察坐标变化

```
移动前：
x: 5.44, y: 5.44, theta: 0.0

按↑键前进一次后：
x: 5.44, y: 6.44, theta: 0.0

按←键左转后：
x: 5.44, y: 6.44, theta: 1.57 (90°)
```

### 运动学公式

```python
# 差速驱动机器人的运动学

# 线速度
v = (v_left + v_right) / 2

# 角速度  

### 🎮 PyBullet 3D运动学演示（进阶）

> 除了Turtlesim，我们还可以用PyBullet看更真实的3D机器人运动！

#### PyBullet 3D小车仿真

```python
#!/usr/bin/env python3
"""
PyBullet 3D机器人运动学演示
"""

import pybullet as p
import pybullet_data
import time
import math

# 连接仿真
client_id = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 加载地面
p.loadURDF("plane.urdf")

# 创建机器人（小车）
def create_robot():
    # 车身
    chassis = p.createCollisionShape(p.BoxShape, halfExtents=[0.3, 0.2, 0.1])
    chassis_mass = 1.0
    chassis_id = p.createMultiBody(
        chassisMass=chassis_mass,
        baseCollisionShapeIndex=chassis,
        basePosition=[0, 0, 0.2]
    )
    
    # 左轮
    left_wheel = p.createCollisionShape(p.CylinderShape, radius=0.1, height=0.05)
    left_wheel_idx = p.createMultiBody(
        baseMass=0.2,
        baseCollisionShapeIndex=left_wheel,
        basePosition=[0.3, 0.25, 0.1],
        baseOrientation=[0, 0, 0, 1]
    )
    
    # 右轮
    right_wheel = p.createCollisionShape(p.CylinderShape, radius=0.1, height=0.05)
    right_wheel_idx = p.createMultiBody(
        baseMass=0.2,
        baseCollisionShapeIndex=right_wheel,
        basePosition=[-0.3, 0.25, 0.1],
        baseOrientation=[0, 0, 0, 1]
    )
    
    # 连接轮子和车身
    p.createConstraint(
        chassis_id, -1, left_wheel_idx, -1,
        p.JOINT_POINT2POINT,
        [0, 0.25, 0], [0.15, 0, 0]
    )
    p.createConstraint(
        chassis_id, -1, right_wheel_idx, -1,
        p.JOINT_POINT2POINT,
        [0, -0.25, 0], [0.15, 0, 0]
    )
    
    return chassis_id, left_wheel_idx, right_wheel_idx

robot, left_wheel, right_wheel = create_robot()

# 运动学参数
wheel_radius = 0.1  # 轮子半径 (m)
wheel_base = 0.5   # 轮间距 (m)

# 控制函数
def move_robot(linear_vel, angular_vel, dt=0.1):
    """
    运动学：计算轮速
    v = (v_l + v_r) / 2
    ω = (v_r - v_l) / L
    """
    # 计算左右轮速度
    v_right = (2 * linear_vel + angular_vel * wheel_base) / 2
    v_left = (2 * linear_vel - angular_vel * wheel_base) / 2
    
    # 设置轮子速度
    p.setJointMotorControl2(robot, left_wheel, p.VELOCITY_CONTROL, targetVelocity=v_left)
    p.setJointMotorControl2(robot, right_wheel, p.VELOCITY_CONTROL, targetVelocity=v_right)
    
    return v_left, v_right

print("3D机器人运动学演示")
print("=" * 50)

# 演示1：走直线
print("\n演示1：前进1米")
v_l, v_r = move_robot(0.5, 0)  # 0.5m/s前进
print(f"左轮速度: {v_l:.2f} m/s, 右轮速度: {v_r:.2f} m/s")

for _ in range(240):  # 约1秒
    p.stepSimulation()
    time.sleep(1./240.)

# 演示2：画圆
print("\n演示2：画圆（半径1米）")
# v = r × ω => ω = v/r = 0.5/1 = 0.5 rad/s
v_l, v_r = move_robot(0.5, 0.5)  # 0.5m/s, 0.5rad/s
print(f"左轮速度: {v_l:.2f} m/s, 右轮速度: {v_r:.2f} m/s")

for _ in range(1250):  # 约5秒
    p.stepSimulation()
    time.sleep(1./240.)

# 停止
move_robot(0, 0)
print("\n演示结束！")

# 读取位置
pos, orn = p.getBasePositionAndOrientation(robot)
print(f"最终位置: x={pos[0]:.2f}, y={pos[1]:.2f}, z={pos[2]:.2f}")
```

#### 运动学公式回顾

```
┌─────────────────────────────────────────────────────────────┐
│                    运动学公式                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  线速度: v = (v_l + v_r) / 2                             │
│                                                             │
│  角速度: ω = (v_r - v_l) / L                             │
│           (L = 轮间距)                                      │
│                                                             │
│  反推轮速:                                                  │
│  v_r = v + ω × L / 2                                      │
│  v_l = v - ω × L / 2                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

ω = (v_right - v_left) / wheel_base

# 位置更新
x_new = x_old + v * cos(θ) * dt
y_new = y_old + v * sin(θ) * dt
θ_new = θ_old + ω * dt
```

---

## 2.1.5 编程实践（80分钟）

### 编写里程计读取节点

```python
#!/usr/bin/env python3
"""
读取Turtlesim的里程计数据
"""

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class PoseReader(Node):
    """读取位置信息的节点"""
    
    def __init__(self):
        super().__init__('pose_reader')
        
        # 订阅/turtle1/pose话题
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        self.get_logger().info('位置读取节点已启动！')
    
    def pose_callback(self, msg):
        """回调函数：收到位置数据时调用"""
        self.get_logger().info(
            f'位置: x={msg.x:.2f}, y={msg.y:.2f}, '
            f'角度: {msg.theta:.2f} rad ({msg.theta*180/3.14:.1f}°)'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PoseReader()
    
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

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | 启动Turtlesim | 正常运行 | ☐ |
| 2 | 监听/turtle1/pose | 能看到实时坐标 | ☐ |
| 3 | 移动观察坐标变化 | 记录移动前后的坐标 | ☐ |
| 4 | 运行PoseReader节点 | 能打印位置信息 | ☐ |
| 5 | 理解坐标系转换 | 能说清世界坐标vs机器人坐标 | ☐ |

---

## 本周作业

### 📝 理论题

1. 解释世界坐标系和机器人坐标系的区别
2. 里程计是如何计算机器人位置的？

### 📐 计算题

已知：机器人左轮速度0.5m/s，右轮速度1.0m/s，轮间距0.5m
- 计算线速度v
- 计算角速度ω
- 计算机器人1秒后的位置变化

### 💻 实践题

编写一个节点，实时显示小乌龟距离原点的距离

---

## 知识点速查表

```
┌─────────────────────────────────────────────────────────────┐
│                    第4周知识点速查                           │
├─────────────────────────────────────────────────────────────┤
│  概念                                                          │
│  ├── 坐标系 = 描述位置和方向的系统                           │
│  ├── 世界坐标 = 固定不变的参考系                            │
│  ├── 机器人坐标 = 随机器人移动的坐标系                       │
│  └── 里程计 = 通过传感器估算移动距离                        │
├─────────────────────────────────────────────────────────────┤
│  公式                                                          │
│  ├── v = (v_l + v_r) / 2    (线速度)                      │
│  ├── ω = (v_r - v_l) / L    (角速度，L=轮间距)            │
│  └── x_new = x + v*cos(θ)*dt                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 课后阅读

- [ROS2坐标变换文档](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)
- [机器人运动学基础](https://en.wikipedia.org/wiki/Kinematics)

---

## 下周预告

> **第5周：传感器与感知基础**
> - 激光雷达介绍
> - 相机与图像
> - RViz可视化

---

*第4周结束！*
