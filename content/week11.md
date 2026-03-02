# 第11周：目标追踪

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 简单追踪 | 颜色追踪 + 框追踪 |
| 第2次 | 3小时 | 多目标追踪 | Sort算法 + ROS2 |

---

## 第一次课：简单追踪方法（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 目标检测回顾 |
| 讲解 | 60分钟 | 颜色追踪 |
| 讲解 | 60分钟 | 框追踪（IOU） |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.3.1 颜色追踪

> 根据颜色定位物体，最简单的追踪方法！

### 原理

```
颜色追踪流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  摄像头图像                                                 │
│       ↓                                                     │
│  转HSV颜色空间                                             │
│       ↓                                                     │
│  颜色范围过滤 (inRange)                                    │
│       ↓                                                     │
│  找轮廓 (findContours)                                    │
│       ↓                                                     │
│  取最大轮廓的中心点                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 代码实现

```python
import cv2
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(0)

# 红色范围（HSV）
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 转HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 颜色过滤
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 追踪最大轮廓
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (x+w//2, y+h//2), 5, (0, 0, 255), -1)
    
    cv2.imshow('Color Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 3.3.2 IOU追踪

> 根据检测框的重叠面积追踪物体

### IOU计算

```python
def calculate_iou(box1, box2):
    """计算两个框的IOU"""
    # box = [x1, y1, x2, y2]
    
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    # 计算重叠面积
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    
    # 计算各自面积
    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])
    
    # 计算IOU
    union = area1 + area2 - intersection
    return intersection / union if union > 0 else 0
```

### 简单追踪器

```python
class SimpleTracker:
    """简单追踪器"""
    
    def __init__(self, iou_threshold=0.3):
        self.tracks = {}  # id -> box
        self.next_id = 0
        self.iou_threshold = iou_threshold
    
    def update(self, detections):
        """更新追踪"""
        # detections: [[x1,y1,x2,y2, conf], ...]
        
        # 如果没有检测
        if not detections:
            self.tracks.clear()
            return {}
        
        # 如果没有历史轨迹，创建新ID
        if not self.tracks:
            for det in detections:
                self.tracks[self.next_id] = det[:4]
                self.next_id += 1
            return self.tracks.copy()
        
        # 简单的匹配
        matched = {}
        used_det = set()
        
        for track_id, old_box in list(self.tracks.items()):
            best_iou = 0
            best_det_idx = -1
            
            for i, det in enumerate(detections):
                if i in used_det:
                    continue
                iou = calculate_iou(old_box, det[:4])
                if iou > best_iou:
                    best_iou = iou
                    best_det_idx = i
            
            if best_iou > self.iou_threshold:
                matched[track_id] = detections[best_det_idx][:4]
                used_det.add(best_det_idx)
        
        self.tracks = matched
        return matched


# 使用
tracker = SimpleTracker(iou_threshold=0.3)

# 每一帧调用
current_detections = [[100, 100, 200, 200, 0.9], ...]  # YOLO输出
tracks = tracker.update(current_detections)
```

---

## 第二次课：多目标追踪（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 简单追踪回顾 |
| 讲解 | 60分钟 | Sort算法 |
| 讲解 | 60分钟 | ROS2集成 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.3.3 Sort追踪器

> **Sort** = Simple Online and Realtime Tracking  
> 简单高效的多目标追踪器 [1]。

### 安装Sort

```bash
pip install sort
```

### 使用Sort

```python
import cv2
import numpy as np
from sort import Sort
from ultralytics import YOLO

# 加载YOLO
model = YOLO('yolov8n.pt')

# 创建追踪器
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # YOLO检测
    results = model(frame, verbose=False)
    
    # 提取检测框
    dets = []
    for r in results:
        for box in r.boxes:
            if float(box.conf[0]) > 0.5:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                dets.append([x1, y1, x2, y2, float(box.conf[0])])
    
    dets = np.array(dets) if dets else np.empty((0, 5))
    
    # 更新追踪
    tracks = tracker.update(dets)
    
    # 绘制结果
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        cv2.rectangle(frame, (int(x1), int(y1)), 
                     (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'ID:{int(track_id)}', 
                   (int(x1), int(y1)-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('Multi-Object Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 3.3.4 ROS2追踪节点

```python
#!/usr/bin/env python3
"""
目标追踪ROS2节点
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np
from sort import Sort


class ObjectTracker(Node):
    """目标追踪节点"""
    
    def __init__(self):
        super().__init__('object_tracker')
        
        # 加载YOLO
        self.model = YOLO('yolov8n.pt')
        
        # 创建追踪器
        self.tracker = Sort(max_age=30, min_hits=3)
        
        # 订阅图像
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.callback, 10)
        
        # 发布追踪结果
        self.publisher = self.create_publisher(
            Int32MultiArray, '/tracked_ids', 10)
        
        self.bridge = CvBridge()
        self.get_logger().info('追踪节点已启动')
    
    def callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # 检测
        results = self.model(cv_image, verbose=False)
        dets = []
        for r in results:
            for box in r.boxes:
                if float(box.conf[0]) > 0.5:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    dets.append([x1, y1, x2, y2, float(box.conf[0])])
        
        dets = np.array(dets) if dets else np.empty((0, 5))
        
        # 追踪
        tracks = self.tracker.update(dets)
        
        # 发布ID
        ids = [int(t[4]) for t in tracks]
        out_msg = Int32MultiArray()
        out_msg.data = ids
        self.publisher.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracker()
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
| 1 | 颜色追踪 | 追踪红色物体 | ☐ |
| 2 | IOU计算 | 实现IOU函数 | ☐ |
| 3 | Sort追踪 | 多目标追踪 | ☐ |
| 4 | ROS2集成 | 发布ID话题 | ☐ |

---

## 参考文献

[1] Bewley, A., et al. (2016). Simple Online and Realtime Tracking. *ICIP*.

---

## 下周预告

> **第12周：Sim2Real - 仿真到现实**
> - Gazebo仿真
> - 真机控制

---

*第11周结束！*
