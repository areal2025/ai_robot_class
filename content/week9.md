# 第9周：机器视觉与AI工具入门

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | OpenCV基础 | 图像读取、显示、颜色 |
| 第2次 | 3小时 | 图像处理 | 边缘检测、轮廓、特征 |

---

## 第一次课：OpenCV基础（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 上周内容回顾 |
| 讲解 | 60分钟 | OpenCV安装与介绍 |
| 讲解 | 60分钟 | 图像基本操作 |
| 茶歇 | 10分钟 | 休息 |
| 演示 | 30分钟 | 演示实验 |

---

## 3.1.1 OpenCV简介

> **OpenCV** = Open Source Computer Vision Library  
> 开源计算机视觉库，用于处理图像和视频 [1]。

```
OpenCV 能做什么：

┌─────────────────────────────────────────────────────────────┐
│  • 人脸检测/识别      • 物体检测/分类                       │
│  • 图像分割          • 边缘检测                             │
│  • 颜色追踪          • 姿态估计                             │
│  • 3D重建           • 深度学习推理                         │
└─────────────────────────────────────────────────────────────┘
```

### 安装

```bash
pip install opencv-python

# 验证
python3 -c "import cv2; print(cv2.__version__)"
```

---

## 3.1.2 图像基本操作

```python
import cv2
import numpy as np

# 读取图像
img = cv2.imread('robot.jpg')

# 查看信息
print(f"形状: {img.shape}")  # (高, 宽, 通道)
print(f"尺寸: {img.size}")

# 显示图像
cv2.imshow('Image', img)
cv2.waitKey(0)  # 等待按键
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('output.jpg', img)
```

### 颜色空间转换

```python
# BGR 转 RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR 转 灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR 转 HSV（用于颜色追踪）
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

### 图像变换

```python
# 调整大小
resized = cv2.resize(img, (640, 480))

# 旋转90度
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# 裁剪
cropped = img[100:300, 200:400]
```

---

## 第二次课：图像处理（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | OpenCV基础回顾 |
| 讲解 | 60分钟 | 边缘检测 |
| 讲解 | 60分钟 | 轮廓与特征 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.1.3 边缘检测

### Canny边缘检测（最简单）

```python
import cv2

# 读取灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny边缘检测
edges = cv2.Canny(gray, 50, 150)

# 参数说明
# 50: 低阈值
# 150: 高阈值

cv2.imshow('Edges', edges)
cv2.waitKey(0)
```

### 原理简介

```
边缘 = 像素变化大的地方

原图:        边缘检测后:
┌─────┐      ┌─────┐
│░░░▓▓│      │    █│
│░░░▓▓│  →   │    █│
│░░░▓▓│      │    █│
└─────┘      └─────┘
```

---

## 3.1.4 轮廓检测

```python
# 边缘检测
edges = cv2.Canny(gray, 50, 150)

# 找轮廓
contours, hierarchy = cv2.findContours(
    edges, 
    cv2.RETR_EXTERNAL,  # 只找外轮廓
    cv2.CHAIN_APPROX_SIMPLE
)

# 绘制轮廓
result = img.copy()
cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

cv2.imshow('Contours', result)
cv2.waitKey(0)

# 轮廓特征
for contour in contours:
    area = cv2.contourArea(contour)      # 面积
    perimeter = cv2.arcLength(contour, True)  # 周长
```

---

## 3.1.5 特征点检测

### 简单角点检测

```python
# Harris角点检测（简单版）
gray = np.float32(gray)
corners = cv2.cornerHarris(gray, 2, 3, 0.04)

# 标记角点
img[corners > 0.01 * corners.max()] = [0, 0, 255]
cv2.imshow('Corners', img)
```

### ORB特征点（推荐）

```python
# ORB - 快速特征点检测
orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(gray, None)

# 绘制特征点
img_keypoints = cv2.drawKeypoints(img, keypoints, None, 
                                   color=(0, 255, 0))

cv2.imshow('ORB', img_keypoints)
```

---

## 3.1.6 ROS2图像处理

```python
#!/usr/bin/env python3
"""
ROS2图像处理节点
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        
        # 订阅图像
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.callback, 10)
        
        # 发布处理后的图像
        self.publisher = self.create_publisher(Image, '/image/edges', 10)
        
        self.bridge = CvBridge()
        self.get_logger().info('图像处理节点已启动')
    
    def callback(self, msg):
        # 转OpenCV格式
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # 转灰度
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # 转ROS格式发布
        edge_msg = self.bridge.cv2_to_imgmsg(edges, 'mono8')
        self.publisher.publish(edge_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImageProcessor()
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
| 1 | 安装OpenCV | 能正常import | ☐ |
| 2 | 读取显示图像 | 能显示图片 | ☐ |
| 3 | 颜色空间转换 | BGR转HSV | ☐ |
| 4 | 边缘检测 | Canny算子 | ☐ |
| 5 | 轮廓检测 | 绘制轮廓 | ☐ |
| 6 | ROS2图像处理 | 话题收发 | ☐ |

---

## 参考文献

[1] Bradski, G. (2000). The OpenCV Library. *Dr. Dobb's Journal*.

[2] OpenCV Team. (2024). *OpenCV Documentation*. Available: https://docs.opencv.org/

---

## 下周预告

> **第10周：物体检测与识别**
> - YOLO目标检测
> - ROS2集成

---

*第9周结束！*
