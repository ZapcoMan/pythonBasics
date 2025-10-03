# waf_demo.py — 极简 WAF demo（FastAPI middleware）
import re, os, time, json, logging
from urllib.parse import unquote_plus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

LOG_PATH = os.getenv("WAF_LOG", "./waf_samples.log")
SCORE_THRESHOLD = int(os.getenv("WAF_BLOCK_SCORE", "100"))  # 默认不拦截（只监控），设小于等于某值可拦截
FAIL_OPEN = os.getenv("WAF_FAIL_OPEN", "1") == "1"

# 规则： (id, regex_str, weight)
RULES = [
    ("sqli_union", r"(?i)\bunion\s+select\b", 50),
    ("sqli_information_schema", r"(?i)information_schema", 40),
    ("xss_tag", r"(?i)<\s*script\b", 30),
    ("xss_event", r"(?i)onerror\s*=|javascript:", 20),
]

# 预编译正则表达式规则以提高匹配效率，并构建权重映射字典
COMPILED = [(rid, re.compile(pat)) for rid, pat, w in [(r[0], r[1], r[2]) for r in RULES]]
WEIGHTS = {r[0]: r[2] for r in RULES}

# 初始化日志记录器，使用JSON格式记录日志便于后续分析
logger = logging.getLogger("waf")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_PATH, encoding="utf8")
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

app = FastAPI()

def normalize_payload(path: str, query: str, ua: str, body: str) -> str:
    """
    对HTTP请求的各个部分进行标准化处理，便于后续检测

    Args:
        path: 请求路径
        query: 查询参数字符串
        ua: User-Agent头部信息
        body: 请求体内容

    Returns:
        str: 标准化后的payload字符串
    """
    # 最基础的正规化：URL decode（一次），小写，拼接
    try:
        q = unquote_plus(query or "")
        b = unquote_plus(body or "")
    except Exception:
        q = query or ""
        b = body or ""
    combined = " ".join([path or "", q, ua or "", b or ""]).lower()
    return combined

@app.middleware("http")
async def waf_middleware(request: Request, call_next):
    """
    WAF中间件，用于检测和拦截恶意请求

    Args:
        request: HTTP请求对象
        call_next: 调用下一个处理函数的回调

    Returns:
        Response: HTTP响应对象
    """
    try:
        body_bytes = await request.body()
        body = body_bytes.decode(errors="ignore")
        ua = request.headers.get("user-agent", "")
        payload = normalize_payload(request.url.path, request.url.query, ua, body)

        score = 0
        matched = []
        for rid, cre in COMPILED:
            if cre.search(payload):
                score += WEIGHTS.get(rid, 10)
                matched.append(rid)

        # 记录请求信息和检测结果
        record = {
            "ts": int(time.time()),
            "src_ip": request.client.host if request.client else None,
            "method": request.method,
            "path": str(request.url.path),
            "query": str(request.url.query),
            "ua": ua,
            "score": score,
            "matched": matched,
            "body_snip": body[:800]
        }
        logger.info(json.dumps(record, ensure_ascii=False))

        # 默认只监控（fail-open）；如需拦截，把 SCORE_THRESHOLD 设为合理值并 FAIL_OPEN=0
        if score >= SCORE_THRESHOLD:
            if FAIL_OPEN:
                # 故障安全：fail-open 时依旧放行，但记录高优先级日志（已记录）
                return await call_next(request)
            else:
                return JSONResponse({"detail": "blocked by waf", "score": score, "matched": matched}, status_code=403)

    except Exception as e:
        # 引擎异常策略：fail-open or fail-closed
        if FAIL_OPEN:
            return await call_next(request)
        else:
            return JSONResponse({"detail": "waf internal error"}, status_code=500)

    return await call_next(request)

@app.get("/health")
async def health():
    """
    健康检查端点

    Returns:
        dict: 包含状态信息的字典
    """
    return {"status": "ok"}

@app.post("/echo")
async def echo(req: Request):
    """
    回显端点，用于测试

    Args:
        req: HTTP请求对象

    Returns:
        dict: 包含请求体内容的字典
    """
    body = await req.body()
    return {"echo": body.decode(errors="ignore")[:1000]}

