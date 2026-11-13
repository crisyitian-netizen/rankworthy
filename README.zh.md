# Rankworthy

**给 Claude 用的 SEO 与 GEO 技能。** 让网站在 Google 排上去、被 ChatGPT、Google AI 概览和 Perplexity 提到，并衡量有没有带来客户。

## 和其他 SEO skill 的区别

- **以生意结果为准**：每条问题都说明影响哪些询价、电话或订单；没有转化追踪就先补上。
- **改线上网站有安全流程**：备份 → 确认 → 修改 → 记录 → 到期复查；批发价等敏感信息不会出现在页面、结构化数据或 llms.txt 里。
- **每条建议标证据等级**：`[Google]` 官方、`[Study]` 研究数据、`[Practice]` 从业者经验、`[Unproven]` 未经证实。不编数据。
- **零配置、免费数据优先**：普通 Claude 对话里就能用，先用 Search Console、GA4、PageSpeed 和线上网页；付费数据可选，花钱前先报价。
- **本地商家和多语言**：Google 商家资料与评价有完整流程；用你的语言回答。
- **前后对比闭环**：基准数据、固定的 AI 测试问题、改动日志，知道哪些改动有效。

## 工具（Python 3，仅标准库）

```bash
python3 scripts/site_check.py https://你的网站
python3 scripts/gsc_analyze.py 查询.csv --brand "品牌名"
python3 scripts/ai_visibility.py init prompts.txt > log.csv
python3 scripts/ai_visibility.py report log.csv
python3 scripts/dataforseo.py volume "关键词" --location 2840 --lang en   # 可选，付费，默认只预览不扣费
```

## 安装 / 能在哪里用

标准 Agent Skill 格式，不只限 Claude Code：

- **Claude Code**：复制到 `~/.claude/skills/rankworthy/`，脚本本地运行，效果最好。
- **Claude 网页 / 桌面 / 手机应用**：压缩后在 设置 → Capabilities → Skills 上传；需开启代码执行，沙盒可能抓不到部分网站，可改为粘贴 HTML 或上传 GSC 导出。
- **Claude API / Agent SDK**：通过 Skills API 上传。
- **Codex、Cursor、Gemini CLI、Copilot、OpenCode 等支持 SKILL.md 的工具**：放到它们的 skills 目录；脚本需要 Python 3。

然后直接说："帮我审计 example.com，先改什么？"

## 付费数据（可选）

通过 [DataForSEO](DATAFORSEO_REFERRAL_LINK) 获取搜索量、搜索结果、地图排名和外链（按量付费）。*推荐链接说明：通过此链接注册，作者可能获得佣金，你的价格不变；也可以直接去 dataforseo.com 注册。*

MIT 许可证。
