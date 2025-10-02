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

COMPILED = [(rid, re.compile(pat)) for rid, pat, w in [(r[0], r[1], r[2]) for r in RULES]]
WEIGHTS = {r[0]: r[2] for r in RULES}

# logger (append json-lines)
logger = logging.getLogger("waf")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_PATH, encoding="utf8")
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

app = FastAPI()

def normalize_payload(path: str, query: str, ua: str, body: str) -> str:
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
    return {"status": "ok"}

@app.post("/echo")
async def echo(req: Request):
    body = await req.body()
    return {"echo": body.decode(errors="ignore")[:1000]}
