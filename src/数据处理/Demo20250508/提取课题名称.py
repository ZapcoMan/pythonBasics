"""
从原始数据中提取课题名称
"""
import re


def extract_project_titles(file_path):
    """
    从Markdown表格文件中提取所有课题名称
    
    Args:
        file_path: 原始数据文件路径
        
    Returns:
        list: 课题名称列表
    """
    titles = []
    
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
        
        if len(fields) >= 1:
            title = fields[0]
            if title:  # 确保课题名称不为空
                titles.append(title)
    
    return titles


def save_titles_to_file(titles, output_path):
    """
    将课题名称保存到文本文件
    
    Args:
        titles: 课题名称列表
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, title in enumerate(titles, 1):
            f.write(f"{i}. {title}\n")
    
    print(f"✓ 已保存 {len(titles)} 个课题名称到: {output_path}")


def save_titles_to_txt_simple(titles, output_path):
    """
    将课题名称保存为纯文本格式（每行一个）
    
    Args:
        titles: 课题名称列表
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for title in titles:
            f.write(title + '\n')
    
    print(f"✓ 已保存 {len(titles)} 个课题名称到: {output_path}")


def main():
    # 输入文件路径
    input_file = r'E:\python\Python_project\01_My_Projects\pythonBasics\src\数据处理\Demo20250508\原始数据.txt'
    
    print("开始提取课题名称...")
    
    # 提取课题名称
    titles = extract_project_titles(input_file)
    
    print(f"✓ 成功提取 {len(titles)} 个课题名称\n")
    
    # 打印前10个课题名称作为示例
    print("=== 前10个课题名称示例 ===")
    for i, title in enumerate(titles[:10], 1):
        print(f"{i}. {title}")
    
    print(f"... 共 {len(titles)} 个课题\n")
    
    # 保存为带编号的文本文件
    output_file_numbered = input_file.replace('原始数据.txt', '课题名称列表_带编号.txt')
    save_titles_to_file(titles, output_file_numbered)
    
    # 保存为纯文本格式（每行一个，方便后续处理）
    output_file_simple = input_file.replace('原始数据.txt', '课题名称列表.txt')
    save_titles_to_txt_simple(titles, output_file_simple)
    
    # 统计分析
    print("\n=== 课题名称分析 ===")
    
    # 统计包含特定关键词的课题数量
    keywords = {
        'SpringBoot': 0,
        'Java': 0,
        'Python': 0,
        'Vue': 0,
        '微信小程序': 0,
        '深度学习': 0,
        '管理系统': 0,
        '设计与实现': 0,
    }
    
    for title in titles:
        title_lower = title.lower()
        if 'springboot' in title_lower or 'spring boot' in title_lower:
            keywords['SpringBoot'] += 1
        if 'java' in title_lower or 'javaweb' in title_lower:
            keywords['Java'] += 1
        if 'python' in title_lower:
            keywords['Python'] += 1
        if 'vue' in title_lower:
            keywords['Vue'] += 1
        if '微信' in title and '小程序' in title:
            keywords['微信小程序'] += 1
        if '深度学习' in title or '神经网络' in title:
            keywords['深度学习'] += 1
        if '管理系统' in title:
            keywords['管理系统'] += 1
        if '设计与实现' in title or '设计与开发' in title:
            keywords['设计与实现'] += 1
    
    print("技术/类型统计：")
    for keyword, count in keywords.items():
        print(f"  {keyword}: {count}个课题")
    
    print("\n数据处理完成！")


if __name__ == '__main__':
    main()
