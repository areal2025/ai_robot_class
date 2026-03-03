#!/usr/bin/env python3
"""
PyBullet机器狗仿真服务器
支持WebSocket控制和VNC显示
"""

import pybullet as p
import pybullet_data
import numpy as np
import json
import asyncio
import websockets
import os
import sys
from datetime import datetime

# 配置
HOST = "0.0.0.0"
PORT = 8765
TOKEN = "ai-robotics-course-2026"

class RobotSimulator:
    def __init__(self):
        # 使用GUI模式（无头）进行渲染
        self.physics_client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setTimeStep(1/240)
        
        # 加载环境
        p.loadURDF("plane.urdf")
        
        # 加载机器人 (使用laikago或创建简单模型)
        try:
            self.robot_id = p.loadURDF("laikago/laikago.urdf", [0, 0.5, 0], useFixedBase=False)
        except:
            # 如果没有laikago，创建一个简单机器人
            self.robot_id = self.create_simple_robot()
        
        # 控制状态
        self.control_state = {
            'forward': 0,
            'lateral': 0,
            'yaw': 0,
            'height': 0.3
        }
        
        print(f"PyBullet仿真已启动 (Client ID: {self.physics_client})")
    
    def create_simple_robot(self):
        """创建简单机器人模型"""
        # 身体
        body_id = p.loadURDF("cube.urdf", [0, 0.5, 0], globalScaling=0.3)
        return body_id
    
    def reset(self):
        """重置机器人"""
        p.resetBasePositionAndOrientation(self.robot_id, [0, 0.5, 0], [0, 0, 0, 1])
        p.resetBaseVelocity(self.robot_id, [0, 0, 0], [0, 0, 0])
    
    def apply_control(self, action):
        """应用控制"""
        self.control_state.update(action)
        
        # 获取当前位置
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # 计算移动
        forward = self.control_state.get('forward', 0)
        yaw = self.control_state.get('yaw', 0)
        
        # 速度控制
        speed = 2.0
        turn_speed = 1.5
        
        # 新位置
        new_pos = list(pos)
        new_pos[0] += forward * speed * 0.01
        new_pos[2] += forward * speed * 0.01
        
        # 高度控制
        target_height = self.control_state.get('height', 0.3)
        new_pos[1] = target_height
        
        # 应用
        p.resetBasePositionAndOrientation(self.robot_id, new_pos, orn)
        
        # 旋转
        euler = p.getEulerFromQuaternion(orn)
        new_yaw = euler[1] + yaw * turn_speed * 0.01
        new_orn = p.getQuaternionFromEuler([euler[0], new_yaw, euler[2]])
        p.resetBasePositionAndOrientation(self.robot_id, new_pos, new_orn)
    
    def get_state(self):
        """获取机器人状态"""
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        vel, ang_vel = p.getBaseVelocity(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        return {
            'position': [round(x, 3) for x in pos],
            'orientation': [round(x, 3) for x in euler],
            'velocity': [round(x, 3) for x in vel],
            'timestamp': datetime.now().isoformat()
        }
    
    def step(self):
        """仿真一步"""
        p.stepSimulation()
    
    def close(self):
        """关闭"""
        p.disconnect()

# 全局仿真器
sim = None

async def handle_client(websocket, path):
    global sim
    client_id = f"client_{id(websocket)}"
    authenticated = False
    
    print(f"[{client_id}] 新连接")
    
    try:
        await websocket.send(json.dumps({
            'type': 'welcome',
            'message': '欢迎使用PyBullet机器狗仿真',
            'token_required': True
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                
                # 认证
                if not authenticated:
                    if data.get('type') == 'auth':
                        if data.get('token') == TOKEN:
                            authenticated = True
                            await websocket.send(json.dumps({
                                'type': 'auth_success',
                                'message': '认证成功！'
                            }))
                            print(f"[{client_id}] 认证成功")
                        else:
                            await websocket.send(json.dumps({
                                'type': 'auth_failed',
                                'message': '令牌错误'
                            }))
                    continue
                
                # 处理控制
                if data.get('type') == 'action':
                    sim.apply_control(data.get('action', {}))
                    await websocket.send(json.dumps({
                        'type': 'state',
                        'data': sim.get_state()
                    }))
                
                elif data.get('type') == 'reset':
                    sim.reset()
                    await websocket.send(json.dumps({'type': 'reset_done'}))
                
                elif data.get('type') == 'state':
                    await websocket.send(json.dumps({
                        'type': 'state',
                        'data': sim.get_state()
                    }))
                
                # 仿真步骤
                sim.step()
                
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': '无效的JSON'
                }))
    
    except websockets.exceptions.ConnectionClosed:
        print(f"[{client_id}] 断开连接")
    finally:
        pass

async def main():
    global sim
    
    print("初始化PyBullet仿真...")
    sim = RobotSimulator()
    
    print(f"启动WebSocket服务器 ws://{HOST}:{PORT}")
    print(f"访问令牌: {TOKEN}")
    
    async with websockets.serve(handle_client, HOST, PORT):
        # 保持仿真运行
        while True:
            await asyncio.sleep(1/60)
            sim.step()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n关闭仿真...")
        sim.close()
