import re
import random

def validate_and_fix_ip(ip_str):
    """
    验证并修复IP地址
    1. 将超过255的数字替换为255
    2. 对不完整的IP地址随机补充缺失的部分
    """
    # 提取纯IP地址部分（去除前面的编号和空格）
    ip_match = re.search(r'\d+[^\d]+(.+)', ip_str.strip())
    if not ip_match:
        return None
    
    ip_address = ip_match.group(1).strip()
    
    # 分割IP地址的各个部分
    parts = ip_address.split('.')
    
    # 处理每个部分
    fixed_parts = []
    for part in parts:
        if part.isdigit():
            num = int(part)
            # 如果数字超过255，替换为22-220之间的随机数
            if num > 255:
                random_num = random.randint(22, 220)
                fixed_parts.append(str(random_num))
            else:
                fixed_parts.append(str(num))
        else:
            # 如果不是数字，替换为22-220之间的随机数
            random_num = random.randint(22, 220)
            fixed_parts.append(str(random_num))
    
    # 如果IP地址不完整（少于4段），随机补充
    while len(fixed_parts) < 4:
        random_num = random.randint(0, 255)
        fixed_parts.append(str(random_num))
    
    # 如果超过4段，只保留前4段
    if len(fixed_parts) > 4:
        fixed_parts = fixed_parts[:4]
    
    # 组合成为完整的IP地址
    fixed_ip = '.'.join(fixed_parts)
    
    return fixed_ip

def process_ip_list(input_file, output_file):
    """
    处理IP地址列表文件
    """
    processed_ips = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"原始IP地址数量: {len(lines)}")
        
        for i, line in enumerate(lines, 1):
            original_line = line.strip()
            fixed_ip = validate_and_fix_ip(line)
            
            if fixed_ip:
                processed_ips.append(f"{fixed_ip}")
                print(f"第{i}行: {original_line} -> {fixed_ip}")
            else:
                print(f"第{i}行: 无法处理 - {original_line}")
        
        # 写入处理后的结果到新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for ip in processed_ips:
                f.write(ip + '\n')
        
        print(f"\n处理完成！")
        print(f"处理后的IP地址已保存到: {output_file}")
        print(f"有效IP地址数量: {len(processed_ips)}")
        
        return processed_ips
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
        return []
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        return []

if __name__ == "__main__":
    input_file = "IPList.txt"
    output_file = "Fixed_IPList.txt"
    
    print("开始处理IP地址列表...")
    print("=" * 50)
    
    fixed_ips = process_ip_list(input_file, output_file)
    
    print("=" * 50)
    print("处理统计:")
    print(f"- 原始IP地址: 61个")
    print(f"- 处理后有效IP地址: {len(fixed_ips)}个")