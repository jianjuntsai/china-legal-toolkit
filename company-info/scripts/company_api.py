"""
企业信息 API 接口库
包含：企业检索、基本信息、涉诉、信用风险、股权、知识产权等 21 个接口
认证：X-Api-Key 头部
文档：https://open.chineselaw.com/docs
"""

import requests
import sys
import os

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
sys.path.insert(0, os.path.join(SKILLS_DIR, "shared"))
from config import API_KEY

BASE_URL_OLD = "https://apiplatform.legalmind.cn/open"
BASE_URL = "https://open.chineselaw.com/open"

HEADERS_GET = {
    "accept": "application/json;charset=UTF-8",
    "X-Api-Key": API_KEY,
}


def _get_old(path, params):
    """旧接口 GET 请求封装（apiplatform.legalmind.cn）"""
    resp = requests.get(f"{BASE_URL_OLD}{path}", headers=HEADERS_GET, params=params)
    result = resp.json()
    if result.get("status") == "success":
        return result.get("data")
    else:
        print(f"[错误] {path}: {result.get('message')}")
        return None


def _get(path, params):
    """新接口 GET 请求封装（open.chineselaw.com）"""
    resp = requests.get(f"{BASE_URL}{path}", headers=HEADERS_GET, params=params)
    result = resp.json()
    if result.get("status") == "success":
        return result.get("data")
    else:
        print(f"[错误] {path}: {result.get('message')}")
        return None


# ──────────────────────────────────────────────
# 基础查询
# ──────────────────────────────────────────────

def search_company_by_name(name, num=2):
    """
    按企业名称/股票简称搜索企业
    - name: 企业名称或股票简称等检索词【必填】
    - num: 返回条数，默认2，最大50
    返回: list[dict] 企业列表，含工商基本信息
    """
    params = {"name": name, "num": num}
    return _get_old("/rh_company_info", params)


def get_company_detail(id=None, tyshxydm=None):
    """
    按企业ID或统一社会信用代码精确查询企业详情
    - id: 企业 ID（与 tyshxydm 至少填一个，优先用 id）
    - tyshxydm: 统一社会信用代码
    返回: dict 企业详情，含工商信息/股东/知识产权/涉诉/风险等
    """
    params = {}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get_old("/rh_company_detail", params)


def get_company_agg_summary(id=None, tyshxydm=None):
    """
    企业聚合总览（18类信息统计概览）
    - id: 企业 ID（与 tyshxydm 至少填一个）
    - tyshxydm: 统一社会信用代码
    返回: dict 含18类信息的统计数据和 TOP20 条目
    推荐作为企业风险摸排的快速入口
    """
    params = {}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseAggregationSummary", params)


# ──────────────────────────────────────────────
# 涉诉信息
# ──────────────────────────────────────────────

def get_company_lawsuit_stats(id=None, tyshxydm=None):
    """
    企业涉诉信息统计
    - id / tyshxydm: 企业标识（至少填一个）
    返回: dict 涉诉案件按多维度分布统计
    """
    params = {}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWritAgg", params)


def get_company_lawsuit_list(id=None, tyshxydm=None, pageNo=1):
    """
    企业涉诉文书列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1（每页约30条）
    返回: dict 含 lst（文书列表）和分页信息
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWritList", params)


def get_company_court_sessions(id=None, tyshxydm=None, pageNo=1):
    """
    企业开庭公告列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    返回: dict 含开庭公告列表和分页信息
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCourtSessionNotice", params)


def get_company_court_notices(id=None, tyshxydm=None, pageNo=1):
    """
    企业法院公告列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    返回: dict 含法院公告列表和分页信息
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCourtNotice", params)


# ──────────────────────────────────────────────
# 信用风险
# ──────────────────────────────────────────────

def get_company_dishonest_exec(id=None, tyshxydm=None, pageNo=1):
    """
    企业失信被执行人信息列表（老赖名单）
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseExecutions", params)


def get_company_executed(id=None, tyshxydm=None, pageNo=1):
    """
    企业被执行人信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseExecutedPerson", params)


def get_company_serious_illegal(id=None, tyshxydm=None, pageNo=1):
    """
    企业严重违法记录列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseSeriousIllegal", params)


def get_company_abnormal_op(id=None, tyshxydm=None, pageNo=1):
    """
    企业经营异常记录列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseAbnormalOperation", params)


def get_company_tax_arrear(id=None, tyshxydm=None, pageNo=1):
    """
    企业欠税公告记录列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCorporateTax", params)


# ──────────────────────────────────────────────
# 股权与融资
# ──────────────────────────────────────────────

def get_company_equity_frozen(id=None, tyshxydm=None, pageNo=1):
    """
    企业股权冻结信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseFrozenEquity", params)


def get_company_equity_pledge(id=None, tyshxydm=None, pageNo=1):
    """
    企业股权出质信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterprisePledge", params)


def get_company_investments(id=None, tyshxydm=None, pageNo=1):
    """
    企业对外投资信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseOutInvest", params)


def get_company_guarantees(id=None, tyshxydm=None, pageNo=1):
    """
    企业对外担保信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseGuaranty", params)


# ──────────────────────────────────────────────
# 知识产权与证书
# ──────────────────────────────────────────────

def get_company_trademarks(id=None, tyshxydm=None, pageNo=1):
    """
    企业商标信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseBrand", params)


def get_company_patents(id=None, tyshxydm=None, pageNo=1):
    """
    企业专利信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterprisePatent", params)


def get_company_software_copyrights(id=None, tyshxydm=None, pageNo=1):
    """
    企业软件著作权信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseSoftRight", params)


def get_company_works_copyrights(id=None, tyshxydm=None, pageNo=1):
    """
    企业作品著作权信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWorksRight", params)


def get_company_icp(id=None, tyshxydm=None, pageNo=1):
    """
    企业网站备案（ICP）信息列表
    - id / tyshxydm: 企业标识（至少填一个）
    - pageNo: 页码，默认1
    """
    params = {"pageNo": pageNo}
    if id:
        params["id"] = id
    if tyshxydm:
        params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseIcp", params)
