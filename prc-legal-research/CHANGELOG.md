# Changelog

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
