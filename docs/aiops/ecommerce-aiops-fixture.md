# Java 电商微服务 AIOps 测试数据

这套辅助数据用于验证真实 CLS、Alertmanager、知识库检索和 AIOps 证据链。应用服务仍在本地运行，Docker 只需提供 Milvus 与 Alertmanager 等基础设施。

## 数据规模与关联

脚本一次生成 10 套 Java 电商微服务故障。每套包含：

- 1 条带异常、指标、阈值和依赖信息的 CLS 关键日志；
- 1 条带 `environment=test`、`fixture=java-ecommerce` 的活动告警；
- 1 份包含告警依据、CLS 查询、根因假设、排查、恢复与验证的 Markdown SOP；
- 1 个独立的 32 位 trace ID。

三类数据通过 `incident_id`、`service`、`alertname`、`sop` 关联，告警 annotations 和 SOP 都包含相同 trace ID。

| # | Java 服务 | 告警 | 故障逻辑 |
|---|---|---|---|
| 1 | `payment-service` | `PaymentGatewayTimeoutHigh` | 支付网关 TLS/读取超时导致订单停留在 PAYING |
| 2 | `inventory-service` | `InventoryReservationLockWaitHigh` | 补库存长事务与热门 SKU 预占发生行锁竞争 |
| 3 | `order-service` | `OrderDatabasePoolExhausted` | 无分页慢查询占满 HikariCP 连接池 |
| 4 | `cart-service` | `CartRedisLatencyHigh` | 促销索引热 key 大对象反序列化阻塞 Redis |
| 5 | `api-gateway` | `GatewayCheckoutCircuitOpen` | 库存服务错误触发结算熔断器打开 |
| 6 | `promotion-service` | `PromotionRuleEvaluationCpuHigh` | 组合促销规则导致指数级计算和 CPU 饱和 |
| 7 | `order-event-consumer` | `OrderEventConsumerLagHigh` | 新枚举值反序列化失败，poison message 持续重试 |
| 8 | `product-search-service` | `ProductSearchTimeoutHigh` | wildcard 查询耗尽 Elasticsearch search 线程池 |
| 9 | `auth-service` | `AuthJwkRefreshFailureHigh` | key 轮换后代理 DNS 故障导致 JWK 缓存无法刷新 |
| 10 | `fulfillment-service` | `FulfillmentProviderUnavailable` | 物流供应商 503 且无退避重试造成请求放大 |

## 执行步骤

1. 启动所需基础设施：

   ```bash
   docker compose -f infra/compose.yaml up -d etcd minio milvus attu alertmanager
   ```

2. 使用本地启动脚本或开发命令启动后端、前端和 CLS MCP Server。

3. 上传 10 条真实 CLS 日志：

   ```bash
   cd apps/backend
   uv run python scripts/generate_and_upload_cls_logs.py --profile java-ecommerce
   ```

4. 向本地 Alertmanager 发布 10 条活动告警：

   ```bash
   uv run python scripts/publish_java_ecommerce_alerts.py --profile java-ecommerce
   ```

5. 为配置的演示用户上传并索引 10 份 SOP：

   ```bash
   uv run python scripts/seed_java_ecommerce_aiops_sops.py --profile java-ecommerce
   ```

6. 打开 AIOps 工作区，刷新活动告警，选择任一 Java 电商告警进行诊断。CLS 查询应命中告警 annotations 中的 trace ID，Planner 应能检索到同名 SOP。

## 兼容量化场景

原有量化服务 fixture 保留，可显式执行：

```bash
uv run python scripts/generate_and_upload_cls_logs.py --profile quant --count 16
uv run python scripts/publish_ecommerce_quant_alert.py --profile quant
uv run python scripts/seed_ecommerce_aiops_sop.py --profile quant
```

所有数据均为 `test` fixture，不包含真实用户信息、密码、token 或云凭据。重复上传 SOP 使用稳定文件名和 overwrite 策略。
