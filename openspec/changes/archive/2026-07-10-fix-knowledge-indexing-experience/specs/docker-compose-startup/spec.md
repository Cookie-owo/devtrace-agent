## MODIFIED Requirements

### Requirement: Milvus stack managed by compose
Compose 堆栈 SHALL 通过 Docker Compose 使用本地可拉取的独立 Milvus 镜像标签来管理 Milvus 独立实例及其所需依赖项。

#### Scenario: Milvus dependencies are compose services
- **WHEN** 检查 Compose 文件
- **THEN** etcd 和 MinIO MUST 应被声明为 Milvus 所依赖的服务。

#### Scenario: Milvus and Attu ports are exposed
- **WHEN** 检查 Compose 文件
- **THEN** Milvus MUST 暴露端口 19530，而 Attu MUST 暴露本地 UI 端口。

#### Scenario: Milvus 镜像标签支持本地启动
- **WHEN** 启动本地 Compose Milvus 服务
- **THEN** 配置的 Milvus 独立镜像标签 MUST 应该可被拉取并通过 Compose health 检查报告 healthy。
