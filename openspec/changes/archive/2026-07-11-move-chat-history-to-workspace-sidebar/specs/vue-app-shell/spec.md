## ADDED Requirements

### Requirement: Chat sessions live in the workspace sidebar
工作区 SHALL 在桌面对话路由的全局左侧栏中提供会话创建和历史会话导航，并使用聊天 store 作为唯一会话状态来源。

#### Scenario: User opens the chat workspace on desktop
- **WHEN** 已登录 user 进入对话路由且桌面左侧栏可见
- **THEN** “对话”导航项之后 MUST 显示新建对话入口和按时间倒序排列的历史会话，聊天主区域 MUST NOT 再显示独立历史列

#### Scenario: User creates a conversation from the rail
- **WHEN** user 点击左侧栏中的新建对话按钮
- **THEN** 前端 MUST 通过现有 chat store 创建并选中新会话，主对话区域 MUST 切换到该会话

#### Scenario: User selects or deletes rail history
- **WHEN** user 在左侧栏选择或删除一项历史会话
- **THEN** 前端 MUST 调用现有会话操作并让左侧栏和主对话区域反映同一状态

### Requirement: Routed workspaces fill the desktop application surface
工作区 SHALL 将全局 header 以下、左侧栏右侧的全部可用桌面空间交给当前路由视图，不得使用居中最大宽度或通用外层留白缩小业务界面。

#### Scenario: User opens a primary workspace
- **WHEN** user 打开对话、知识库或智能诊断任一桌面 Web 路由
- **THEN** 对应根视图 MUST 紧贴路由内容区边界并占满可用宽度和高度，MUST NOT 暴露外围 canvas 留白

#### Scenario: Workspace content is longer than its surface
- **WHEN** 当前业务视图内容超过可用高度
- **THEN** 业务视图 MUST 在自身定义的区域内滚动，MUST NOT 通过全局内容 padding 或文档滚动制造额外留白
