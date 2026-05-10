"""
法律法规 API 接口库
包含：法规/法条关键词检索、详情获取、语义检索
认证：X-Api-Key 头部
文档：https://open.chineselaw.com/docs
"""

import requests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../shared"))
from config import API_KEY

BASE_URL = "https://apiplatform.legalmind.cn/open"
SEMANTIC_BASE_URL = "https://open.chineselaw.com"

HEADERS_JSON = {
    "accept": "application/json;charset=UTF-8",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY,
}


def _post(path, payload):
    """POST 请求封装，返回 data 字段，失败时返回 None 并打印错误"""
    resp = requests.post(f"{BASE_URL}{path}", headers=HEADERS_JSON, json=payload)
    result = resp.json()
    if result.get("status") == "success":
        return result.get("data")
    else:
        print(f"[错误] {path}: {result.get('message')}")
        return None


# ──────────────────────────────────────────────
# 法律法规类
# ──────────────────────────────────────────────

def search_fagui(keyword=None, search_mode=None, fgmc=None, sxx=None,
                 xljb_1=None, fbrq_start=None, fbrq_end=None,
                 ssrq_start=None, ssrq_end=None, top_k=10):
    """
    法规关键词检索
    - keyword: 法规关键词（可不填，此时按过滤条件返回列表）
    - search_mode: AND/OR，默认 AND
    - fgmc: 法规名称过滤
    - sxx: 时效性过滤（现行有效/失效/已被修改/部分失效/尚未生效）
    - xljb_1: 效力级别过滤（宪法/法律/司法解释/行政法规/部门规章等）
    - fbrq_start/fbrq_end: 发布日期范围，格式 yyyy-MM-dd
    - ssrq_start/ssrq_end: 实施日期范围，格式 yyyy-MM-dd
    - top_k: 返回条数，默认10，最大50
    返回: list[dict] 法规列表，每条含 id/fgmc/xljb_1/sxx/fbrq/ssrq/content(高亮片段) 等
    """
    payload = {"top_k": top_k}
    if keyword:
        payload["keyword"] = keyword
    if search_mode:
        payload["search_mode"] = search_mode
    if fgmc:
        payload["fgmc"] = fgmc
    if sxx:
        payload["sxx"] = sxx
    if xljb_1:
        payload["xljb_1"] = xljb_1
    if fbrq_start:
        payload["fbrq_start"] = fbrq_start
    if fbrq_end:
        payload["fbrq_end"] = fbrq_end
    if ssrq_start:
        payload["ssrq_start"] = ssrq_start
    if ssrq_end:
        payload["ssrq_end"] = ssrq_end
    return _post("/rh_fg_search", payload)


def get_fagui_detail(id=None, fgmc=None, refer_date=None):
    """
    法规详情（获取全文 content）
    - id: 法规ID（与 fgmc 至少填一个）
    - fgmc: 法规名称
    - refer_date: 参考日期，格式 yyyy-MM-dd（不填则返回当前有效版本）
    返回: dict 法规详情，含 id/fgmc/xljb_1/sxx/fbrq/ssrq/fbbm/content 等
    """
    payload = {}
    if id:
        payload["id"] = id
    if fgmc:
        payload["fgmc"] = fgmc
    if refer_date:
        payload["refer_date"] = refer_date
    return _post("/rh_fg_detail", payload)


def search_fatiao(keyword, search_mode=None, fgmc=None, sxx=None,
                  xljb_1=None, fbrq_start=None, fbrq_end=None,
                  ssrq_start=None, ssrq_end=None, top_k=10):
    """
    法条关键词检索
    - keyword: 法条关键词（必填）
    - search_mode: AND/OR，默认 AND
    - fgmc: 法规名称过滤
    - sxx: 时效性过滤
    - xljb_1: 效力级别过滤
    - fbrq_start/fbrq_end: 发布日期范围
    - ssrq_start/ssrq_end: 实施日期范围
    - top_k: 返回条数，默认10，最大50
    返回: list[dict] 法条列表，每条含 id/fgid/ftmc/ft_num/fgmc/content/llm_content/sxx 等
    注：llm_content 格式为 "- 《{fgmc}》{ft_num}##{content}"，适合直接传给 LLM
    """
    payload = {"keyword": keyword, "top_k": top_k}
    if search_mode:
        payload["search_mode"] = search_mode
    if fgmc:
        payload["fgmc"] = fgmc
    if sxx:
        payload["sxx"] = sxx
    if xljb_1:
        payload["xljb_1"] = xljb_1
    if fbrq_start:
        payload["fbrq_start"] = fbrq_start
    if fbrq_end:
        payload["fbrq_end"] = fbrq_end
    if ssrq_start:
        payload["ssrq_start"] = ssrq_start
    if ssrq_end:
        payload["ssrq_end"] = ssrq_end
    return _post("/rh_ft_search", payload)


def get_fatiao_detail(id=None, fgmc=None, ftnum=None, refer_date=None):
    """
    法条详情
    - id: 法条ID（与 fgmc+ftnum 至少填一组）
    - fgmc: 法规名称（id 为空时必填）
    - ftnum: 法条号（id 为空时必填，如"第一百条"）
    - refer_date: 参考日期，格式 yyyy-MM-dd
    返回: dict 法条详情，含 id/fgid/ftmc/ft_num/fgmc/content/sxx/xljb_1/fbrq/ssrq 等
    """
    payload = {}
    if id:
        payload["id"] = id
    if fgmc:
        payload["fgmc"] = fgmc
    if ftnum:
        payload["ftnum"] = ftnum
    if refer_date:
        payload["refer_date"] = refer_date
    return _post("/rh_ft_detail", payload)


def search_fatiao_semantic(query, rewrite_flag=True, sxx=None, effect1=None,
                           law_start=None, law_end=None, return_num=20):
    """
    法律法规语义检索（向量检索）
    - query: 自然语言查询文本（必填），如"合同解除后的违约金如何认定"
    - rewrite_flag: 是否对查询做改写，默认 True
    - sxx: 时效性过滤列表，如 ["现行有效"]
    - effect1: 一级效力级别列表，如 ["法律", "司法解释"]
    - law_start/law_end: 法条生效日期范围，格式 yyyy-MM-dd
    - return_num: 返回法条数量，默认 20
    返回: list[dict] 法条列表，每条含 ftid/fgid/fgtitle/num/content/sxx/effect1/score 等
    适用场景：问题模糊、术语不确定、或需要发现潜在相关法条时
    """
    payload = {"query": query, "rewrite_flag": rewrite_flag, "return_num": return_num}
    fatiao_filter = {}
    if sxx:
        fatiao_filter["sxx"] = sxx if isinstance(sxx, list) else [sxx]
    if effect1:
        fatiao_filter["effect1"] = effect1 if isinstance(effect1, list) else [effect1]
    if law_start:
        fatiao_filter["law_start"] = law_start
    if law_end:
        fatiao_filter["law_end"] = law_end
    if fatiao_filter:
        payload["fatiao_filter"] = fatiao_filter

    resp = requests.post(
        f"{SEMANTIC_BASE_URL}/open/law_vector_search",
        headers=HEADERS_JSON,
        json=payload,
    )
    result = resp.json()
    if result.get("code") in (200, 201):
        return result.get("extra", {}).get("fatiao", [])
    else:
        print(f"[错误] law_vector_search: {result.get('msg')}")
        return None
