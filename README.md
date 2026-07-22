# Personal Manager

一个个人管理系统，包含待办事项、财务记录、学习记录和体重管理功能。

## 功能特性

- **待办事项**：管理日常任务，支持添加、编辑、删除和标记完成
- **财务记录**：记录收入和支出，查看月度统计和每日详情
- **学习记录**：记录学习项目和学习时长
- **体重管理**：记录体重变化，查看趋势图表和历史记录

## 技术栈

- **前端**：Vue 3 + Element Plus + Vite
- **后端**：FastAPI + SQLAlchemy + SQLite
- **认证**：JWT + OAuth2

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+

### 安装步骤

1. **克隆仓库**
```bash
git clone <repository-url>
cd personal-manager
```

2. **安装后端依赖**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

3. **安装前端依赖**
```bash
cd ../frontend
npm install
```

4. **初始化数据库**
```bash
cd ../backend
python init_sample_data.py
```

5. **启动开发服务器**

后端：
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

前端：
```bash
cd frontend
npm run dev
```

6. **访问应用**

在浏览器中访问：http://localhost:5173

### 默认账号

- 用户名：hzs
- 密码：123

## 项目结构

```
personal-manager/
├── backend/
│   ├── app/
│   │   ├── core/          # 核心配置（数据库、配置文件）
│   │   ├── models/        # 数据模型
│   │   ├── routes/        # API 路由
│   │   ├── schemas/       # Pydantic 模型
│   │   └── utils/         # 工具函数
│   ├── main.py            # 应用入口
│   ├── requirements.txt   # Python 依赖
│   └── init_sample_data.py # 示例数据初始化
├── frontend/
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── components/    # 通用组件
│   │   ├── views/         # 页面组件
│   │   └── App.vue        # 主应用组件
│   └── package.json       # Node.js 依赖
└── README.md
```

## API 接口

### 认证
- `POST /api/auth/login` - 登录
- `POST /api/auth/register` - 注册
- `GET /api/auth/me` - 获取当前用户

### 待办事项
- `GET /api/todo/` - 获取待办列表
- `POST /api/todo/` - 创建待办
- `PUT /api/todo/{id}` - 更新待办
- `DELETE /api/todo/{id}` - 删除待办

### 财务记录
- `GET /api/finance/` - 获取财务记录
- `POST /api/finance/` - 创建财务记录
- `GET /api/finance/wallet` - 获取钱包余额
- `GET /api/finance/monthly-stats` - 获取月度统计

### 学习记录
- `GET /api/learning/` - 获取学习记录
- `POST /api/learning/` - 创建学习记录

### 健康记录
- `GET /api/health/weight-loss/` - 获取体重记录
- `POST /api/health/weight-loss/` - 创建体重记录

## 部署

### 打包前端
```bash
cd frontend
npm run build
```

### 运行后端（生产模式）
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 许可证

MIT License
