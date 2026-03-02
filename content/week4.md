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



### 2D坐标系图示

<svg width="300" height="250" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="300" height="250" fill="#f8f9fa"/>
  
  <!-- Grid lines -->
  <line x1="30" y1="30" x2="280" y2="30" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="30" y1="80" x2="280" y2="80" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="30" y1="130" x2="280" y2="130" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="30" y1="180" x2="280" y2="180" stroke="#e0e0e0" stroke-width="1"/>
  
  <line x1="30" y1="30" x2="30" y2="230" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="80" y1="30" x2="80" y2="230" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="130" y1="30" x2="130" y2="230" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="180" y1="30" x2="180" y2="230" stroke="#e0e0e0" stroke-width="1"/>
  <line x1="230" y1="30" x2="230" y2="230" stroke="#e0e0e0" stroke-width="1"/>
  
  <!-- Axes -->
  <line x1="30" y1="200" x2="280" y2="200" stroke="black" stroke-width="2"/>
  <line x1="30" y1="200" x2="30" y2="50" stroke="black" stroke-width="2"/>
  
  <!-- Arrow heads -->
  <polygon points="280,200 270,195 270,205" fill="black"/>
  <polygon points="30,50 25,60 35,60" fill="black"/>
  
  <!-- Axis labels -->
  <text x="260" y="220" font-size="16" fill="black">X</text>
  <text x="15" y="55" font-size="16" fill="black">Y</text>
  
  <!-- Origin -->
  <text x="40" y="220" font-size="12" fill="#666">(0,0)</text>
  
  <!-- Robot position -->
  <circle cx="150" cy="120" r="15" fill="#3498db" opacity="0.7"/>
  <text x="135" y="125" font-size="10" fill="white">Robot</text>
  
  <!-- Position vector -->
  <line x1="30" y1="200" x2="150" y2="120" stroke="#e74c3c" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="80" y="170" font-size="11" fill="#e74c3c">P(x,y)</text>
  
  <!-- Theta arrow -->
  <path d="M 150 155 Q 170 165 165 180" stroke="green" fill="none" stroke-width="2"/>
  <text x="170" y="175" font-size="11" fill="green">θ</text>
</svg>


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



### LaTeX公式表示

运动学基本公式：

$$v = \frac{v_l + v_r}{2}$$

$$\omega = \frac{v_r - v_l}{L}$$

其中：
- $v$ = 线速度 (m/s)
- $v_l, v_r$ = 左/右轮速度 (m/s)
- $\omega$ = 角速度 (rad/s)
- $L$ = 轮间距 (m)

位置更新公式：

$$x_{new} = x + v \cdot \cos(\theta) \cdot \Delta t$$

$$y_{new} = y + v \cdot \sin(\theta) \cdot \Delta t$$

$$\theta_{new} = \theta + \omega \cdot \Delta t$$


### 运动学公式

```python
# 差速驱动机器人的运动学

# 线速度
v = (v_left + v_right) / 2

# 角速度  

#

---

### 参考文献

[1] Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson Education. ISBN: 978-0201543613

[2] Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. John Wiley & Sons. ISBN: 978-0471649908

[3] Siciliano, B., Khatib, O., & Kröger, T. (2008). *Springer Handbook of Robotics*. Springer. doi:10.1007/978-3-540-30301-5

[4] Featherstone, R. (2014). *Rigid Body Dynamics Algorithms*. Springer. ISBN: 978-0387743141

[5] Tsai, R. W. (1999). *A Computational Introduction to Robotics*. Springer. ISBN: 978-0387985016


## 🎮 PyBullet 3D运动学演示（进阶）

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

#

### LaTeX公式表示

运动学基本公式：

$$v = \frac{v_l + v_r}{2}$$

$$\omega = \frac{v_r - v_l}{L}$$

其中：
- $v$ = 线速度 (m/s)
- $v_l, v_r$ = 左/右轮速度 (m/s)
- $\omega$ = 角速度 (rad/s)
- $L$ = 轮间距 (m)

位置更新公式：

$$x_{new} = x + v \cdot \cos(\theta) \cdot \Delta t$$

$$y_{new} = y + v \cdot \sin(\theta) \cdot \Delta t$$

$$\theta_{new} = \theta + \omega \cdot \Delta t$$


### 运动学公式回顾

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

---

## 🧠 拓展思考：逆运动学

> 除了让机器人**按给定速度移动**（正运动学），我们还可以**反着来**——给定目标位置，计算需要的关节角度！

### 什么是逆运动学？

```
┌─────────────────────────────────────────────────────────────┐
│                    正运动学 vs 逆运动学                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  正运动学 (Forward Kinematics)                              │
│  ───────────────────────────────────────                   │
│  输入：关节角度 [θ₁, θ₂, θ₃]                                │
│  输出：末端位置 (x, y, z)                                   │
│                                                             │
│  示例：给定关节角度 → 计算手在哪里                            │
│                                                             │
│  ───────────────────────────────────────                   │
│                                                             │
│  逆运动学 (Inverse Kinematics)                             │
│  ───────────────────────────────────────                   │
│  输入：末端位置 (x, y, z)                                   │
│  输出：关节角度 [θ₁, θ₂, θ₃]                                │
│                                                             │
│  示例：想要手到达这里 → 计算关节要转多少                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 生活中的例子

```
伸手拿水杯：

正运动学：      你转动肩膀、肘部、手腕 → 手到达某个位置
              （关节角度 → 末端位置）

逆运动学：      你想让手碰到水杯 → 大脑计算各关节要转多少
              （目标位置 → 关节角度）
```

### 简单的2关节机械臂

```
机械臂几何：

        末端
         │
    L2   │  θ₂
    ─────┤
         │
    θ₁   │
─────────┼─────────
   L1    │   基座
         │
         
参数：
- L1 = 上臂长度 (比如1米)
- L2 = 前臂长度 (比如1米)
- θ₁ = 肩关节角度
- θ₂ = 肘关节角度
```

#### 正运动学公式

```
已知：θ₁ = 45°, θ₂ = 45°, L1 = L2 = 1m

计算末端位置：

x = L1 × cos(θ₁) + L2 × cos(θ₁ + θ₂)
y = L1 × sin(θ₁) + L2 × sin(θ₁ + θ₂)

代入：
x = 1 × cos(45°) + 1 × cos(90°)
  = 0.707 + 0 = 0.707m

y = 1 × sin(45°) + 1 × sin(90°)
  = 0.707 + 1 = 1.707m
```

#### 逆运动学公式（简化版）

```
已知：目标位置 (x, y) = (0.5, 1.5m)

求解关节角度（简化）：

θ₂ = arccos((x² + y² - L1² - L2²) / (2 × L1 × L2))

θ₁ = atan2(y, x) - atan2(L2 × sin(θ₂), L1 + L2 × cos(θ₂))

这是一个非线性方程组，通常用数值方法求解！
```

### Python计算示例

```python
import math

def forward_kinematics(theta1, theta2, L1=1.0, L2=1.0):
    """正运动学：关节角度 → 末端位置"""
    x = L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2)
    y = L1 * math.sin(theta1) + L2 * math.sin(theta1 + theta2)
    return x, y

def inverse_kinematics(x, y, L1=1.0, L2=1.0):
    """逆运动学：末端位置 → 关节角度"""
    # 计算肘部角度
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    # 限制范围避免数值误差
    cos_theta2 = max(-1, min(1, cos_theta2))
    theta2 = math.acos(cos_theta2)
    
    # 计算肩部角度
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)
    
    return theta1, theta2

# 示例
theta1, theta2 = 0, 0  # 初始角度
x, y = forward_kinematics(theta1, theta2)
print(f"正运动学: θ1={theta1:.2f}, θ2={theta2:.2f} → 末端位置=({x:.2f}, {y:.2f})")

# 逆运动学
target_x, target_y = 1.0, 1.0
theta1, theta2 = inverse_kinematics(target_x, target_y)
print(f"逆运动学: 目标=({target_x}, {target_y}) → θ1={math.degrees(theta1):.1f}°, θ2={math.degrees(theta2):.1f}°")
```

### 关节叠加效应

```
演示：不同关节角度如何叠加

┌─────────────────────────────────────────────────────────────┐
│  关节1旋转45°                                            │
│  ──────────────────                                       │
│          ╱                                                │
│         ╱  关节2也在旋转                                  │
│        ╱ ──────────                                       │
│       ╱                                                   │
│      ╱                                                    │
│     ╱                                                     │
│    ─                                                        │
│                                                             │
│  结果：末端位置 = 关节1效果 + 关节2效果 + 交叉项           │
│                                                             │
│  x = L1×cos(θ1) + L2×cos(θ1+θ2)                        │
│       └────────┘    └─────────────┘                      │
│         单独效果      叠加效果                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 关节叠加的物理意义

```python
"""
关节叠加效应演示
"""

import math
import matplotlib.pyplot as plt

L1 = 1.0
L2 = 1.0

# 只动关节1
theta1_range = [math.radians(a) for a in range(0, 91)]
x1_only = [L1 * math.cos(t) + L2 * math.cos(t) for t in theta1_range]
y1_only = [L1 * math.sin(t) + L2 * math.sin(t) for t in theta1_range]

# 两个关节同时动
theta2_range = [math.radians(a) for a in range(0, 91)]
x_both = [L1 * math.cos(t) + L2 * math.cos(t*2) for t in theta1_range]
y_both = [L1 * math.sin(t) + L2 * math.sin(t*2) for t in theta1_range]

print("关节1单独运动 vs 两个关节叠加运动：")
print("\n角度   只动关节1       两个关节同时动")
print("-" * 50)
for i in range(0, 91, 30):
    print(f"{i}°    ({x1_only[i]:.2f}, {y1_only[i]:.2f})    ({x_both[i]:.2f}, {y_both[i]:.2f})")
```

## 📐 自由度的定义

> 自由度(DOF = Degrees of Freedom)是机器人学中最重要的概念之一！

### 什么是自由度？

> **自由度** = 机器人**独立运动**的数目

```
┌─────────────────────────────────────────────────────────────┐
│                    例子：从1D到3D                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1D (1自由度)                                              │
│  ─────────────                                             │
│  只能来回移动                                               │
│  ○──────────○                                               │
│  ←────────→                                                │
│                                                             │
│  ────────────────────────────────────────────────────────   │
│                                                             │
│  2D (3自由度)                                              │
│  ─────────────                                             │
│  可以在平面移动 + 旋转                                       │
│          ↑                                                  │
│     ↖   │   ↗                                             │
│      │  │  │                                              │
│  ←────┼──┼──→                                              │
│      │  │  │                                              │
│     ↙   │   ↘                                             │
│          ↓                                                  │
│  位置(x,y) + 方向(θ) = 3个自由度                         │
│                                                             │
│  ────────────────────────────────────────────────────────   │
│                                                             │
│  3D (6自由度)                                              │
│  ─────────────                                             │
│  空间移动 + 空间旋转                                        │
│                                                             │
│  位置(x,y,z) + 姿态(Roll,Pitch,Yaw) = 6个自由度           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 机器人自由度

| 机器人类型 | 典型自由度 | 说明 |
|------------|-----------|------|------|
| 差速驱动小车 | 2 | x,y位移 |
| 全向移动机器人 | 3 | x,y位移 + 旋转 |
| 机械臂(6轴) | 6 | 6个关节 |
| 四足机器人 | 12+ | 每条腿3个关节 |
| 人形机器人 | 30+ | 全身关节 |
| 无人机 | 6 | 位置+姿态 |

### 自由度 vs 关节数

```
┌─────────────────────────────────────────────────────────────┐
│  常见误解：自由度 = 关节数                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  实际上：                                                   │
│  • 关节数 ≥ 自由度数（冗余）                               │
│  • 可以有"冗余自由度"（比如7轴机械臂 > 6个末端自由度）    │
│  • 冗余机械臂更灵活，可以避开障碍物                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2D vs 3D 运动

| 维度 | 位置 | 姿态 | 总自由度 |
|------|------|------|---------|
| 2D | x, y | θ | 3 |
| 3D | x, y, z | roll, pitch, yaw | 6 |

### 思考：Turtlesim的小乌龟有几个自由度？

```
┌─────────────────────────────────────────────────────────────┐
│  小乌龟的运动：                                              │
│                                                             │
│  • 可以在2D平面移动 (x, y) = 2个位置自由度               │
│  • 可以旋转方向 θ = 1个姿态自由度                          │
│                                                             │
│  总计：3个自由度 (在2D空间)                               │
│                                                             │
│  但是！它只有2个控制输入：                                  │
│  • 线速度 (控制x,y)                                        │
│  • 角速度 (控制θ)                                         │
│                                                             │
│  这就是为什么它不能直接侧向移动！                           │
└─────────────────────────────────────────────────────────────┘
```

### 思考题

> 🔥 **挑战**：尝试回答以下问题

1. **为什么逆运动学更难？**
   - 正运动学有唯一解
   - 逆运动学可能有多个解（机械臂的"肘向上"vs"肘向下"）

2. **关节越多越难？**
   - 2关节机械臂有解析解
   - 6关节（人体手臂）需要数值迭代求解

3. **实际应用：**
   - 工业机械臂如何抓取任意位置的物体？
   - 机器人如何保证末端不碰到障碍物？

---

### 📚 延伸学习

- **PyBullet IK** - PyBullet内置逆运动学求解器
- **KDL** - ROS的运动学库
- **MoveIt** - ROS机械臂规划框架

