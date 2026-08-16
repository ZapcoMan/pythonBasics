import re
import random
from collections import OrderedDict

def parse_up_list(file_path):
    """解析UP主列表文件，提取UP主名称和链接"""
    up_list = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # 使用正则表达式匹配 "序号. UP主名称 - 链接" 格式
                match = re.match(r'^\d+\.\s*(.+?)\s*-\s*(https://space\.bilibili\.com/\d+)$', line)
                if match:
                    name = match.group(1).strip()
                    url = match.group(2).strip()
                    # 提取用户ID（数字部分）
                    user_id = re.search(r'https://space\.bilibili\.com/(\d+)', url).group(1)
                    up_list.append({
                        'name': name,
                        'url': url,
                        'user_id': user_id
                    })
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

    return up_list

def deduplicate_by_url(up_lists):
    """根据链接地址去重"""
    # 使用OrderedDict保持插入顺序
    unique_ups = OrderedDict()

    for up_list in up_lists:
        for up in up_list:
            # 以用户ID作为唯一标识进行去重
            user_id = up['user_id']
            if user_id not in unique_ups:
                unique_ups[user_id] = up
            else:
                # 如果已存在，可以选择保留信息更完整的记录
                existing = unique_ups[user_id]
                # 这里简单地保留第一个遇到的记录
                pass

    return list(unique_ups.values())

def save_deduplicated_list(up_list, output_file):
    """保存去重后的列表到文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("去重后的UP主关注列表:\n")
            f.write("=" * 50 + "\n\n")

            for i, up in enumerate(up_list, 1):
                f.write(f"{i}. {up['name']} - {up['url']}\n")

            f.write(f"\n总计: {len(up_list)} 个唯一的UP主\n")

        print(f"去重结果已保存到: {output_file}")
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False


def validate_and_fix_ip(ip_address):
    """验证并修复IP地址
    
    Args:
        ip_address (str): 原始IP地址字符串
    
    Returns:
        str: 修复后的合法IP地址
    """
    # 移除可能存在的空格
    ip_address = ip_address.strip()
    
    # 分割IP地址段
    segments = ip_address.split('.')
    
    # 处理不完整的IP地址（少于4段）
    if len(segments) < 4:
        # 为缺失的段随机生成0-255的数字
        while len(segments) < 4:
            segments.append(str(random.randint(0, 255)))
    
    # 处理超过4段的情况
    elif len(segments) > 4:
        segments = segments[:4]
    
    # 修复每个段
    fixed_segments = []
    for segment in segments:
        # 移除前导零（但保留单独的0）
        segment = segment.lstrip('0')
        if not segment:  # 如果全是0，保留一个0
            segment = '0'
        
        try:
            num = int(segment)
            # 如果数字超过255，替换为255
            if num > 255:
                fixed_segments.append('255')
            else:
                fixed_segments.append(str(num))
        except ValueError:
            # 如果转换失败，使用随机数
            fixed_segments.append(str(random.randint(0, 255)))
    
    return '.'.join(fixed_segments)


def process_ip_list(input_file, output_file):
    """处理IP地址列表文件，修复不合法的IP地址
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    
    Returns:
        tuple: (原始IP数量, 修复后IP数量, 修复详情)
    """
    original_ips = []
    fixed_ips = []
    fix_details = []
    
    try:
        # 读取原始IP地址
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                
                original_ips.append(line)
                
                # 修复IP地址
                fixed_ip = validate_and_fix_ip(line)
                fixed_ips.append(fixed_ip)
                
                # 记录修复详情
                if line != fixed_ip:
                    fix_details.append({
                        'line': line_num,
                        'original': line,
                        'fixed': fixed_ip,
                        'reason': get_fix_reason(line, fixed_ip)
                    })
        
        # 保存修复后的IP列表
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("修复后的IP地址列表\n")
            f.write("=" * 50 + "\n\n")
            
            for i, ip in enumerate(fixed_ips, 1):
                f.write(f"{i}. {ip}\n")
            
            f.write(f"\n总计: {len(fixed_ips)} 个IP地址\n")
            
            # 添加统计信息
            f.write("\n" + "=" * 50 + "\n")
            f.write("处理统计:\n")
            f.write(f"原始IP数量: {len(original_ips)}\n")
            f.write(f"修复后IP数量: {len(fixed_ips)}\n")
            f.write(f"修复的IP数量: {len(fix_details)}\n")
            
            if fix_details:
                f.write("\n修复详情:\n")
                f.write("-" * 30 + "\n")
                for detail in fix_details:
                    f.write(f"行 {detail['line']}: {detail['original']} -> {detail['fixed']} ({detail['reason']})\n")
        
        print(f"IP地址处理完成，结果已保存到: {output_file}")
        return len(original_ips), len(fixed_ips), fix_details
        
    except FileNotFoundError:
        print(f"文件未找到: {input_file}")
        return 0, 0, []
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return 0, 0, []


def get_fix_reason(original, fixed):
    """获取IP地址修复原因"""
    if original == fixed:
        return "无需修复"
    
    orig_parts = original.split('.')
    fixed_parts = fixed.split('.')
    
    reasons = []
    
    # 检查是否是不完整IP
    if len(orig_parts) < 4:
        reasons.append("补全缺失段")
    
    # 检查是否有超范围数字
    for i, (orig, fix) in enumerate(zip(orig_parts, fixed_parts)):
        try:
            orig_num = int(orig.lstrip('0') or '0')
            fix_num = int(fix)
            if orig_num > 255 and fix_num == 255:
                reasons.append(f"段{i+1}超出范围({orig_num}->255)")
        except ValueError:
            reasons.append(f"段{i+1}格式错误")
    
    return "; ".join(reasons) if reasons else "其他修复"


if __name__ == "__main__":
    print("=" * 60)
    print("多功能数据处理工具")
    print("=" * 60)
    
    # 选择处理模式
    print("\n请选择处理模式:")
    print("1. 处理UP主关注列表去重")
    print("2. 处理IP地址列表修复")
    print("3. 同时处理两种任务")
    
    choice = input("\n请输入选择 (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        # UP主列表处理
        print("\n" + "=" * 40)
        print("开始处理UP主关注列表...")
        print("=" * 40)
        
        # 文件路径
        # E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\去重\index.py
        file1 = r'E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\BeginningAll_bilibili_followingsList.txt'
        file2 = r'E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\WallyVibe_bilibili_followings_List.txt'
        output_file = r'E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\deduplicated_up_list.txt'

        print("开始读取UP主列表文件...")

        # 读取两个文件
        up_list1 = parse_up_list(file1)
        up_list2 = parse_up_list(file2)

        print(f"从文件1读取到 {len(up_list1)} 个UP主")
        print(f"从文件2读取到 {len(up_list2)} 个UP主")

        # 合并列表
        all_ups = up_list1 + up_list2
        print(f"合并后共有 {len(all_ups)} 个UP主记录")

        # 按链接地址去重
        unique_ups = deduplicate_by_url([up_list1, up_list2])
        print(f"去重后剩余 {len(unique_ups)} 个唯一的UP主")

        # 保存结果
        if save_deduplicated_list(unique_ups, output_file):
            # 打印前10个结果作为示例
            print("\n前10个去重后的UP主:")
            print("-" * 40)
            for i, up in enumerate(unique_ups[:10], 1):
                print(f"{i}. {up['name']} - {up['url']}")

            if len(unique_ups) > 10:
                print(f"... 还有 {len(unique_ups) - 10} 个UP主")

        # 统计重复情况
        total_records = len(all_ups)
        unique_records = len(unique_ups)
        duplicate_count = total_records - unique_records

        print(f"\n统计信息:")
        print(f"总记录数: {total_records}")
        print(f"唯一记录数: {unique_records}")
        print(f"重复记录数: {duplicate_count}")
        print(f"重复率: {duplicate_count / total_records * 100:.2f}%")
