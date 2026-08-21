# 电商量化定价延迟 SOP

## 范围

请使用此过程处理 `QuantRiskPricingLatencyHigh` 从 `quant-risk-service` 在 `ecommerce-quant` 命名空间中的警报。该警报表示 Java `PricingEngine` 报价计算在服务处理 `CSI300-202607` 估值请求时超过了两秒的 SLO，使用的是 `VAR` 风险模型。

## 预期证据

在活动警报时间窗口内搜索 CLS 的 `quant-risk-service` 事件。相关设备证据包括相同的服务、环境 `test`、SOP 标识符 `ecommerce-quant-pricing-latency-sop`，以及通过 `market_data_retry`、`pricing_executor_saturated`、`quote_calculation_timeout`、`upstream_market_data_unavailable` 和 `pricing_engine_recovered` 的进展。

## 调查

1. 验证警报标签标识 `quant-risk-service`、`critical` 严重性以及活动开始时间。  
2. 检索受影响时间范围内的 CLS 事件，并按 `trace_id` 和 `order_id` 分组。  
3. 确认 `quote_calculation_timeout` 是否在市场数据重试或执行器饱和后发生。  
4. 仅当 `upstream_market_data_unavailable` 出现在同一相关窗口中时，才将其视为依赖性故障的证据。  
5. 如果 `pricing_engine_recovered` 存在，请记录恢复证据，但继续从超时事件评估客户影响。

## 修复

1. 在更改风险计算之前，检查市场数据服务 health 和响应延迟。  
2. 如果定价执行器仍然过载，减少或排队非紧急的估值请求。  
3. 在上游恢复后仍存在超时情况时，升级到量化平台 owner。  
4. 在最终诊断报告中记录警报、跟踪标识符、观察到的延迟和恢复证据。

## 安全性

不要将凭证、客户信息或交易细节放入日志、工单或诊断报告中。结论必须仅限于所获取的 SOP 和工具证据。
