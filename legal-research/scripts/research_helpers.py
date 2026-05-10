"""
法律研究 Skill 辅助模块
从各专项模块导入所有 API 函数，供 legal-research Skill 使用
"""

import sys
import os

_base = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(_base, "../../law-search/scripts"))
sys.path.insert(0, os.path.join(_base, "../../case-search/scripts"))
sys.path.insert(0, os.path.join(_base, "../../company-info/scripts"))
sys.path.insert(0, os.path.join(_base, "../../shared"))

from law_api import (
    search_fagui,
    get_fagui_detail,
    search_fatiao,
    get_fatiao_detail,
    search_fatiao_semantic,
)

from case_api import (
    search_qwal,
    search_ptal,
    get_case_detail,
    search_case_semantic,
)

from company_api import (
    search_company_by_name,
    get_company_detail,
)

from tavily_search import (
    search_secondary_sources,
    search_lawfirm_articles,
    search_government_interpretations,
    search_academic_sources,
)

__all__ = [
    "search_fagui", "get_fagui_detail", "search_fatiao", "get_fatiao_detail",
    "search_fatiao_semantic",
    "search_qwal", "search_ptal", "get_case_detail", "search_case_semantic",
    "search_company_by_name", "get_company_detail",
    "search_secondary_sources", "search_lawfirm_articles",
    "search_government_interpretations", "search_academic_sources",
]
