## ADDED Requirements

### Requirement: Detailed answer citation presentation
聊天工作区 SHALL 将后端提供的每个知识引用的详细信息暴露给流式传输或持久化的助手回答。

#### Scenario: Assistant answer uses a knowledge citation
- **WHEN** 可见的助手回答包含知识引用
- **THEN** 前端 MUST 显示其源文档标题、绑定的 chunk 摘录、相关性分数（如果存在）、源分类和元数据，而不会编造缺失字段。

#### Scenario: Citation arrives while streaming
- **WHEN** 一个 `reference.source` 事件在聊天流期间到达
- **THEN** 前端 MUST 在流完成前将返回的引用详情添加到可见的源上下文中。

#### Scenario: Citation is loaded from history
- **WHEN** 使 user 打开一个带有已保存引用的持久化聊天会话
- **THEN** 使前端 MUST 从持久化消息元数据中渲染相同的可用引用详情

### Requirement: Citation source classification and navigation
聊天工作区 SHALL 用于区分普通文档、SOPs 和诊断案例，并为可访问的基于文档的引用提供文档导航。

#### Scenario: Knowledge type is supplied
- **WHEN** 引用标识符可识别其知识类型  
- **THEN** 前端 MUST 可明显区分 `document`、`sop` 和 `diagnostic-case` 来源。

#### Scenario: Operator opens a cited document
- **WHEN** 一个操作员选择一个带有文档和知识库标识符的引用
- **THEN** 前端 MUST 导航到已认证的知识工作区，并通过其现有的 owner 范围的 API 边界打开该文档。

#### Scenario: Citation has no document target
- **WHEN** 引用没有可访问的文档标识符
- **THEN** 前端 MUST 保留其证据详情和 MUST NOT 显示损坏的导航操作。

### Requirement: Responsive evidence controls
详细的引用显示 SHALL 在台式机和窄视口上仍保持可读且可用。

#### Scenario: Operator views a citation on a narrow viewport
- **WHEN** 详细控件在狭窄的聊天工作区中显示
- **THEN** 其摘要、元数据和源操作 MUST 会重新布局，而不会出现水平页面溢出。
