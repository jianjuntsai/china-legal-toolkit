# Changelog

## [3.0.0] - 2026-05-10

### Changed
- 项目重命名为 `china-legal-toolkit`，由单一 Skill 扩展为四模块工具包
- 重构目录结构：`prc-legal-research/` 拆分为 `law-search/`、`case-search/`、`company-info/`、`legal-research/` 四个独立 Skill 目录
- 共享代码迁移至 `shared/`（config、tavily_search）
- 原 `yuandian_api.py` 拆分为三个专项模块：`law_api.py`、`case_api.py`、`company_api.py`

### Added
- **新 Skill：法条检索**（`law-search/`）— 支持关键词/精确/语义三种检索模式
- **新 Skill：裁判文书检索**（`case-search/`）— 支持主题/案号/权威案例/语义四种检索模式
- **新 Skill：企业信息查询**（`company-info/`）— 支持 21 个接口，含工商/风险/诉讼/股权/知识产权
- `company_api.py` 新增 19 个企业信息接口（聚合总览、涉诉、信用风险、股权、知识产权等）

---

## [2.1.0] - 2026-05-06

### Added
- `search_fatiao_semantic(query, ...)` — 法条语义检索（向量检索），调用元典 `POST /open/law_vector_search`
- `search_case_semantic(query, ...)` — 案例语义检索（向量检索），调用元典 `POST /open/case_vector_search`
- SKILL.md 新增"关键词检索 vs 语义检索使用原则"说明
- SKILL.md 第五阶段新增"5.2.1 语义检索补充"，明确触发条件与使用方式

---

## [2.0.0] - 2026-04-13

### Changed
- 升级为八阶段工作流（新增第四阶段：二手文献分析）
- 备忘录增加"九、关键资料溯引图"（mermaid）

### Added
- evals/iteration-2：四组评测案例及评测报告
- examples：对应的法律备忘录示例文件

---

## [1.0.0] - 2026-04-12

### Added
- 初始版本发布
- 七阶段法律研究工作流
- 元典 API 封装（`yuandian_api.py`）：法规/法条关键词检索、案例检索、企业信息
- Tavily 二手文献检索封装（`tavily_search.py`）
- 法律备忘录标准输出格式
- 引用格式规范（`references/引用格式要求.md`）
