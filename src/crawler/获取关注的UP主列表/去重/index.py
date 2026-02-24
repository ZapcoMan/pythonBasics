import re
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

def main():
    # 文件路径
    file1 = r'E:\python\Python_project\pythonBasics\src\crawler\获取关注的UP主列表\BeginningAll_bilibili_followingsList.txt'
    file2 = r'E:\python\Python_project\pythonBasics\src\crawler\获取关注的UP主列表\WallyVibe_bilibili_followings_List.txt'
    output_file = r'E:\python\Python_project\pythonBasics\src\crawler\获取关注的UP主列表\deduplicated_up_list.txt'

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
        for i, up in enumerate(unique_ups[:1000], 1):
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
    print(f"重复率: {duplicate_count/total_records*100:.2f}%")

if __name__ == "__main__":
    main()
