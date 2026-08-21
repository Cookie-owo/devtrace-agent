# Knowledge Answer Citation View Specification

## Purpose

在聊天工作区中定义详细的、有证据支持的知识引用，包括分类、实时更新和owner范围内的导航到源文档。

## Requirements

### Requirement: Detailed answer citation presentation
聊天工作区 SHALL 将后端提供的每个知识引用的详细信息暴露给流式或持久化助手回答。

#### Scenario: Assistant answer uses a knowledge citation
- **WHEN** 可见的助手回答包含知识引用
- **THEN** 前端 MUST 显示其源文档标题，限定 chunk 的摘录，当存在时的相关性分数，源分类和元数据，而不虚构缺失字段。

#### Scenario: Citation arrives while streaming
- **WHEN** 一个 `reference.source` 事件在聊天流期间到达
- **THEN** 前端 MUST 在流完成前将返回的引用详情添加到可见的源上下文中。

#### Scenario: Citation is loaded from history
- **WHEN** 使 user 打开一个持久化的聊天会话，并包含已保存的引用
- **THEN** 的前端 MUST 从持久化消息元数据中呈现相同的可用引用详细信息。

### Requirement: Citation source classification and navigation
聊天工作区 SHALL 用于区分普通文档、SOP 和诊断案例，并为可访问的基于文档的引用提供文档导航。

#### Scenario: Knowledge type is supplied
- **WHEN** 引用标识其知识类型  
- **THEN** 前端 MUST 可视地区分 `document`、`sop` 和 `diagnostic-case` 来源。

#### Scenario: Operator opens a cited document
- **WHEN** 一个操作员选择一个包含文档和知识库标识符的引用
- **THEN** 前端 MUST 导航到已认证的知识工作区，并通过其现有的 owner 范围的 API 边界打开该文档。

#### Scenario: Citation has no document target
- **WHEN** 引用没有可访问的文档标识符
- **THEN** 前端 MUST 保留其证据详情和 MUST NOT 显示损坏的导航操作。

### Requirement: Responsive evidence controls
详细的引用显示 SHALL 在桌面和窄视口上仍可读且可用。

#### Scenario: Operator views a citation on a narrow viewport
- **WHEN** 详细控制在狭窄的聊天工作区中显示
- **THEN** 其摘要、元数据和源操作 MUST 会重新排列，而不会导致水平页面溢出。

### Requirement: Visible retrieval stage trace
聊天工作区 SHALL 在知识库引用摘要和详情中展示向量、BM25 和 rerank 三阶段的排名与分数。

#### Scenario: 引用命中三个阶段
- **WHEN** 可见引用包含三个阶段的排名和分数
- **THEN** 前端 MUST 展示向量名次与相似度、BM25 名次与原始分、rerank 名次与相关度。

#### Scenario: 粗召回阶段未命中
- **WHEN** 引用的向量或 BM25 排名为空
- **THEN** 前端 MUST 对该阶段显示“未召回”，并 MUST NOT 伪造排名或分数。

#### Scenario: 移动端展示阶段轨迹
- **WHEN** 三阶段引用摘要位于窄视口
- **THEN** 阶段标签 MUST 自动换行且不得产生水平页面溢出。
