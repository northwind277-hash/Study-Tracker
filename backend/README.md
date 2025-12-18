# StudyTracker Backend

StudyTracker是一个面向研究生/学生的学习任务与学习行为分析平台，这是项目的后端部分，使用FastAPI框架开发。

## 技术栈

- **Web框架**: FastAPI 0.115.0
- **数据库**: SQLAlchemy 2.0.35
- **数据库类型**: SQLite（默认）
- **认证**: JWT (JSON Web Token)
- **数据验证**: Pydantic 2.9.2
- **开发服务器**: Uvicorn 0.32.0

## 项目结构

```
backend/
├── app/
│   ├── core/           # 核心配置（数据库、安全等）
│   ├── db/             # 数据库相关（会话、模型基类）
│   ├── models/         # 数据库模型
│   ├── schemas/        # 数据验证和序列化
│   ├── crud/           # CRUD操作
│   ├── services/       # 业务逻辑服务
│   ├── api/            # API接口
│   │   └── v1/         # API版本1
│   └── utils/          # 工具函数
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行开发服务器

```bash
uvicorn app.main:app --reload
```

服务器将在 `http://localhost:8000` 上运行。

### 3. 访问API文档

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API接口

### 认证接口

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录

### 任务接口

- `GET /api/v1/tasks` - 获取所有任务
- `POST /api/v1/tasks` - 创建新任务
- `GET /api/v1/tasks/{id}` - 获取单个任务
- `PUT /api/v1/tasks/{id}` - 更新任务
- `DELETE /api/v1/tasks/{id}` - 删除任务

### 学习记录接口

- `GET /api/v1/records` - 获取所有学习记录（可按日期范围过滤）
- `POST /api/v1/records` - 创建新学习记录
- `GET /api/v1/records/{id}` - 获取单个学习记录
- `PUT /api/v1/records/{id}` - 更新学习记录
- `DELETE /api/v1/records/{id}` - 删除学习记录

### 统计接口

- `GET /api/v1/stats/daily` - 获取每日学习统计
- `GET /api/v1/stats/task` - 获取任务学习时间统计
- `GET /api/v1/stats/total` - 获取总学习统计
- `GET /api/v1/stats/weekly` - 获取最近几周的学习统计

## 数据库设计

### 用户表 (users)

- id: 用户ID (主键)
- username: 用户名 (唯一)
- email: 邮箱 (唯一)
- password_hash: 加密密码
- created_at: 注册时间

### 任务表 (tasks)

- id: 任务ID (主键)
- user_id: 所属用户ID (外键)
- title: 任务标题
- description: 任务描述
- priority: 优先级 (1低 2中 3高)
- status: 状态 (0未开始 1进行中 2完成)
- created_at: 创建时间

### 学习记录表 (study_records)

- id: 记录ID (主键)
- user_id: 用户ID (外键)
- task_id: 任务ID (外键)
- record_date: 学习日期
- duration: 学习分钟数
- created_at: 创建时间

## 配置说明

项目配置主要在 `app/core/config.py` 中定义，支持通过 `.env` 文件覆盖默认配置。

主要配置项：

- `DATABASE_URL`: 数据库连接URL
- `SECRET_KEY`: JWT密钥
- `ALGORITHM`: JWT算法
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌过期时间（分钟）

## 开发建议

1. 使用虚拟环境进行开发
2. 每完成一个功能模块后编写测试
3. 遵循PEP 8代码风格规范
4. 使用FastAPI提供的依赖注入系统管理依赖
5. 对于复杂业务逻辑，使用服务层（services）进行封装

## 许可证

MIT
