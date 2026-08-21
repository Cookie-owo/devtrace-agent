## Context

知识库页面位于固定高度且 overflow hidden 的工作区。当前文档 body 没有 `minmax(0, 1fr)` 高度轨道，列表只有横向滚动，展开详情和分片预览没有最大高度，因此内容会撑开或被祖先裁切。

## Goals / Non-Goals

**Goals:**

- 桌面端长文档列表在剩余工作区内纵向滚动。
- 展开详情和分片预览具有清晰、独立的滚动区域。
- 窄屏保持自然页面滚动和触控可用性。

**Non-Goals:**

- 不改变文档表格列、预览数据数量或 API。
- 不重构知识库视觉风格。

## Decisions

- 桌面端 `KnowledgeView` 使用 `auto auto minmax(0, 1fr)`，body/documents 逐层设置 `min-height: 0` 与 overflow 约束。
- `KnowledgeDocumentList` 同时使用 `overflow: auto`，承担长列表纵向滚动和窄表格横向滚动。
- 详情区域设置基于 viewport 的 `max-height` 和 `overflow-y: auto`，预览列表也有内部上限，保证后续文档仍可访问。
- 小屏 media query 切回 `height:auto` 和 visible overflow，避免三层嵌套滚动。

## Risks / Trade-offs

- [嵌套滚动可能影响移动端] → 仅桌面启用有界内部滚动，窄屏恢复文档流。
- [固定上限在矮屏过小] → 使用 `clamp()` 与 `dvh` 计算响应式高度。
