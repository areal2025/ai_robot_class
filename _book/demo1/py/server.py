#!/usr/bin/env python3
"""
PyBullet 机器狗仿真后端
支持 WebSocket 实时控制
"""

import asyncio
import json
import websockets
import pybullet as p
import pybullet_data
import numpy as np
import argparse
import os
from datetime import datetime

# 配置
HOST = "0.0.0.0"
PORT = 8765
TOKEN = "ai-robotics-course-2026"

# 全局状态
robot_id = None
client_count = 0
connected_clients = set()

def setup_pybullet(gui=False):
    """初始化PyBullet仿真"""
    if gui:
        client = p.connect(p.GUI)
    else:
        client = p.connect(p.DIRECT)
    
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.setTimeStep(1/240)
    
    # 加载环境
    p.loadURDF("plane.urdf")
    
    # 加载宇树机器狗 (简化版)
    robot_pos = [0, 0.5, 0]
    robot_id = p.loadURDF("laikago/laikago.urdf", robot_pos, useFixedBase=False)
    
    # 设置初始姿态
    for joint_idx in range(p.getNumJoints(robot_id)):
        p.resetJointState(robot_id, joint_idx, 0)
    
    return robot_id

def reset_robot(robot_id):
    """重置机器人位置"""
    p.resetBasePositionAndOrientation(robot_id, [0, 0.5, 0], [0, 0, 0, 1])
    for joint_idx in range(p.getNumJoints(robot_id)):
        p.resetJointState(robot_id, joint_idx, 0)

def apply_action(robot_id, action):
    """
    应用控制指令
    action: dict with keys: forward, lateral, yaw, height, roll, pitch
    """
    # 简化的控制逻辑
    # 实际宇树机器人需要复杂的步态算法
    base_vel = action.get('forward', 0) * 2.0
    turn_vel = action.get('yaw', 0) * 1.5
    
    # 获取当前位置
    pos, orn = p.getBasePositionAndOrientation(robot_id)
    
    # 计算新位置
    new_pos = [
        pos[0] + base_vel * 0.01,
        max(0.35, pos[1] + action.get('height', 0) * 0.01),
        pos[2]
    ]
    
    # 应用移动
    p.resetBasePositionAndOrientation(robot_id, new_pos, orn)
    
    return {
        'position': new_pos,
        'velocity': [base_vel, 0, turn_vel],
        'timestamp': datetime.now().isoformat()
    }

def get_robot_state(robot_id):
    """获取机器人状态"""
    pos, orn = p.getBasePositionAndOrientation(robot_id)
    vel, ang_vel = p.getBaseVelocity(robot_id)
    
    # 转换为欧拉角
    euler = p.getEulerFromQuaternion(orn)
    
    return {
        'position': list(pos),
        'orientation': list(euler),
        'velocity': list(vel),
        'angular_velocity': list(ang_vel),
        'timestamp': datetime.now().isoformat()
    }

async def handle_client(websocket, path):
    """处理WebSocket客户端连接"""
    global client_count
    
    client_id = f"client_{client_count}"
    client_count += 1
    connected_clients.add(websocket)
    
    print(f"[{client_id}] Connected from {websocket.remote_address}")
    
    try:
        # 发送欢迎消息
        await websocket.send(json.dumps({
            'type': 'welcome',
            'client_id': client_id,
            'token_required': True,
            'message': '请提供访问令牌'
        }))
        
        authenticated = False
        local_robot_id = None
        
        async for message in websocket:
            try:
                data = json.loads(message)
                
                # 验证令牌
                if not authenticated:
                    if data.get('type') == 'auth':
                        token = data.get('token', '')
                        if token == TOKEN:
                            authenticated = True
                            local_robot_id = setup_pybullet(gui=False)
                            await websocket.send(json.dumps({
                                'type': 'auth_success',
                                'message': '认证成功！正在初始化仿真...'
                            }))
                            print(f"[{client_id}] Authenticated successfully")
                        else:
                            await websocket.send(json.dumps({
                                'type': 'auth_failed',
                                'message': '令牌错误，请重试'
                            }))
                    continue
                
                # 处理控制指令
                if data.get('type') == 'action':
                    action = data.get('action', {})
                    state = apply_action(local_robot_id, action)
                    await websocket.send(json.dumps({
                        'type': 'state',
                        'data': state
                    }))
                    
                elif data.get('type') == 'reset':
                    reset_robot(local_robot_id)
                    await websocket.send(json.dumps({
                        'type': 'reset_done'
                    }))
                    
                elif data.get('type') == 'state':
                    state = get_robot_state(local_robot_id)
                    await websocket.send(json.dumps({
                        'type': 'state',
                        'data': state
                    }))
                    
                # 仿真步骤
                p.stepSimulation()
                
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': '无效的JSON消息'
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[{client_id}] Disconnected")
    finally:
        connected_clients.discard(websocket)
        if local_robot_id:
            p.removeBody(local_robot_id)

async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='PyBullet机器狗仿真服务器')
    parser.add_argument('--port', type=int, default=PORT, help='WebSocket端口')
    parser.add_argument('--token', type=str, default=TOKEN, help='访问令牌')
    args = parser.parse_args()
    
    global TOKEN
    TOKEN = args.token
    
    # 初始化PyBullet
    print("初始化PyBullet仿真环境...")
    setup_pybullet(gui=False)
    print("仿真环境就绪！")
    
    # 启动WebSocket服务器
    async with websockets.serve(handle_client, HOST, args.port):
        print(f"🚀 服务器运行在 ws://{HOST}:{args.port}")
        print(f"🔑 访问令牌: {TOKEN}")
        print("按 Ctrl+C 停止")
        
        # 保持运行
        while True:
            await asyncio.sleep(1)
            p.stepSimulation()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")
