import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.todo import Todo
from app.models.finance import Finance
from app.models.learning import Learning
from app.models.health import WeightLoss

DATABASE_URL = "sqlite:///./personal_manager.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

hashed_password = bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

user = User(
    username="hzs",
    email="hzs@example.com",
    hashed_password=hashed_password,
    balance=1000.0
)
db.add(user)
db.commit()
db.refresh(user)

todos = [
    {"title": "完成项目报告", "content": "编写项目进度报告", "priority": 3, "date": "2026-07-22", "completed": False},
    {"title": "学习Python", "content": "学习FastAPI框架", "priority": 2, "date": "2026-07-22", "completed": True},
    {"title": "购买日用品", "content": "购买牙膏、洗发水", "priority": 1, "date": "2026-07-21", "completed": True},
    {"title": "健身", "content": "去健身房锻炼1小时", "priority": 2, "date": "2026-07-22", "completed": False},
    {"title": "阅读书籍", "content": "阅读《代码大全》", "priority": 2, "date": "2026-07-22", "completed": False},
    {"title": "整理文档", "content": "整理项目文档", "priority": 3, "date": "2026-07-23", "completed": False},
    {"title": "开会", "content": "参加项目例会", "priority": 3, "date": "2026-07-22", "completed": True},
    {"title": "写代码", "content": "完成功能开发", "priority": 3, "date": "2026-07-22", "completed": False},
    {"title": "复习考试", "content": "复习Python考试", "priority": 2, "date": "2026-07-24", "completed": False},
    {"title": "打扫卫生", "content": "打扫房间卫生", "priority": 1, "date": "2026-07-22", "completed": True},
    {"title": "做饭", "content": "准备晚餐", "priority": 1, "date": "2026-07-22", "completed": False},
    {"title": "洗衣服", "content": "清洗衣物", "priority": 1, "date": "2026-07-21", "completed": True},
    {"title": "回复邮件", "content": "回复工作邮件", "priority": 2, "date": "2026-07-22", "completed": False},
    {"title": "学习Vue", "content": "学习Vue3组合式API", "priority": 2, "date": "2026-07-25", "completed": False},
    {"title": "看电影", "content": "观看电影", "priority": 1, "date": "2026-07-22", "completed": True},
    {"title": "写日记", "content": "记录今日心情", "priority": 1, "date": "2026-07-22", "completed": False},
    {"title": "学习英语", "content": "背诵英语单词", "priority": 2, "date": "2026-07-22", "completed": True},
    {"title": "购物", "content": "购买生活用品", "priority": 1, "date": "2026-07-26", "completed": False},
    {"title": "旅游计划", "content": "制定旅游计划", "priority": 2, "date": "2026-07-22", "completed": False},
    {"title": "学习SQL", "content": "学习SQL查询优化", "priority": 3, "date": "2026-07-22", "completed": False},
]

for todo_data in todos:
    todo = Todo(user_id=user.id, **todo_data)
    db.add(todo)

finances = [
    {"type": "income", "category": "工资", "amount": 5000.0, "description": "月薪", "date": "2026-07-01"},
    {"type": "expense", "category": "餐饮", "amount": 500.0, "description": "日常餐饮", "date": "2026-07-05"},
    {"type": "expense", "category": "交通", "amount": 200.0, "description": "地铁费用", "date": "2026-07-06"},
    {"type": "income", "category": "副业", "amount": 1000.0, "description": "兼职收入", "date": "2026-07-10"},
    {"type": "expense", "category": "购物", "amount": 300.0, "description": "购买衣服", "date": "2026-07-15"},
    {"type": "income", "category": "工资", "amount": 5500.0, "description": "月薪", "date": "2027-01-01"},
    {"type": "expense", "category": "餐饮", "amount": 600.0, "description": "日常餐饮", "date": "2027-01-05"},
]

for finance_data in finances:
    finance = Finance(user_id=user.id, **finance_data)
    db.add(finance)

learnings = [
    {"project": "Python学习", "category": "计算机", "outline": "第一章：Python基础语法（变量、数据类型、运算符）；第二章：流程控制（条件语句、循环结构）；第三章：函数与模块；第四章：面向对象编程；第五章：文件操作与异常处理", "estimated_duration": 480, "accumulated_duration": 120, "progress": 25, "start_date": "2026-07-01"},
    {"project": "FastAPI框架", "category": "计算机", "outline": "第一章：FastAPI入门与环境搭建；第二章：路由与请求处理；第三章：数据验证与Pydantic模型；第四章：数据库操作与SQLAlchemy；第五章：认证与授权；第六章：API文档与测试", "estimated_duration": 320, "accumulated_duration": 180, "progress": 56, "start_date": "2026-07-08"},
    {"project": "数据结构", "category": "计算机", "outline": "第一章：数组与链表；第二章：栈与队列；第三章：树与二叉树；第四章：图与图算法；第五章：哈希表；第六章：排序与查找算法", "estimated_duration": 300, "accumulated_duration": 45, "progress": 15, "start_date": "2026-07-15"},
    {"project": "高等数学", "category": "数学", "outline": "第一章：函数与极限；第二章：导数与微分；第三章：微分中值定理；第四章：不定积分；第五章：定积分；第六章：微分方程", "estimated_duration": 480, "accumulated_duration": 90, "progress": 19, "start_date": "2026-07-05"},
    {"project": "线性代数", "category": "数学", "outline": "第一章：行列式；第二章：矩阵及其运算；第三章：矩阵的初等变换；第四章：向量组的线性相关性；第五章：相似矩阵与二次型", "estimated_duration": 240, "accumulated_duration": 120, "progress": 50, "start_date": "2026-07-03"},
    {"project": "概率论", "category": "数学", "outline": "第一章：随机事件与概率；第二章：随机变量及其分布；第三章：数字特征；第四章：大数定律与中心极限定理；第五章：数理统计基础", "estimated_duration": 200, "accumulated_duration": 30, "progress": 15, "start_date": "2026-07-12"},
    {"project": "词汇背诵", "category": "英语", "outline": "第一阶段：CET-4核心词汇（2000词）；第二阶段：CET-6进阶词汇（1500词）；第三阶段：考研英语词汇（2000词）；第四阶段：专业领域词汇", "estimated_duration": 200, "accumulated_duration": 60, "progress": 30, "start_date": "2026-07-10"},
    {"project": "语法学习", "category": "英语", "outline": "第一章：时态与语态；第二章：从句（定语从句、状语从句、名词性从句）；第三章：非谓语动词；第四章：虚拟语气；第五章：倒装与强调", "estimated_duration": 160, "accumulated_duration": 80, "progress": 50, "start_date": "2026-07-08"},
    {"project": "阅读训练", "category": "英语", "outline": "第一章：精读技巧（词汇理解、句子分析）；第二章：泛读训练（快速阅读、信息抓取）；第三章：题型解析（主旨题、细节题、推断题）；第四章：真题练习与模拟", "estimated_duration": 150, "accumulated_duration": 20, "progress": 13, "start_date": "2026-07-14"},
]

for learning_data in learnings:
    learning = Learning(user_id=user.id, **learning_data)
    db.add(learning)

weight_loss_records = [
    {"date": "2026-07-01", "weight": 80.0, "height": 170.0},
    {"date": "2026-07-02", "weight": 79.8, "height": 170.0},
    {"date": "2026-07-03", "weight": 79.6, "height": 170.0},
    {"date": "2026-07-04", "weight": 79.5, "height": 170.0},
    {"date": "2026-07-05", "weight": 79.3, "height": 170.0},
    {"date": "2026-07-06", "weight": 79.2, "height": 170.0},
    {"date": "2026-07-07", "weight": 79.0, "height": 170.0},
    {"date": "2026-07-08", "weight": 78.9, "height": 170.0},
    {"date": "2026-07-09", "weight": 78.7, "height": 170.0},
    {"date": "2026-07-10", "weight": 78.5, "height": 170.0},
    {"date": "2026-07-11", "weight": 78.4, "height": 170.0},
    {"date": "2026-07-12", "weight": 78.2, "height": 170.0},
    {"date": "2026-07-13", "weight": 78.0, "height": 170.0},
    {"date": "2026-07-14", "weight": 77.8, "height": 170.0},
    {"date": "2026-07-15", "weight": 77.7, "height": 170.0},
    {"date": "2026-07-16", "weight": 77.5, "height": 170.0},
    {"date": "2026-07-17", "weight": 77.4, "height": 170.0},
    {"date": "2026-07-18", "weight": 77.2, "height": 170.0},
    {"date": "2026-07-19", "weight": 77.0, "height": 170.0},
    {"date": "2026-07-20", "weight": 76.9, "height": 170.0},
    {"date": "2026-07-21", "weight": 76.8, "height": 170.0},
    {"date": "2026-07-22", "weight": 76.6, "height": 170.0},
]

for record_data in weight_loss_records:
    record = WeightLoss(user_id=user.id, **record_data)
    db.add(record)

db.commit()

print("示例数据初始化完成！")
print(f"用户: hzs, 密码: 123")
print(f"创建了 {len(todos)} 条待办事项")
print(f"创建了 {len(finances)} 条财务记录")
print(f"创建了 {len(learnings)} 条学习记录")

db.close()
