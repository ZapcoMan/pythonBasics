import csv
from pprint import pprint
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 创建线程锁，确保写入文件时的线程安全
lock = threading.Lock()

# 打开CSV文件准备写入数据
f = open('data.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(f)
# 创建DictWriter对象，指定列名
csv_writer = csv.DictWriter(f, fieldnames=[
    '岗位名称',
    '公司名称',
    '公司规模',
    '工作地区',
    '学历要求',
    '工作经验',
    '薪资',
    '联系电话',
    '工作地点',
    '全职/兼职',
    '岗位描述',
])
# 写入表头
csv_writer.writeheader()

# 设置请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/",
    "Cookie": "Hm_lvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740156; HMACCOUNT=F9272A1A931930E9; Hm_lpvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740747"
}

def fetch_job_details(record):
    """
    获取单个职位的详细信息
    """
    try:
        # 构造职位详情页URL
        url = "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/internet/r/c/webpage/homepage/position/detail/" + record['bcb009']

        # 发送GET请求获取职位详情
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        json_data = response.json()

        # 提取所需字段信息
        dit = {
            '岗位名称': json_data['data']['bce055'],
            '公司名称': json_data['data']['aab004'],
            '公司规模': json_data['data']['aab056Name'],
            '工作地区': json_data['data']['acb204Name'],
            '学历要求': json_data['data']['aac011Name'],
            '工作经验': json_data['data']['aae162Name'],
            '薪资': json_data['data']['bcca68'],
            '联系电话': json_data['data']['aae005'],
            '工作地点': json_data['data']['acc530'],
            '全职/兼职': json_data['data']['acb239Name'],
            '岗位描述': json_data['data']['acb22a'],
        }

        # 使用线程锁确保写入文件的线程安全
        with lock:
            csv_writer.writerow(dit)

        print(f"已爬取职位: {json_data['data']['bce055']}")
        return dit
    except Exception as e:
        print(f"获取职位详情失败: {e}")
        return None

def fetch_job_list(page):
    """
    获取指定页码的职位列表
    """
    try:
        # 构造职位列表请求URL
        link = 'https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/internet/retrieval/c/recruitment/homepage/positions'
        # 请求参数
        data = {"bce055": "", "acb241": "", "acb242": "", "aab056": "", "lately": -1, "bze433": "", "aac011": "", "aae162": "",
                "acb239": "", "acb204": "440000000000", "acb204Name": "广东省", "gzxz": "0", "releaseType": "1",
                "pageTag": "01", "acb118": None, "bae045": "05", "orderType": "01", "current": page, "size": 40, "bcb687": ""}

        # 发送POST请求获取职位列表
        link_data = requests.post(link, json=data, headers=headers)
        link_data.raise_for_status()  # 检查请求是否成功
        jsonLinkData = link_data.json()
        records = jsonLinkData['data']['records']

        print(f"已获取第 {page} 页职位列表，共 {len(records)} 个职位")
        return records
    except Exception as e:
        print(f"获取第 {page} 页职位列表失败: {e}")
        return []

# 使用多线程爬取数据
def main():
    # 创建线程池，设置合适的线程数
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交职位列表请求任务
        future_to_page = {executor.submit(fetch_job_list, page): page for page in range(1, 10)}

        # 收集所有职位记录
        all_records = []
        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                records = future.result()
                all_records.extend(records)
            except Exception as e:
                print(f"处理第 {page} 页结果时出错: {e}")

        # 提交职位详情请求任务
        print(f"开始获取 {len(all_records)} 个职位的详细信息...")
        detail_futures = {executor.submit(fetch_job_details, record): record for record in all_records}

        # 等待所有任务完成
        completed = 0
        for future in as_completed(detail_futures):
            try:
                result = future.result()
                completed += 1
                print(f"进度: {completed}/{len(all_records)}")
            except Exception as e:
                print(f"处理职位详情时出错: {e}")

if __name__ == "__main__":
    main()
    f.close()  # 关闭文件
