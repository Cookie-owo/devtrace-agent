## Context

当前 `ChatView` 同时渲染历史会话、对话正文和提示词/Skill 配置三列，而 `WorkspaceLayout` 的全局侧栏只包含路由导航。会话状态已经由 Pinia `chat` store 统一管理，因此可由布局和聊天视图共享，不需要复制数据源。系统提示词组件会在每次 `configuration` 对象变化且没有展开项时自动展开选中项，Skill 保存引起的配置对象替换因此覆盖了用户的折叠选择。

## Goals / Non-Goals

**Goals:**

- 桌面端在全局左侧栏的“对话”入口之后展示新建入口和历史会话。
- 聊天工作区移除桌面历史列，为对话正文提供更大宽度。
- user 与 assistant 消息使用相同的透明正文容器，同时保留 user 靠右、assistant 靠左的阅读分流。
- 聊天工作区内的可聚焦控件和输入容器不显示绿色或灰色焦点矩形框。
- 固定 AIOps 桌面工作区高度，长报告在报告正文内部滚动。
- Chat、Knowledge 和 AIOps 根视图铺满全局 header 以下的剩余桌面空间。
- 配置保存刷新后保持系统提示词的展开/收起状态。

**Non-Goals:**

- 不修改会话 API、排序方式或持久化模型。
- 不改变提示词与 Skill 的选择契约。
- 不把会话历史长期复制到组件本地状态。
- 不实现移动端专用导航、抽屉或响应式替代入口；本项目前端仅面向桌面 Web。

## Decisions

- `WorkspaceLayout` 读取现有 `chat` store，并通过 `WorkspaceNavigation` 的命名插槽把 `ChatSessionList` 放在对话导航项之后。相较让导航组件直接依赖业务 store，插槽保持全局导航可复用且明确了视觉顺序。
- `ChatSessionList` 增加 `rail` 外观变体。桌面侧栏使用深色、紧凑、可滚动样式，所有操作继续通过 emit 调用同一 chat store。
- `ChatView` 桌面布局改为对话和配置两列，不再渲染第二份历史会话组件。
- `ChatTranscript` 删除 user 专属背景、圆角、内边距和内容宽度规则；保留 user 外层的右对齐，消息仍通过“你/助手”角色标签区分，并共用现有长文本换行保护。
- 删除聊天 composer 的 `:focus-within` 视觉规则，并在 `.chat-view` 范围内覆盖表单控件、按钮和链接的 `:focus`/`:focus-visible` outline。该决定按产品要求优先消除矩形焦点框，作用域不扩散到其他工作区。
- `ChatPromptSidebar` 使用一次性初始化标志：仅首次收到非空配置时根据当前选择初始化展开项。后续 Skill 保存、提示词选择或其他配置刷新只同步草稿，不重置 `expandedIds`。
- `AiopsView` 使用与聊天工作区一致的桌面视口高度约束，三栏容器不再由内容撑高。中栏采用状态、报告、过程三行网格；`AiopsReportPanel` 的标题和报告元信息固定，Markdown 正文成为独立纵向滚动容器。
- `WorkspaceLayout` 主区使用 `auto minmax(0, 1fr)` 两行网格，路由内容容器移除 `max-width`、居中和 padding。Chat/AIOps 根视图直接占满 `height: 100%`；Knowledge 根视图占满画布并在自身内部滚动和提供内容间距。
- 视觉继续采用现有深色 rail 和浅色内容面，不采纳与运维工作台不匹配的高饱和紫色方案；交互按钮保持 Lucide 图标、明确 aria-label 和至少 44px 的窄屏点击区域。

## Risks / Trade-offs

- [布局与 ChatView 同时挂载时可能重复初始化] → 保留 `ChatView.initialize()` 作为唯一网络初始化入口，布局只消费 store 状态和调用已有操作。
- [配置首次加载后选中提示词发生变化不会自动展开] → “使用中”标记仍会更新；展开状态属于用户局部 UI 选择，必须优先保持。
