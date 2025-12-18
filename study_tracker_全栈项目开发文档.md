# StudyTracker 全栈项目开发文档

> **项目定位**：面向研究生/学生的学习任务与学习行为分析平台  
> **技术栈**：FastAPI + Vue3 + JWT + ECharts  
> **目标**：在真实工程结构下，完成一个可持续扩展、可升级为 AI / 毕设的中等复杂度项目

---

## 一、项目背景与目标

### 1.1 背景
- 学习任务零散，缺乏统一管理
- 学习过程缺乏量化反馈
- 现有工具偏记录，缺乏分析能力

### 1.2 项目目标
- 管理学习任务（Task）
- 记录学习行为（StudyRecord）
- 对学习数据进行统计分析
- 提供可视化结果
- 为后续 AI / 智能分析预留接口

---

## 二、系统总体架构

```
Vue3 Frontend
    |
  Axios
    |
FastAPI Backend
    ├── Auth (JWT)
    ├── Task
    ├── StudyRecord
    ├── Stats (Service)
    |
SQLAlchemy ORM
    |
Database
```

---

## 三、功能需求分析（PRD）

### 3.1 用户系统
- 用户注册
- 用户登录
- JWT 鉴权
- 接口访问控制

### 3.2 学习任务管理
- 创建任务
- 编辑任务
- 删除任务
- 查询任务列表
- 修改任务状态

任务属性：
- 标题
- 描述
- 优先级（低/中/高）
- 状态（未开始/进行中/完成）

### 3.3 学习记录模块
- 新增学习记录
- 关联任务
- 记录学习日期与时长
- 查询时间区间内记录

### 3.4 数据统计模块（核心亮点）
- 每日学习时长统计
- 各任务学习时间占比
- 任务完成率统计

---

## 四、后端项目目录结构

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── record.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── record.py
│   │   └── stats.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── record.py
│   ├── services/
│   │   ├── stats.py
│   │   └── record.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── task.py
│   │       ├── record.py
│   │       └── stats.py
│   └── utils/
│       └── time.py
├── requirements.txt
└── README.md
```

---

## 五、数据库设计

### 5.1 User 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 用户 ID |
| username | VARCHAR(50) | 唯一 |
| email | VARCHAR(100) | 唯一 |
| password_hash | VARCHAR(255) | 加密密码 |
| created_at | DATETIME | 注册时间 |

### 5.2 Task 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 任务 ID |
| user_id | INT FK | 所属用户 |
| title | VARCHAR(100) | 标题 |
| description | TEXT | 描述 |
| priority | INT | 1低 2中 3高 |
| status | INT | 0未开始 1进行中 2完成 |
| created_at | DATETIME | 创建时间 |

### 5.3 StudyRecord 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 记录 ID |
| user_id | INT FK | 用户 |
| task_id | INT FK | 任务 |
| record_date | DATE | 学习日期 |
| duration | INT | 学习分钟数 |
| created_at | DATETIME | 创建时间 |

---

## 六、API 设计文档

### 6.1 Auth 模块

#### POST /api/v1/auth/register
```json
{ "username": "test", "email": "test@mail.com", "password": "123456" }
```

#### POST /api/v1/auth/login
```json
{ "username": "test", "password": "123456" }
```

返回：
```json
{ "access_token": "xxx", "token_type": "bearer" }
```

---

### 6.2 Task 模块

#### POST /api/v1/tasks
```json
{ "title": "学习 FastAPI", "description": "接口开发", "priority": 2 }
```

#### GET /api/v1/tasks

#### PUT /api/v1/tasks/{id}

#### DELETE /api/v1/tasks/{id}

---

### 6.3 StudyRecord 模块

#### POST /api/v1/records
```json
{ "task_id": 1, "record_date": "2025-12-16", "duration": 120 }
```

#### GET /api/v1/records?start=2025-12-01&end=2025-12-31

---

### 6.4 Stats 模块（Service 层）

#### GET /api/v1/stats/daily
```json
[{ "date": "2025-12-16", "total_minutes": 180 }]
```

#### GET /api/v1/stats/task
```json
[{ "task": "FastAPI", "minutes": 300 }]
```

---

## 七、Service 层设计原则

### 7.1 何时使用 Service
- 一个接口涉及多个表
- 一个业务流程包含多步骤
- 多个接口复用同一业务逻辑

### 7.2 推荐调用链
```
API → Service → CRUD → Model
```

---

## 八、开发阶段规划（建议）

### 阶段一（基础版）
- 用户系统
- 任务管理
- 学习记录

### 阶段二（增强版）
- 数据统计
- Service 层重构

### 阶段三（智能版）
- 学习标签
- 学习笔记
- AI 学习分析

---

## 九、项目可演进方向

- AI 学习建议
- RAG + 学习笔记问答
- 学习效率预测
- 毕业设计升级版本

---

## 十、学习与开发建议

- 每个模块独立完成并测试
- 接口优先，前端后写
- 每完成一个模块写小总结

> **这是一个可以不断成长的项目，而不是一次性作业。**

