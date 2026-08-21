## MODIFIED Requirements

### Requirement: ### 需求：由 Compose 提供的 Milvus 运行时
后端 Milvus 向量存储 SHALL 将 Docker Compose Milvus 服务视为其本地运行时依赖项，并 SHALL NOT 从应用程序代码中启动 Milvus。

#### Scenario: Local settings target compose service
- **WHEN** 后端项目配置文件被检查
- **THEN** 它们 MUST 包含与 Compose 管理的 Milvus 服务兼容的 Milvus URI 和集合设置。

#### Scenario: Vector settings come from project config
- **WHEN** 后端向量存储配置已构建
- **THEN** 它从跟踪的项目配置文件中读取 MUST、collection、dimension、index、metric 和 search 设置，并从本地机器环境变量中 MUST NOT 读取。

#### Scenario: Application code does not launch Milvus
- **WHEN** 向量存储代码已检查
- **THEN** 它 MUST NOT 通过 Docker 执行 shell 命令，启动 Milvus 进程，或依赖 bat 或 sh 启动脚本。
