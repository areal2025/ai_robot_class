# 第10周：物体检测与识别

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | 经典方法 | HOG + SVM 物体分类 |
| 第2次 | 3小时 | 深度学习方法 | YOLO实时检测 |

---

## 第一次课：经典方法（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | OpenCV基础回顾 |
| 讲解 | 60分钟 | HOG特征提取 |
| 讲解 | 60分钟 | SVM分类器 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.2.1 HOG特征提取

> **HOG** = Histogram of Oriented Gradients  
> 方向梯度直方图特征 [1]。

### HOG原理

```
HOG特征提取流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. 图像预处理                                             │
│     读取图像 → 灰度化 → 归一化                           │
│                                                             │
│  2. 计算梯度                                               │
│     使用[-1, 0, 1]卷积核                                  │
│     Gx = ∂I/∂x, Gy = ∂I/∂y                              │
│                                                             │
│  3. 单元格梯度直方图                                       │
│     将图像分成8×8像素的小格子                             │
│     每个格子计算9个方向的梯度直方图                        │
│                                                             │
│  4. 块归一化                                             │
│     2×2个格子组成一个块                                 │
│     对块内梯度进行L2归一化                                │
│                                                             │
│  5. 特征向量                                             │
│     所有块的HOG特征串联成最终特征向量                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### HOG Python实现

```python
import cv2
import numpy as np
from skimage.feature import hog


def extract_hog(image):
    """提取HOG特征"""
    
    # 图像预处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 128))
    
    # 提取HOG特征
    features = hog(
        resized,
        orientations=9,           # 方向数
        pixels_per_cell=(8, 8),   # 单元格大小
        cells_per_block=(2, 2),   # 块内单元格数
        block_norm='L2-Hys',
        visualize=False,
        feature_vector=True
    )
    
    return features


# 使用示例
img = cv2.imread('sample.jpg')
hog_features = extract_hog(img)
print(f"HOG特征维度: {hog_features.shape}")
```

### 特征可视化

```python
# 可视化HOG特征
features, hog_image = hog(
    resized,
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    visualize=True,
    feature_vector=True
)

cv2.imshow('HOG Features', hog_image)
cv2.waitKey(0)
```

---

## 3.2.2 SVM分类器

> **SVM** = Support Vector Machine  
> 支持向量机分类器 [2]。

### SVM原理

```
SVM分类原理：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  二分类问题：                                               │
│                                                             │
│        ● ● ● ● ●                                         │
│      ────────────── ○ ○ ○ ○ ○                           │
│        ● ● ●                                            │
│                                                             │
│      支持向量                                              │
│                                                             │
│  目标：找到一个超平面，最大化两类之间的间隔                │
│                                                             │
│  优化目标：                                               │
│  minimize: ||w||²                                         │
│  subject to: y_i(w·x_i + b) ≥ 1                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 使用SVM进行物体分类

```python
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np


def train_object_classifier(pos_images, neg_images):
    """训练物体分类器"""
    
    # 提取HOG特征
    pos_features = [extract_hog(img) for img in pos_images]
    neg_features = [extract_hog(img) for img in neg_images]
    
    # 准备数据
    X = np.array(pos_features + neg_features)
    y = np.array([1] * len(pos_features) + [0] * len(neg_features))
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 训练SVM
    svm = LinearSVC(C=1.0, max_iter=10000)
    svm.fit(X_train_scaled, y_train)
    
    # 评估
    accuracy = svm.score(X_test_scaled, y_test)
    print(f"准确率: {accuracy:.2%}")
    
    return svm, scaler


# 使用预训练模型进行预测
def predict_image(svm, scaler, image):
    """预测图像类别"""
    features = extract_hog(image).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = svm.predict(features_scaled)
    return prediction[0]
```

---

## 第二次课：深度学习方法（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | HOG+SVM回顾 |
| 讲解 | 60分钟 | YOLO目标检测 |
| 讲解 | 60分钟 | ROS2集成 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.2.3 YOLO目标检测

> **YOLO** = You Only Look Once  
> 实时目标检测算法 [3]。

### YOLO发展历程

```
YOLO版本对比：

┌─────────────────────────────────────────────────────────────┐
│  版本     发布时间   mAP@50    FPS    特点                │
├─────────────────────────────────────────────────────────────┤
│  YOLOv1  2015     63.4%    45     首个单阶段检测器        │
│  YOLOv2  2017     78.5%    40     引入Anchor Box        │
│  YOLOv3  2018     85.5%    35     多尺度预测            │
│  YOLOv4  2020     89.8%    65     Bag of Freebies    │
│  YOLOv5  2020     89.6%   140     PyTorch实现         │
│  YOLOv8  2023     94.0%   120     最新版本             │
│  YOLOv10 2024     95.5%   200+    实时SOTA             │
└─────────────────────────────────────────────────────────────┘
```

### YOLO原理

```
YOLO检测流程：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  输入图像 (416×416)                                        │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         CNN特征提取                   │   │
│  │    (Darknet / CSP / PANet)         │   │
│  └─────────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    特征图 (13×13, 26×26, 52×52)   │   │
│  │    每个格子预测:                          │   │
│  │    - 边界框 (x,y,w,h)                 │   │
│  │    - 物体概率                          │   │
│  │    - 类别概率                        │   │
│  └─────────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         NMS非极大值抑制                           │   │
│  └─────────────────────────────────────────────────────┘   │
│          ↓                                                  │
│  输出: 检测框 + 类别 + 置信度                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### YOLO Python实现

```python
# 使用Ultralytics YOLOv8
from ultralytics import YOLO
import cv2


# 加载模型
model = YOLO('yolov8n.pt')  # nano版本（最快）

# 检测图像
results = model('sample.jpg', save=True)

# 处理结果
for result in results:
    boxes = result.boxes  # 检测框
    for box in boxes:
        # 获取坐标
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        # 获取类别和置信度
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls]
        
        # 绘制框
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'{label} {conf:.2f}', 
                   (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (0, 255, 0), 2)

cv2.imshow('YOLO Detection', img)
cv2.waitKey(0)
```

### ROS2集成

```python
#!/usr/bin/env python3
"""
YOLO目标检测ROS2节点
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2


class YOLODetector(Node):
    """YOLO目标检测节点"""
    
    def __init__(self):
        super().__init__('yolo_detector')
        
        # 加载YOLO模型
        self.model = YOLO('yolov8n.pt')
        
        # 订阅图像话题
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        self.bridge = CvBridge()
        
        self.get_logger().info('YOLO检测节点已启动')
    
    def image_callback(self, msg):
        """图像回调"""
        # ROS图像转OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # YOLO检测
        results = self.model(cv_image, verbose=False)
        
        # 处理结果
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls]
                self.get_logger().info(f'检测到: {label} {conf:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = YOLODetector()
    
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

## 3.2.4 公开数据集

### 常用目标检测数据集

| 数据集 | 类别数 | 图像数 | 特点 |
|--------|-------|--------|-------|
| COCO [4] | 80 | 330K | 日常场景，最流行 |
| PASCAL VOC | 20 | 11K | 经典基准 |
| Open Images | 600 | 9M | 最多类别 |
| KITTI | 8 | 15K | 自动驾驶 |

### 下载COCO数据集

```bash
# 使用pycocotools
pip install pycocotools

# 或下载预训练模型
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # 自动下载
```

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | HOG特征提取 | 提取特征并可视化 | ☐ |
| 2 | SVM训练 | 训练简单分类器 | ☐ |
| 3 | YOLO安装 | 能运行检测 | ☐ |
| 4 | YOLO检测 | 检测图像中物体 | ☐ |
| 5 | ROS2集成 | 发布检测结果 | ☐ |

---

## 参考文献

[1] Dalal, N., & Triggs, B. (2005). Histograms of Oriented Gradients for Human Detection. *CVPR*.

[2] Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. *Machine Learning*, 20(3), 273-297.

[3] Redmon, J., et al. (2016). You Only Look Once: Unified, Real-Time Object Detection. *CVPR*.

[4] Lin, T.Y., et al. (2014). Microsoft COCO: Common Objects in Context. *ECCV*.

---

## 下周预告

> **第11周：视觉追踪与光流法**
> - 经典方法：光流法
> - 深度学习：DeepSORT追踪
> - ROS2集成

---

*第10周结束！*
