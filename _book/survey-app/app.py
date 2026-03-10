#!/usr/bin/env python3
"""
AI机器人课程 - 学生问卷调查系统
基于Flask + SQLite
"""

from flask import Flask, render_template_string, request, redirect, url_for, g
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = '/root/.openclaw/workspace/ros2-course/survey-app/students.db'

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学生问卷 - AI机器人课程</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
            min-height: 100vh; 
            color: #fff;
            padding: 20px;
        }
        .container { 
            max-width: 700px; 
            margin: 0 auto; 
            background: #1e1e30;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 { 
            text-align: center; 
            color: #00d4ff;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .question {
            margin-bottom: 25px;
            padding: 20px;
            background: #252540;
            border-radius: 12px;
        }
        .question-num {
            color: #00d4ff;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .question-text {
            font-size: 16px;
            margin-bottom: 15px;
        }
        .options {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .option {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            background: #1a1a2e;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
        }
        .option:hover {
            background: #2a2a4e;
        }
        .option.selected {
            border-color: #00d4ff;
            background: rgba(0, 212, 255, 0.1);
        }
        .option input {
            margin-right: 12px;
            accent-color: #00d4ff;
            width: 18px;
            height: 18px;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            padding: 15px;
            background: #1a1a2e;
            border: 2px solid #333;
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: #00d4ff;
        }
        .submit-btn {
            display: block;
            width: 100%;
            padding: 18px;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 30px;
            transition: transform 0.2s;
        }
        .submit-btn:hover {
            transform: scale(1.02);
        }
        .thanks {
            text-align: center;
            padding: 40px;
        }
        .thanks h2 {
            color: #00ff88;
            margin-bottom: 15px;
        }
        .required {
            color: #ff6b6b;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 学生问卷调查</h1>
        <p class="subtitle">AI机器人课程 - 帮助老师了解大家的学习背景</p>
        
        <form id="surveyForm">
            <!-- Q1: Name -->
            <div class="question">
                <div class="question-num">问题 1/10 <span class="required">*必填</span></div>
                <div class="question-text">你的姓名？</div>
                <input type="text" name="name" required style="width:100%;padding:12px;background:#1a1a2e;border:2px solid #333;border-radius:8px;color:#fff;font-size:14px;">
            </div>
            
            <!-- Q2: Student ID -->
            <div class="question">
                <div class="question-num">问题 2/10 <span class="required">*必填</span></div>
                <div class="question-text">你的学号？</div>
                <input type="text" name="student_id" required style="width:100%;padding:12px;background:#1a1a2e;border:2px solid #333;border-radius:8px;color:#fff;font-size:14px;">
            </div>
            
            <!-- Q3: Major -->
            <div class="question">
                <div class="question-num">问题 3/10</div>
                <div class="question-text">你的专业是？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="major" value="cs"> 计算机科学/软件工程</label>
                    <label class="option"><input type="radio" name="major" value="ee"> 电子/电气工程</label>
                    <label class="option"><input type="radio" name="major" value="me"> 机械工程</label>
                    <label class="option"><input type="radio" name="major" value="ai"> 人工智能</label>
                    <label class="option"><input type="radio" name="major" value="other"> 其他专业</label>
                </div>
            </div>
            
            <!-- Q4: Programming Experience -->
            <div class="question">
                <div class="question-num">问题 4/10</div>
                <div class="question-text">你之前接触过编程吗？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="programming" value="0"> 完全没有</label>
                    <label class="option"><input type="radio" name="programming" value="1"> 简单了解过</label>
                    <label class="option"><input type="radio" name="programming" value="2"> 学过一些基础</label>
                    <label class="option"><input type="radio" name="programming" value="3"> 有项目经验</label>
                </div>
            </div>
            
            <!-- Q5: Python Level -->
            <div class="question">
                <div class="question-num">问题 5/10</div>
                <div class="question-text">你使用过Python吗？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="python" value="0"> 没用过</label>
                    <label class="option"><input type="radio" name="python" value="1"> 听说过</label>
                    <label class="option"><input type="radio" name="python" value="2"> 写过简单代码</label>
                    <label class="option"><input type="radio" name="python" value="3"> 比较熟练</label>
                </div>
            </div>
            
            <!-- Q6: ROS Experience -->
            <div class="question">
                <div class="question-num">问题 6/10</div>
                <div class="question-text">你了解ROS/ROS2吗？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="ros" value="0"> 完全不了解</label>
                    <label class="option"><input type="radio" name="ros" value="1"> 听说过</label>
                    <label class="option"><input type="radio" name="ros" value="2"> 简单用过</label>
                    <label class="option"><input type="radio" name="ros" value="3"> 有项目经验</label>
                </div>
            </div>
            
            <!-- Q7: Robot Experience -->
            <div class="question">
                <div class="question-num">问题 7/10</div>
                <div class="question-text">你接触过机器人吗？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="robot" value="0"> 完全没有</label>
                    <label class="option"><input type="radio" name="robot" value="1"> 在视频/书中见过</label>
                    <label class="option"><input type="radio" name="robot" value="2"> 玩过消费级机器人</label>
                    <label class="option"><input type="radio" name="robot" value="3"> 参加过机器人比赛/项目</label>
                </div>
            </div>
            
            <!-- Q8: AI Experience -->
            <div class="question">
                <div class="question-num">问题 8/10</div>
                <div class="question-text">你了解人工智能/机器学习吗？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="ai" value="0"> 完全不了解</label>
                    <label class="option"><input type="radio" name="ai" value="1"> 听说过概念</label>
                    <label class="option"><input type="radio" name="ai" value="2"> 看过教程/课程</label>
                    <label class="option"><input type="radio" name="ai" value="3"> 有实际项目经验</label>
                </div>
            </div>
            
            <!-- Q9: Interest -->
            <div class="question">
                <div class="question-num">问题 9/10</div>
                <div class="question-text">你对机器人的哪个方向最感兴趣？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="interest" value="vision"> 视觉识别/感知</label>
                    <label class="option"><input type="radio" name="interest" value="motion"> 运动控制/导航</label>
                    <label class="option"><input type="radio" name="interest" value="speech"> 语音交互/AI助手</label>
                    <label class="option"><input type="radio" name="interest" value="arm"> 机械臂/抓取</label>
                    <label class="option"><input type="radio" name="interest" value="ai"> AI/深度学习</label>
                </div>
            </div>
            
            <!-- Q10: Goal -->
            <div class="question">
                <div class="question-num">问题 10/10</div>
                <div class="question-text">你学习本课程的目标是什么？</div>
                <div class="options">
                    <label class="option"><input type="radio" name="goal" value="interest"> 纯粹兴趣，想了解</label>
                    <label class="option"><input type="radio" name="goal" value="career"> 为将来工作/科研做准备</label>
                    <label class="option"><input type="radio" name="goal" value="project"> 想完成一个机器人项目</label>
                    <label class="option"><input type="radio" name="goal" value="skill"> 掌握一项实用技能</label>
                </div>
            </div>
            
            <button type="submit" class="submit-btn">提交问卷</button>
        </form>
        
        <div id="thanks" class="thanks" style="display:none;">
            <h2>✅ 感谢提交！</h2>
            <p>老师会根据大家的背景调整课程内容</p>
            <p style="margin-top:20px"><a href="/" style="color:#00d4ff;">← 返回首页</a></p>
        </div>
    </div>
    
    <script>
        document.getElementById('surveyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            data.timestamp = new Date().toISOString();
            
            fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(r => r.json()).then(result => {
                if(result.success) {
                    this.style.display = 'none';
                    document.getElementById('thanks').style.display = 'block';
                }
            });
        });
        
        document.querySelectorAll('.option').forEach(opt => {
            opt.addEventListener('click', function() {
                const radio = this.querySelector('input[type="radio"]');
                radio.checked = true;
                this.parentElement.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    </script>
</body>
</html>
'''

# Database functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            major TEXT,
            programming INTEGER DEFAULT 0,
            python INTEGER DEFAULT 0,
            ros INTEGER DEFAULT 0,
            robot INTEGER DEFAULT 0,
            ai INTEGER DEFAULT 0,
            interest TEXT,
            goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    
    db = get_db()
    db.execute('''
        INSERT INTO students (name, student_id, major, programming, python, ros, robot, ai, interest, goal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name', ''),
        data.get('student_id', ''),
        data.get('major', ''),
        data.get('programming', 0),
        data.get('python', 0),
        data.get('ros', 0),
        data.get('robot', 0),
        data.get('ai', 0),
        data.get('interest', ''),
        data.get('goal', '')
    ))
    db.commit()
    
    return {'success': True, 'message': '提交成功！'}

@app.route('/api/stats')
def stats():
    """View survey statistics"""
    db = get_db()
    c = db.cursor()
    
    # Total students
    c.execute('SELECT COUNT(*) as total FROM students')
    total = c.fetchone()['total']
    
    # Major distribution
    c.execute('SELECT major, COUNT(*) as count FROM students GROUP BY major')
    majors = [{'major': row['major'], 'count': row['count']} for row in c.fetchall()]
    
    # Python level distribution
    c.execute('SELECT python, COUNT(*) as count FROM students GROUP BY python')
    python_levels = [{'level': row['python'], 'count': row['count']} for row in c.fetchall()]
    
    return {
        'total': total,
        'majors': majors,
        'python_levels': python_levels
    }

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DB_PATH):
        init_db()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=False)
