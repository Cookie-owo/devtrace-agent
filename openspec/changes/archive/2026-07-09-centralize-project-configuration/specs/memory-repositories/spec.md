## ADDED Requirements

### Requirement: Memory database project configuration
后端 SHALL 从跟踪的项目配置文件中加载 SQLite 内存数据库设置。

#### Scenario: Memory database URL comes from project config
- **WHEN** 后端内存数据库配置已构建
- **THEN** 它 MUST 从跟踪的项目配置中读取数据库 URL，并 MUST NOT 读取本地机器环境变量。

#### Scenario: Alembic uses project config for application migrations
- **WHEN** Alembic 在应用程序启动或开发者迁移命令时运行
- **THEN** 它 MUST 能够从后端应用程序使用的同一跟踪项目配置文件中解析内存数据库 URL 。
