## Why

知识库文档列表较长或展开分片预览后，当前页面的高度与 overflow 约束会裁切后续内容，预览本身也没有独立滚动区域，导致用户无法查看完整文档和后续条目。

## What Changes

- 将知识库桌面工作区改为稳定的受限高度网格，文档区域占用剩余空间。
- 为文档列表提供纵向滚动，同时保留表格横向滚动能力。
- 为展开后的文档详情与分片预览提供有界的独立纵向滚动区域。
- 在窄屏下恢复自然页面滚动，避免嵌套滚动阻碍触控操作。
- 增加布局源码和组件渲染测试，并使用浏览器验证长列表与长预览。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `knowledge-base-ui`: 增加长文档列表和展开预览的可滚动、可访问布局要求。

## Impact

影响 `KnowledgeView`、`KnowledgeDocumentList`、`KnowledgeDocumentDetail` 的 CSS 和前端布局测试；不修改知识库 API 或数据结构。
