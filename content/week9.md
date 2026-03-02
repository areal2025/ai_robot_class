# 第9周：机器视觉与AI工具入门

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | OpenCV基础 | 图像读取、显示、颜色空间 |
| 第2次 | 3小时 | 经典视觉算法 | 边缘检测、轮廓提取、特征点 |

---

## 第一次课：OpenCV基础（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | 上周内容回顾 |
| 讲解 | 60分钟 | OpenCV简介与安装 |
| 讲解 | 60分钟 | 图像基本操作 |
| 茶歇 | 10分钟 | 休息 |
| 演示 | 30分钟 | 演示实验 |

---

## 3.1.1 OpenCV简介

> **OpenCV** = Open Source Computer Vision Library  
> 开源计算机视觉库，由Intel于1999年创建 [1]。

```
OpenCV 应用领域：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  • 人脸检测与识别      • 物体检测与分类                   │
│  • 图像分割          • 相机校准                         │
│  • 运动分析          • 机器学习                         │
│  • 3D重建           • 深度学习推理                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 安装OpenCV

```bash
# Python安装
pip install opencv-python

# 验证安装
python3 -c "import cv2; print(cv2.__version__)"
```

---

## 3.1.2 图像基本操作

### 读取与显示图像

```python
import cv2
import numpy as np

# 读取图像
img = cv2.imread('robot.jpg')

# 获取图像信息
print(f"形状: {img.shape}")  # (高, 宽, 通道)
print(f"尺寸: {img.size}")    # 总像素数
print(f"数据类型: {img.dtype}") # uint8

# 显示图像
cv2.imshow('Robot Image', img)
cv2.waitKey(0)  # 等待按键
cv2.destroyAllWindows()
```

### 颜色空间

```python
# BGR 转 RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR 转 灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR 转 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 在HSV中提取红色区域
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)
```

### 图像变换

```python
# 调整大小
resized = cv2.resize(img, (640, 480))

# 旋转
rows, cols = img.shape[:2]
M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
rotated = cv2.warpAffine(img, M, (cols, rows))

# 平移
M = np.float32([[1, 0, 100], [0, 1, 50]])
translated = cv2.warpAffine(img, M, (cols, rows))

# 裁剪
cropped = img[100:300, 200:400]
```

---

## 第二次课：经典视觉算法（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | OpenCV基础回顾 |
| 讲解 | 60分钟 | 边缘检测 |
| 讲解 | 60分钟 | 轮廓检测与特征 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.1.3 边缘检测

### Sobel算子

```python
import cv2
import numpy as np

# 读取灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sobel算子
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.sqrt(sobelx**2 + sobely**2)

# 显示
cv2.imshow('Sobel', sobel)
cv2.waitKey(0)
```

### Canny边缘检测

```python
# Canny边缘检测
edges = cv2.Canny(gray, 50, 150)

# 参数说明
# 50: 第一个阈值（低阈值）
# 150: 第二个阈值（高阈值）
# 低阈值和高阈值之间的边缘取决于与强边缘的连接

cv2.imshow('Canny Edges', edges)
cv2.waitKey(0)
```

### 边缘检测原理

```
边缘检测原理：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  原始图像                                                   │
│  ┌───┬───┬───┐                                            │
│  │ 0 │ 0 │ 0 │                                            │
│  ├───┼───┼───┤                                            │
│  │ 0 │255│ 0 │  ← 边缘 (梯度变化大)                       │
│  ├───┼───┼───┤                                            │
│  │ 0 │ 0 │ 0 │                                            │
│  └───┴───┴───┘                                            │
│                                                             │
│  梯度 = |∂I/∂x| + |∂I/∂y|                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3.1.4 轮廓检测

```python
# 边缘检测
edges = cv2.Canny(gray, 50, 150)

# 查找轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
result = img.copy()
cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

# 显示
cv2.imshow('Contours', result)
cv2.waitKey(0)

# 轮廓特征
for contour in contours:
    area = cv2.contourArea(contour)      # 面积
    perimeter = cv2.arcLength(contour, True)  # 周长
    x, y, w, h = cv2.boundingRect(contour)  # 边界框
```

---

## 3.1.5 特征点检测

### Harris角点检测

```python
# Harris角点检测
gray = np.float32(gray)
corners = cv2.cornerHarris(gray, 2, 3, 0.04)

# 放大角点
corners = cv2.dilate(corners, None)

# 标记角点
img[corners > 0.01 * corners.max()] = [0, 0, 255]

cv2.imshow('Harris Corners', img)
```

### ORB特征点（快速检测）

```python
# ORB (Oriented FAST and Rotated BRIEF)
orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(gray, None)

# 绘制特征点
img_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))

cv2.imshow('ORB Features', img_keypoints)
```

---

## 3.1.6 ROS2中的图像处理

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
    """图像处理节点"""
    
    def __init__(self):
        super().__init__('image_processor')
        
        # 创建订阅者
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # 创建发布者
        self.publisher = self.create_publisher(Image, '/image/processed', 10)
        
        # 创建CV Bridge
        self.bridge = CvBridge()
        
        self.get_logger().info('图像处理节点已启动')
    
    def image_callback(self, msg):
        """处理接收到的图像"""
        # ROS图像转OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # 转灰度图
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # OpenCV转ROS图像
        edge_msg = self.bridge.cv2_to_imgmsg(edges, 'mono8')
        
        # 发布
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

[1] Bradski, G. (2000). The OpenCV Library. *Dr. Dobb's Journal of Software Tools*.

[2] OpenCV Team. (2024). *OpenCV Documentation*. Available: https://docs.opencv.org/

[3] Szeliski, R. (2010). *Computer Vision: Algorithms and Applications*. Springer. ISBN: 978-1848829343

---

## 下周预告

> **第10周：物体检测与识别**
> - 经典方法：HOG + SVM
> - 深度学习：YOLO目标检测
> - 公开数据集：COCO、PASCAL VOC

---

*第9周结束！*
