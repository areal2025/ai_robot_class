# 第11周：视觉追踪与光流法

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 经典光流法 | Lucas-Kanade算法 |
| 第2次 | 3小时 | 目标追踪 | 卡尔曼滤波 + DeepSORT |

---

## 第一次课：经典光流法（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 目标检测回顾 |
| 讲解 | 60分钟 | 光流法原理 |
| 讲解 | 60分钟 | Lucas-Kanade实现 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.3.1 光流法简介

> **光流** = 物体表面像素的表观运动模式 [1]。

```
光流定义：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  连续帧中像素的位移场：                                   │
│                                                             │
│  Frame t         Frame t+1                                 │
│  ┌───┬───┐    ┌───┬───┐                                  │
│  │ A │ B │ →  │ A'│ B'│  A移动到A'                        │
│  │ C │ D │    │ C'│ D'│  C移动到C'                        │
│  └───┴───┘    └───┴───┘                                  │
│                                                             │
│  光流向量： A→A' = (dx, dy)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 光流的应用

| 应用 | 说明 |
|------|------|
| 运动估计 | 估计相机/物体运动 |
| 目标追踪 | 追踪移动物体 |
| 动作识别 | 识别行为模式 |
| 视频 stabilization | 稳定视频 |

---

## 3.3.2 Lucas-Kanade算法

> Lucas-Kanade算法是最常用的稀疏光流算法 [2]。

### LK算法原理

```
Lucas-Kanade 基本假设：

1. 亮度恒定：I(x,y,t) = I(x+dx, y+dy, t+dt)
2. 小运动：相邻帧间位移很小
3. 空间一致性：相邻像素有相似运动

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  优化目标：                                                 │
│                                                             │
│  最小化: Σ[I_x(u,v)·dx + I_y(u,v)·dy + I_t]²             │
│                                                             │
│  其中：                                                    │
│  I_x = ∂I/∂x  (x方向梯度)                              │
│  I_y = ∂I/∂y  (y方向梯度)                              │
│  I_t = ∂I/∂t  (时间梯度)                               │
│                                                             │
│  求解：                                                   │
│  [dx, dy] = (A^T A)^(-1) A^T b                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### LK Python实现

```python
import cv2
import numpy as np


def lucas_kanade(prev_gray, curr_gray, prev_points):
    """Lucas-Kanade光流"""
    
    # Lucas-Kanade参数
    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )
    
    # 计算光流
    curr_points, status, error = cv2.calcOpticalFlowPyrLK(
        prev_gray, 
        curr_gray, 
        prev_points,
        None,
        **lk_params
    )
    
    return curr_points, status


# 使用示例
cap = cv2.VideoCapture('video.mp4')

# 读取第一帧
ret, frame1 = cap.read()
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# 选择要追踪的角点
prev_points = cv2.goodFeaturesToTrack(
    prev_gray, 
    maxCorners=100,
    qualityLevel=0.3,
    minDistance=7
)

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    
    curr_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # 计算光流
    curr_points, status, error = lucas_kanade(
        prev_gray, 
        curr_gray, 
        prev_points
    )
    
    # 绘制追踪结果
    for i, (prev, curr) in enumerate(zip(prev_points, curr_points)):
        a, b = curr.ravel()
        c, d = prev.ravel()
        frame2 = cv2.circle(frame2, (a, b), 5, (0, 255, 0), -1)
    
    cv2.imshow('Optical Flow', frame2)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
    prev_gray = curr_gray.copy()
    prev_points = curr_points.reshape(-1, 1, 2)

cap.release()
cv2.destroyAllWindows()
```

---

## 第二次课：目标追踪（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 光流法回顾 |
| 讲解 | 60分钟 | 卡尔曼滤波 |
| 讲解 | 60分钟 | DeepSORT追踪 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.3.3 卡尔曼滤波

> **卡尔曼滤波** = 预测 + 观测的最优状态估计 [3]。

### 卡尔曼滤波原理

```
卡尔曼滤波流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  预测步骤 (Prediction)                                     │
│  ─────────────────────                                    │
│  x̂ₖ₊₁ = F·x̂ₖ + B·uₖ           (状态预测)               │
│  Pₖ₊₁ = F·Pₖ·Fᵀ + Q            (协方差预测)            │
│                                                             │
│  更新步骤 (Update)                                        │
│  ─────────────────────                                    │
│  Kₖ = Pₖ·Hᵀ(H·Pₖ·Hᵀ + R)⁻¹    (卡尔曼增益)           │
│  x̂ₖ = x̂ₖ + Kₖ(zₖ - H·x̂ₖ)   (状态更新)               │
│  Pₖ = (I - Kₖ·H)·Pₖ          (协方差更新)             │
│                                                             │
│  其中：                                                    │
│  x̂ = 状态估计        P = 协方差矩阵                       │
│  F = 状态转移矩阵   H = 观测矩阵                         │
│  Q = 过程噪声      R = 观测噪声                         │
│  K = 卡尔曼增益                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 简单卡尔曼滤波实现

```python
import numpy as np


class SimpleKalmanFilter:
    """简单卡尔曼滤波"""
    
    def __init__(self, dt=0.1, process_noise=0.01, measurement_noise=0.1):
        # 状态 [位置, 速度]
        self.x = np.array([0.0, 0.0])
        
        # 状态转移矩阵
        self.F = np.array([
            [1, dt],    # 位置 = 旧位置 + 速度*dt
            [0, 1]      # 速度 = 旧速度
        ])
        
        # 观测矩阵 (只观测位置)
        self.H = np.array([[1, 0]])
        
        # 协方差矩阵
        self.P = np.eye(2)
        
        # 噪声
        self.Q = np.eye(2) * process_noise
        self.R = np.eye(1) * measurement_noise
    
    def predict(self):
        """预测步骤"""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x
    
    def update(self, z):
        """更新步骤"""
        # 预测观测
        z_pred = self.H @ self.x
        
        # 卡尔曼增益
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # 更新状态
        y = z - z_pred  # 观测残差
        self.x = self.x + K @ y
        
        # 更新协方差
        self.P = (np.eye(2) - K @ self.H) @ self.P
        
        return self.x


# 使用示例
kf = SimpleKalmanFilter(dt=0.1)

# 模拟测量
measurements = [1.2, 2.1, 3.3, 4.0, 5.1, 5.8]

for z in measurements:
    kf.predict()
    kf.update(np.array([z]))
    print(f"真实位置: {z:.1f}, 估计: {kf.x[0]:.2f}")
```

---

## 3.3.4 DeepSORT追踪

> **DeepSORT** = Simple Online and Realtime Tracking with a Deep Association Metric  
> 结合深度学习外观特征的追踪算法 [4]。

### DeepSORT原理

```
DeepSORT追踪流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  输入: 检测框 + 特征向量                                    │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  1. 预测: 卡尔曼滤波预测下一帧位置              │   │
│  └─────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  2. 关联: 匹配检测框与追踪轨迹                   │   │
│  │     - 距离度量 (IoU)                              │   │
│  │     - 外观度量 (余弦距离)                         │   │
│  └─────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  3. 更新: 卡尔曼滤波更新 + 特征更新            │   │
│  └─────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  输出: 追踪ID + 边界框                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 使用DeepSORT

```bash
# 安装
pip install sort
```

```python
import cv2
import numpy as np
from sort import Sort


# 创建追踪器
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# 加载YOLO
from ultralytics import YOLO
model = YOLO('yolov8n.pt')

# 打开视频
cap = cv2.VideoCapture('video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # YOLO检测
    results = model(frame, verbose=False)
    dets = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0])
            if conf > 0.5:
                dets.append([x1, y1, x2, y2, conf])
    
    # 转换为numpy数组
    dets = np.array(dets) if dets else np.empty((0, 5))
    
    # 更新追踪器
    tracks = tracker.update(dets)
    
    # 绘制结果
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        cv2.rectangle(frame, (int(x1), int(y1)), 
                        (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'ID:{int(track_id)}', 
                    (int(x1), int(y1)-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('DeepSORT', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 3.3.5 ROS2集成

```python
#!/usr/bin/env python3
"""
视觉追踪ROS2节点
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np
from sort import Sort


class VisualTracker(Node):
    """视觉追踪节点"""
    
    def __init__(self):
        super().__init__('visual_tracker')
        
        # 加载YOLO
        self.model = YOLO('yolov8n.pt')
        
        # 创建追踪器
        self.tracker = Sort(max_age=30, min_hits=3)
        
        # 订阅图像
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # 发布追踪结果
        self.publisher = self.create_publisher(Point, '/tracker/positions', 10)
        
        self.bridge = CvBridge()
        
        self.get_logger().info('视觉追踪节点已启动')
    
    def image_callback(self, msg):
        """图像回调"""
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # YOLO检测
        results = self.model(cv_image, verbose=False)
        
        # 提取检测框
        dets = []
        for r in results:
            for box in r.boxes:
                if float(box.conf[0]) > 0.5:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    dets.append([x1, y1, x2, y2, float(box.conf[0])])
        
        dets = np.array(dets) if dets else np.empty((0, 5))
        
        # 更新追踪
        tracks = self.tracker.update(dets)
        
        # 发布第一个追踪目标的位置
        if len(tracks) > 0:
            x1, y1, x2, y2, track_id = tracks[0]
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            point = Point()
            point.x = float(center_x)
            point.y = float(center_y)
            point.z = float(track_id)
            self.publisher.publish(point)


def main(args=None):
    rclpy.init(args=args)
    node = VisualTracker()
    
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
| 1 | 光流法 | Lucas-Kanade实现 | ☐ |
| 2 | 卡尔曼滤波 | 简单追踪 | ☐ |
| 3 | DeepSORT | 多目标追踪 | ☐ |
| 4 | ROS2集成 | 发布位置话题 | ☐ |

---

## 参考文献

[1] Gibson, J.J. (1950). *The Perception of the Visual World*. Houghton Mifflin.

[2] Lucas, B.D., & Kanade, T. (1981). An Iterative Image Registration Technique. *IJCAI*.

[3] Kalman, R.E. (1960). A New Approach to Linear Filtering. *Transactions of the ASME*.

[4] Wojke, N., Bewley, A., & Paulus, D. (2017). Simple Online and Realtime Tracking with a Deep Association Metric. *ICIP*.

---

## 下周预告

> **第12周：Sim2Real - 仿真到现实**
> - 仿真环境配置
> - 真机连接
> - 项目展示

---

*第11周结束！*
