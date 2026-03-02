# 第10周：物体检测与识别

**课时**: 6小时（第一次课3小时 + 第二次课3小时）

---

## 📋 本周课程表

| 次序 | 时间 | 主题 | 内容 |
|------|------|------|------|
| 第1次 | 3小时 | YOLO目标检测 | 预训练模型使用 |
| 第2次 | 3小时 | ROS2集成 | 检测结果发布 |

---

## 第一次课：YOLO目标检测（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | OpenCV回顾 |
| 讲解 | 60分钟 | YOLO简介 |
| 讲解 | 60分钟 | 预训练模型使用 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.2.1 YOLO简介

> **YOLO** = You Only Look Once  
> 只需看一次图像就能检测出所有物体！

```
YOLO检测示例：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ┌─────┐                                                   │
│    │ 人 │     ┌────┐                                         │
│    └─────┘     │ 狗 │   ┌──┐                                 │
│                 └────┘   │车│                                 │
│                                                             │
│  输出: 物体类别 + 位置 + 置信度                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### YOLO版本

| 版本 | 速度 | 准确率 | 推荐 |
|------|------|--------|------|
| YOLOv8n | 最快 | 较低 | 学习用 |
| YOLOv8s | 快 | 中等 | 平衡 |
| YOLOv8m | 中等 | 较高 | 进阶 |

---

## 3.2.2 安装YOLO

```bash
# 安装Ultralytics库
pip install ultralytics

# 验证安装
python3 -c "from ultralytics import YOLO; print('OK')"
```

---

## 3.2.3 YOLO快速使用

```python
from ultralytics import YOLO

# 加载预训练模型（自动下载）
model = YOLO('yolov8n.pt')

# 检测图像
results = model('street.jpg')

# 显示结果
for r in results:
    print(f"检测到 {len(r.boxes)} 个物体")
    for box in r.boxes:
        cls = model.names[int(box.cls[0])]
        conf = float(box.conf[0])
        print(f"  - {cls}: {conf:.2%}")
```

### 检测摄像头

```python
# 检测摄像头
results = model(0)  # 0 = 默认摄像头

# 检测视频文件
results = model('video.mp4', save=True)
```

---

## 第二次课：ROS2集成（3小时）

### ⏱️ 时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| 复习 | 20分钟 | YOLO使用回顾 |
| 讲解 | 60分钟 | ROS2话题发布 |
| 讲解 | 60分钟 | 可视化显示 |
| 茶歇 | 10分钟 | 休息 |
| 实践 | 60分钟 | 实验练习 |

---

## 3.2.4 ROS2目标检测节点

```python
#!/usr/bin/env python3
"""
YOLO目标检测ROS2节点
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2


class YOLODetector(Node):
    """YOLO目标检测节点"""
    
    def __init__(self):
        super().__init__('yolo_detector')
        
        # 加载YOLO模型
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info('YOLO模型已加载')
        
        # 订阅图像话题
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # 发布检测结果（简单版：发布检测到的类别）
        self.publisher = self.create_publisher(String, '/detected_objects', 10)
        
        self.bridge = CvBridge()
        self.get_logger().info('YOLO检测节点已启动')
    
    def image_callback(self, msg):
        """图像回调"""
        try:
            # ROS图像转OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            
            # YOLO检测
            results = self.model(cv_image, verbose=False)
            
            # 提取检测结果
            detected = []
            for r in results:
                for box in r.boxes:
                    if float(box.conf[0]) > 0.5:  # 置信度阈值
                        cls = self.model.names[int(box.cls[0])]
                        detected.append(cls)
            
            # 发布结果
            if detected:
                msg_out = String()
                msg_out.data = ', '.join(set(detected))
                self.publisher.publish(msg_out)
            
        except Exception as e:
            self.get_logger().error(f'检测失败: {e}')


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

### 启动命令

```bash
# 1. 启动摄像头
ros2 launch usb_cam usb_cam.launch.py

# 2. 启动YOLO检测
ros2 run your_package yolo_detector

# 3. 查看检测结果
ros2 topic echo /detected_objects
```

---

## 本周实验报告

### ✅ 验收清单

| 序号 | 实验 | 要求 | 完成 |
|------|------|------|------|
| 1 | 安装YOLO | 能import | ☐ |
| 2 | 检测图片 | 运行检测 | ☐ |
| 3 | 检测摄像头 | 实时检测 | ☐ |
| 4 | ROS2节点 | 发布话题 | ☐ |

---

## 参考文献

[1] Ultralytics. (2024). *YOLOv8 Documentation*. Available: https://docs.ultralytics.com/

[2] Redmon, J., et al. (2016). You Only Look Once. *CVPR*.

---

## 下周预告

> **第11周：目标追踪**
> - 简单追踪方法
> - ROS2集成

---

*第10周结束！*
