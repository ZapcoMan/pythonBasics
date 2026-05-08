import re
import csv
import json
from collections import Counter, defaultdict

def parse_markdown_table(file_path):
    """解析Markdown表格文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 跳过表头和分隔线（前2行）
    for line in lines[2:]:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue

        # 分割字段
        fields = [field.strip() for field in line.split('|')]
        # 移除首尾空字段
        fields = [f for f in fields if f]

        if len(fields) == 4:
            data.append({
                '课题名称': fields[0],
                '学生姓名': fields[1],
                '学生学号': fields[2],
                '函授站': fields[3]
            })

    return data

def save_to_csv(data, output_path):
    """保存为CSV文件"""
    if not data:
        return

    fieldnames = ['课题名称', '学生姓名', '学生学号', '函授站']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ CSV文件已保存: {output_path}")

def analyze_by_station(data):
    """按函授站统计分析"""
    station_counter = Counter([item['函授站'] for item in data])
    print("\n=== 函授站人数统计 ===")
    for station, count in station_counter.most_common():
        print(f"{station}: {count}人")
    return dict(station_counter)

def analyze_technology(data):
    """按技术栈分析"""
    tech_keywords = {
        'SpringBoot': r'spring\s*boot|springboot',
        'Java': r'\bjava\b|\bjavaweb\b',
        'Python': r'\bpython\b',
        'Vue': r'\bvue\b',
        '微信小程序': r'微信.*小程序|小程序',
        '深度学习': r'深度学习|神经网络',
        '区块链': r'区块链',
        'Android': r'\bandroid\b',
        'PHP': r'\bphp\b',
        '大数据': r'大数据|hadoop|spark',
        'Web': r'\bweb\b|b/s',
    }

    tech_counter = Counter()
    for item in data:
        title = item['课题名称'].lower()
        for tech, pattern in tech_keywords.items():
            if re.search(pattern, title, re.IGNORECASE):
                tech_counter[tech] += 1

    print("\n=== 技术栈使用统计 ===")
    for tech, count in tech_counter.most_common():
        print(f"{tech}: {count}个课题")
    return dict(tech_counter)

def extract_keywords(data):
    """提取课题关键词"""
    keywords = []
    for item in data:
        title = item['课题名称']
        # 提取"基于XXX"的技术关键词
        match = re.search(r'基于(.+?)的', title)
        if match:
            keywords.append(match.group(1))

    keyword_counter = Counter(keywords)
    print("\n=== 热门课题方向TOP20 ===")
    for keyword, count in keyword_counter.most_common(20):
        print(f"{keyword}: {count}次")
    return keyword_counter

def generate_summary_report(data, output_path='分析报告.json'):
    """生成综合分析报告"""
    report = {
        '总人数': len(data),
        '函授站分布': analyze_by_station(data),
        '技术栈分布': analyze_technology(data),
        '热门方向': dict(extract_keywords(data).most_common(20)),
        '学生列表': data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 分析报告已保存: {output_path}")

    return report

def main():
    input_file = r'E:\python\Python_project\01_My_Projects\pythonBasics\src\数据处理\Demo20250508\原始数据.txt'

    print("开始处理数据...")

    # 1. 解析数据
    data = parse_markdown_table(input_file)
    print(f"✓ 成功解析 {len(data)} 条记录")

    # 2. 保存为CSV
    csv_output = input_file.replace('.txt', '.csv')
    save_to_csv(data, csv_output)

    # 3. 生成分析报告
    report = generate_summary_report(data)

    # 4. 打印基本统计
    print("\n=== 数据概览 ===")
    print(f"总记录数: {report['总人数']}")
    print(f"函授站数量: {len(report['函授站分布'])}")
    print(f"涉及技术栈: {len(report['技术栈分布'])}种")

    print("\n数据处理完成！")

if __name__ == '__main__':
    main()
