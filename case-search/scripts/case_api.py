"""
裁判文书 API 接口库
包含：权威案例/普通案例关键词检索、案例详情、语义检索
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

HEADERS_GET = {
    "accept": "application/json;charset=UTF-8",
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


def _get(path, params):
    """GET 请求封装，返回 data 字段，失败时返回 None 并打印错误"""
    resp = requests.get(f"{BASE_URL}{path}", headers=HEADERS_GET, params=params)
    result = resp.json()
    if result.get("status") == "success":
        return result.get("data")
    else:
        print(f"[错误] {path}: {result.get('message')}")
        return None


# ──────────────────────────────────────────────
# 案例文书类
# ──────────────────────────────────────────────

def search_qwal(qw=None, search_mode=None, title=None, ah=None,
                ay=None, jbdw=None, xzqh_p=None, wszl=None, ajlb=None,
                ja_start=None, ja_end=None, top_k=10):
    """
    权威案例关键词检索（指导性案例、典型案例等）
    - qw: 全文关键词
    - search_mode: and/or，默认 and
    - title: 标题精确匹配
    - ah: 案号
    - ay: 案由列表（多值为或关系）
    - jbdw: 经办法院列表
    - xzqh_p: 省级行政区列表（北京/上海/广东等）
    - wszl: 文书种类列表（判决书/裁定书/调解书/决定书）
    - ajlb: 案件类别（刑事案件/民事案件/行政案件等）
    - ja_start/ja_end: 裁判日期范围，格式 yyyy-MM-dd
    - top_k: 返回条数，默认10，最大50
    返回: dict，含 total（命中总数）和 lst（列表，每条含 id/ah/title/ay/content/llm_content 等）
    注：请求体不能为空，至少传一个字段（如 top_k）
    """
    payload = {"top_k": top_k}
    if qw:
        payload["qw"] = qw
    if search_mode:
        payload["search_mode"] = search_mode
    if title:
        payload["title"] = title
    if ah:
        payload["ah"] = ah
    if ay:
        payload["ay"] = ay
    if jbdw:
        payload["jbdw"] = jbdw
    if xzqh_p:
        payload["xzqh_p"] = xzqh_p
    if wszl:
        payload["wszl"] = wszl
    if ajlb:
        payload["ajlb"] = ajlb
    if ja_start:
        payload["ja_start"] = ja_start
    if ja_end:
        payload["ja_end"] = ja_end
    return _post("/rh_qwal_search", payload)


def search_ptal(qw=None, fxgc=None, search_mode=None, title=None, ah=None,
                ay=None, jbdw=None, xzqh_p=None, wszl=None, ajlb=None,
                ja_start=None, ja_end=None, yyft=None, ft_search_mode=None,
                top_k=10):
    """
    普通案例关键词检索（裁判文书网等）
    - qw: 全文关键词
    - fxgc: 分析过程关键词（独立检索字段）
    - search_mode: and/or，默认 and
    - title: 标题精确匹配
    - ah: 案号
    - ay: 案由列表
    - jbdw: 经办法院/承办单位列表
    - xzqh_p: 省级行政区列表
    - wszl: 文书种类列表
    - ajlb: 案件类别
    - ja_start/ja_end: 结案/裁判日期范围
    - yyft: 援引法条列表（如 ["中华人民共和国刑法第二条"]，法条号需为中文格式）
    - ft_search_mode: yyft 拼接模式，and/or，默认 and
    - top_k: 返回条数，默认10，最大50
    返回: dict，含 total 和 lst（每条含 id/ah/title/ay/content/llm_content 等）
    """
    payload = {"top_k": top_k}
    if qw:
        payload["qw"] = qw
    if fxgc:
        payload["fxgc"] = fxgc
    if search_mode:
        payload["search_mode"] = search_mode
    if title:
        payload["title"] = title
    if ah:
        payload["ah"] = ah
    if ay:
        payload["ay"] = ay
    if jbdw:
        payload["jbdw"] = jbdw
    if xzqh_p:
        payload["xzqh_p"] = xzqh_p
    if wszl:
        payload["wszl"] = wszl
    if ajlb:
        payload["ajlb"] = ajlb
    if ja_start:
        payload["ja_start"] = ja_start
    if ja_end:
        payload["ja_end"] = ja_end
    if yyft:
        payload["yyft"] = yyft
    if ft_search_mode:
        payload["ft_search_mode"] = ft_search_mode
    return _post("/rh_ptal_search", payload)


def get_case_detail(type, id=None, ah=None):
    """
    案例详情（普通案例或权威案例）
    - type: "ptal"（普通案例）或 "qwal"（权威案例）【必填】
    - id: 案例 ID（与 ah 至少填一个）
    - ah: 案号
    返回: list[dict] 最多10条，普通案例含 content/dsr/fxgc/pjjg 等详细字段
    """
    params = {"type": type}
    if id:
        params["id"] = id
    if ah:
        params["ah"] = ah
    return _get("/rh_case_details", params)


def search_case_semantic(query, rewrite_flag=True, wenshu_type=None, wszl=None,
                         ja_start=None, ja_end=None, dianxing=False,
                         fayuan=None, cj=None, xzqh_p=None, return_num=20):
    """
    案例语义检索（向量检索）
    - query: 自然语言查询文本（必填），如"股东减资退出后债权人追偿"
    - rewrite_flag: 是否对查询做改写，默认 True
    - wenshu_type: 案件类别，如"民事案件"/"刑事案件"/"行政案件"
    - wszl: 文书种类编码列表，如 ["1"]（判决书）
    - ja_start/ja_end: 结案日期范围，格式 yyyy-MM-dd
    - dianxing: False（默认，普通+权威）或 True（仅权威案例）
    - fayuan: 法院名称列表
    - cj: 法院层级，如"最高"/"高级"/"中级"/"基层"
    - xzqh_p: 省级行政区，如"北京"
    - return_num: 返回案例数量，默认 20
    返回: list[dict] 案例列表，每条含 scid/title/ah/ay/ajlb/content/score 等
    适用场景：寻找事实相似判例、案例类比推理、或关键词检索召回不足时
    """
    payload = {"query": query, "rewrite_flag": rewrite_flag, "return_num": return_num}
    wenshu_filter = {"dianxing": dianxing}
    if wenshu_type:
        wenshu_filter["wenshu_type"] = wenshu_type
    if wszl:
        wenshu_filter["wszl"] = wszl if isinstance(wszl, list) else [wszl]
    if ja_start:
        wenshu_filter["ja_start"] = ja_start
    if ja_end:
        wenshu_filter["ja_end"] = ja_end
    if fayuan:
        wenshu_filter["fayuan"] = fayuan if isinstance(fayuan, list) else [fayuan]
    if cj:
        wenshu_filter["cj"] = cj
    if xzqh_p:
        wenshu_filter["xzqh_p"] = xzqh_p
    payload["wenshu_filter"] = wenshu_filter

    resp = requests.post(
        f"{SEMANTIC_BASE_URL}/open/case_vector_search",
        headers=HEADERS_JSON,
        json=payload,
    )
    result = resp.json()
    if result.get("code") in (200, 201):
        return result.get("extra", {}).get("wenshu", [])
    else:
        print(f"[错误] case_vector_search: {result.get('msg')}")
        return None
