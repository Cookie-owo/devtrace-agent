## Why

后端需要一个持久化的内存层，以便在聊天和AIOps工作流中可以安全地保存对话状态、诊断进度、报告、工具审计记录以及LangGraph checkpoint。现在建立这一点可以为业务代码提供一个稳定的仓库边界，而不是将SQLite表结构泄露到后续服务中。

## 什么更改

- 为聊天会话、消息历史、AIOps 诊断任务、诊断报告、工具调用审计条目和 AIOps LangGraph checkpoints 添加基于 SQLite 的内存存储。
- 为内存模式定义 SQLAlchemy ORM 模型，并通过 Alembic 迁移来管理模式。
- 暴露仓库接口和 SQLite 实现，以便应用程序/业务代码依赖于存储抽象而不是 SQLAlchemy 表、SQL 语句或 SQLite 细节。
- 支持按聊天会话、诊断任务和时间范围进行的历史查询。
- 保持仓库契约的结构，以便以后可以用 PostgreSQL 或其他数据库实现替换 SQLite 而不更改业务服务。

## 功能

### 新功能

- `memory-repositories`：后端内存持久化，SQLAlchemy/Alembic 模式管理，以及聊天、AIOps 诊断、工具审计和 LangGraph checkpoint 数据的仓库合约。

### 修改后的功能

- `project-foundation`: 后端质量检查现在将数据库迁移配置和仓库测试作为后端模板的一部分。

## 影响

- 为 SQLAlchemy、Alembic 和异步 SQLite 访问添加后端依赖项。
- 添加后端内存模型、数据库/会话配置、Alembic 环境和初始迁移、仓库接口以及 SQLite 仓库实现。
- 添加对迁移、仓库行为、查询过滤和仓库边界导入的测试。
- 更新后端文档和本地 SQLite 内存数据库配置的环境示例。
