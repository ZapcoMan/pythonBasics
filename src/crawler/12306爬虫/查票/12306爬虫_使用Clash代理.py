"""
12306 爬虫 - 使用 Clash 代理自动切换 IP

功能：
- 查询 12306 火车票信息
- 使用 Clash 自动切换代理服务
- 自动/手动切换节点
- 统计请求成功率和 IP 使用情况

用法：
    python 12306爬虫_使用Clash代理.py
"""

import sys
import time
import random
import requests
from prettytable import PrettyTable
from urllib3.exceptions import InsecureRequestWarning
import warnings

# 关闭 SSL 警告
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# 导入 Clash 自动切换服务
sys.path.insert(0, r'E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\12306爬虫\查票')
from clash_auto_switch_service import ClashAutoSwitchService


# 12306 查票 API 接口
API_URL = (
    "https://kyfw.12306.cn/otn/leftTicket/queryO"
    "?leftTicketDTO.train_date={date}"
    "&leftTicketDTO.from_station={from_station}"
    "&leftTicketDTO.to_station={to_station}"
    "&purpose_codes=ADULT"
)

# User-Agent 列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]

# Cookie（需要根据实际情况更新）
COOKIE = '_uab_collina=173449375088168679444499; JSESSIONID=003C9E88F16CE95CAA005B9B6C852578; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_wfdc_flag=dc; BIGipServerotn=1658388746.50210.0000; BIGipServerpassport=921174282.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromDate=2024-12-19; _jc_save_toDate=2024-12-19'


def get_headers():
    """生成随机请求头"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Cookie': COOKIE,
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
    }


def parse_ticket_data(result_item):
    """解析单条票务数据"""
    fields = result_item.split('|')
    
    return {
        '车次': fields[3],
        '出发站': fields[6],
        '到达站': fields[7],
        '出发时间': fields[8],
        '到达时间': fields[9],
        '耗时': fields[10],
        '商务座': fields[32] if len(fields) > 32 else '--',
        '一等座': fields[31] if len(fields) > 31 else '--',
        '二等座': fields[30] if len(fields) > 30 else '--',
        '特等座': fields[25] if len(fields) > 25 else '--',
        '软卧': fields[23] if len(fields) > 23 else '--',
        '硬卧': fields[28] if len(fields) > 28 else '--',
        '软座': fields[24] if len(fields) > 24 else '--',
        '硬座': fields[29] if len(fields) > 29 else '--',
        '无座': fields[26] if len(fields) > 26 else '--',
        '高级软卧': fields[21] if len(fields) > 21 else '--',
    }


def print_ticket_table(ticket_list):
    """打印票务表格"""
    tb = PrettyTable()
    tb.field_names = [
        '序号', '车次', '出发时间', '到达时间', '耗时',
        '商务座', '一等座', '二等座', '特等座',
        '软卧', '硬卧', '软座', '硬座', '无座', '高级软卧'
    ]
    
    for idx, ticket in enumerate(ticket_list, 1):
        tb.add_row([
            idx,
            ticket['车次'],
            ticket['出发时间'],
            ticket['到达时间'],
            ticket['耗时'],
            ticket['商务座'],
            ticket['一等座'],
            ticket['二等座'],
            ticket['特等座'],
            ticket['软卧'],
            ticket['硬卧'],
            ticket['软座'],
            ticket['硬座'],
            ticket['无座'],
            ticket['高级软卧'],
        ])
    
    print(tb)
    print(f"\n共查询到 {len(ticket_list)} 趟列车")


def query_tickets_with_clash(service, date="2024-12-19", from_station="BJP", to_station="SHH"):
    """使用 Clash 代理查询票务信息"""
    url = API_URL.format(date=date, from_station=from_station, to_station=to_station)
    proxy = service.get_proxy()
    current_node = service.get_current_node()
    
    print(f"\n当前节点: {current_node}")
    print(f"查询: {from_station} -> {to_station} ({date})")
    print("-" * 60)
    
    try:
        response = requests.get(
            url=url,
            headers=get_headers(),
            proxies=proxy,
            timeout=15,
            verify=False
        )
        
        if response.status_code == 200:
            json_data = response.json()
            result = json_data.get('data', {}).get('result', [])
            
            if result:
                ticket_list = [parse_ticket_data(item) for item in result]
                print_ticket_table(ticket_list)
                return True, len(result)
            else:
                print("未查询到票务数据")
                return True, 0
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False, 0
            
    except requests.exceptions.ProxyError as e:
        print(f"代理错误: {e}")
        return False, 0
    except requests.exceptions.Timeout:
        print("请求超时")
        return False, 0
    except Exception as e:
        print(f"请求异常: {e}")
        return False, 0


def main():
    print("=" * 60)
    print("12306 爬虫 - Clash 自动切换 IP")
    print("=" * 60)
    
    # 创建 Clash 自动切换服务
    service = ClashAutoSwitchService(
        clash_secret="1212121",
        clash_proxy_port=7899,
        switch_interval=15,  # 每 15 秒自动切换
    )
    
    # 启动自动切换
    service.start()
    print(f"当前节点: {service.get_current_node()}")
    print(f"可用节点数: {len(service.get_nodes())}")
    print(f"切换间隔: {service.switch_interval} 秒")
    print()
    
    # 统计信息
    total_requests = 0
    success_requests = 0
    failed_requests = 0
    total_tickets = 0
    ips_seen = set()
    
    # 多次查询演示（模拟自动切换）
    query_count = 5
    
    for i in range(query_count):
        print(f"\n{'='*60}")
        print(f"第 {i+1} 次查询")
        print(f"{'='*60}")
        
        total_requests += 1
        success, ticket_count = query_tickets_with_clash(service)
        
        if success:
            success_requests += 1
            total_tickets += ticket_count
            # 记录 IP（这里简化处理，实际可以通过 httpbin.org/ip 获取）
            ips_seen.add(f"node_{service.get_current_node()}")
        else:
            failed_requests += 1
        
        # 等待一段时间让自动切换生效
        if i < query_count - 1:
            print(f"\n等待 5 秒后进行下一次查询...")
            time.sleep(5)
    
    # 手动切换演示
    print(f"\n{'='*60}")
    print("手动切换节点演示")
    print(f"{'='*60}")
    
    print(f"当前节点: {service.get_current_node()}")
    service.switch_node()
    print(f"切换后: {service.get_current_node()}")
    
    # 再查询一次
    total_requests += 1
    success, ticket_count = query_tickets_with_clash(service)
    if success:
        success_requests += 1
        total_tickets += ticket_count
    else:
        failed_requests += 1
    
    # 停止服务
    service.stop()
    
    # 打印统计信息
    print(f"\n{'='*60}")
    print("统计信息")
    print(f"{'='*60}")
    print(f"总请求数: {total_requests}")
    print(f"成功: {success_requests}")
    print(f"失败: {failed_requests}")
    print(f"成功率: {success_requests/total_requests*100:.1f}%" if total_requests > 0 else "成功率: 0%")
    print(f"查询到的车票总数: {total_tickets}")
    print(f"使用过的节点数: {len(ips_seen)}")
    print(f"节点列表: {', '.join(ips_seen)}")
    print("\n测试完成！")


if __name__ == "__main__":
    main()