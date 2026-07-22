# Personal Manager - 个人管理系统

一个基于 Vue 3 + FastAPI 的个人管理系统，包含学习管理、减肥追踪、财务管理和待办事项等功能。

## 功能特性

- **学习管理**: 添加学习项目，记录预计时间和累计学习时长
- **减肥追踪**: 记录每日体重，查看体重变化趋势图表
- **财务管理**: 记录收支，查看月度统计
- **待办事项**: 添加、完成和管理日常任务
- **用户认证**: 登录/注册系统

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus 组件库
- Vue Router
- Axios

### 后端
- FastAPI
- SQLAlchemy
- SQLite
- JWT 认证

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+

### 在 Windows 上运行

#### 方法一：使用构建脚本（推荐）

1. 打开命令提示符 (CMD) 或 PowerShell

2. 克隆项目到本地：
```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
```

3. 运行构建脚本：
```bash
build.bat
```

4. 在浏览器中访问：http://localhost:8000

5. 使用默认账号登录：
   - 用户名：hzs
   - 密码：123

#### 方法二：手动运行

1. 克隆项目：
```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
```

2. 安装前端依赖并构建：
```bash
cd frontend
npm install
npm run build
```

3. 安装后端依赖：
```bash
cd ../backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. 初始化数据库并启动服务：
```bash
python init_sample_data.py
python main.py
```

5. 在浏览器中访问：http://localhost:8000

### 在 macOS/Linux 上运行

```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
./build.sh
```

## 项目结构

```
personal-manager/
├── backend/                  # 后端代码
│   ├── app/                  # 应用核心
│   │   ├── core/             # 配置和数据库
│   │   ├── models/           # 数据模型
│   │   ├── routes/           # API 路由
│   │   ├── schemas/          # 数据验证
│   │   └── utils/            # 工具函数
│   ├── main.py               # 入口文件
│   └── requirements.txt      # Python 依赖
├── frontend/                 # 前端代码
│   ├── src/                  # 源代码
│   │   ├── views/            # 页面组件
│   │   ├── api/              # API 调用
│   │   └── router/           # 路由配置
│   └── package.json          # Node.js 依赖
├── build.bat                 # Windows 构建脚本
└── build.sh                  # macOS/Linux 构建脚本
```

## 默认账号

- 用户名：hzs
- 密码：123

## License

MIT
