# China Legal Toolkit

面向中国境内法律研究的 Claude Code Skills 工具包，基于[元典 API](https://open.chineselaw.com/) 和 [Tavily](https://www.tavily.com/) 构建，提供四个独立 Skill 模块。

## 四个 Skill

| Skill | 目录 | 说明 |
|-------|------|------|
| **法条检索** | `law-search/` | 精确查询/主题检索法律条文原文，支持关键词与语义双模式 |
| **裁判文书检索** | `case-search/` | 权威案例与普通案例检索，支持按主题、法院、地域、时间筛选 |
| **企业信息查询** | `company-info/` | 企业工商信息、风险摸排（诉讼/失信/违法）、股权、知识产权等 21 类查询 |
| **法律研究** | `legal-research/` | 综合性法律研究 Skill，生成标准法律研究备忘录（Markdown） |

## 数据来源

| 类型 | 来源 | 用途 |
|------|------|------|
| 权威法律渊源（Primary Sources） | [元典 API](https://open.chineselaw.com/)（法条原文、裁判文书、企业信息） | 结论的唯一权威依据 |
| 二手文献（Secondary Sources） | [Tavily](https://www.tavily.com/)（律所文章、政府解读、学术论文） | 法律研究 Skill 专用，构建分析框架 |

## 安装

### 1. 克隆仓库

```bash
git clone <仓库地址>
cd china-legal-toolkit
```

### 2. 配置 API Key

```bash
cp shared/config.example.py shared/config.py
```

编辑 `shared/config.py`，填入 API Key：

```python
API_KEY = "你的元典API密钥"          # 前往 https://apiplatform.legalmind.cn/ 获取
TAVILY_API_KEY = "你的TavilyAPI密钥"  # 前往 https://www.tavily.com/ 获取（法律研究 Skill 专用）
```

> 如使用 Claude Code，首次启动 Skill 时会自动检测到未配置的 Key，引导你输入。

### 3. 安装 Skill

将所需 Skill 目录安装到 Claude Code：

```bash
# 安装法条检索 Skill
cp -r law-search ~/.claude/skills/

# 安装裁判文书检索 Skill
cp -r case-search ~/.claude/skills/

# 安装企业信息查询 Skill
cp -r company-info ~/.claude/skills/

# 安装综合法律研究 Skill
cp -r legal-research ~/.claude/skills/
```

### 4. 安装 Python 依赖

```bash
pip install requests tavily-python
```

## 法律研究 Skill 输出格式

法律研究 Skill 生成标准法律研究备忘录（`法律备忘录_{主题}_{日期}.md`），包含：

```
一、核心结论
二、研究前提与适用范围
三、主要规则依据（法条原文）
四、分析
五、实务观点（二手文献观点）
六、风险与不确定性
七、结论与实务建议
八、主要法规依据清单
九、关键资料溯引图（mermaid）
```

## 目录结构

```
china-legal-toolkit/
├── README.md
├── CHANGELOG.md
├── CLAUDE.md
│
├── shared/                         # 共享基础设施
│   ├── config.example.py           # API Key 配置模板
│   ├── config.py                   # API Key 配置（本地，不提交 Git）
│   └── tavily_search.py            # Tavily 二手文献检索
│
├── law-search/                     # Skill 1：法条检索
│   ├── SKILL.md
│   └── scripts/
│       └── law_api.py              # 法规/法条 API（5个接口）
│
├── case-search/                    # Skill 2：裁判文书检索
│   ├── SKILL.md
│   └── scripts/
│       └── case_api.py             # 案例 API（4个接口）
│
├── company-info/                   # Skill 3：企业信息查询
│   ├── SKILL.md
│   └── scripts/
│       └── company_api.py          # 企业信息 API（21个接口）
│
├── legal-research/                 # Skill 4：综合法律研究
│   ├── SKILL.md
│   ├── references/
│   │   └── 引用格式要求.md
│   └── scripts/
│       └── research_helpers.py     # 汇总导入各模块 API
│
├── examples/                       # 法律备忘录示例
├── evals/                          # Skill 评测数据
└── outputs/                        # 实际运行输出
```

## 注意事项

- 法律研究备忘录仅供参考，不构成正式法律意见，建议交由执业律师复核
- API 调用会产生费用，请参考[元典 API](https://open.chineselaw.com/) 和 [Tavily](https://www.tavily.com/) 各自定价
- 首次注册元典 API 可免费享有 1000 积分；Tavily 免费用户可享有 1000 次/月权益

## License

MIT
