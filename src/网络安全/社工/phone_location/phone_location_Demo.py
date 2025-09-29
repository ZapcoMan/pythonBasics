import subprocess
from collections import Counter

# 定义数组
array = [
    134, 135, 136, 137, 138, 139, 147, 148, 150, 151, 152, 157, 158, 159,
    172, 178, 182, 183, 184, 187, 188, 195, 198, 130, 131, 132, 145, 146,
    155, 156, 166, 167, 171, 175, 176, 185, 186, 133, 149, 153, 173, 174,
    177, 180, 181, 189, 191, 199
]

# 对每个元素执行操作
for i in array:
    # 读取文件内容
    try:
        with open('phone_location.sql', 'r', encoding='UTF-8') as file:
            content = file.read()

        # 使用 grep 和 awk 的功能
        grep_result = [line for line in content.split('\n') if f"'{i}'" in line]
        awk_result = [line.split()[7] for line in grep_result]

        # 排序、去重计数并输出出现次数最多的结果
        count_result = Counter(awk_result)
        most_common = count_result.most_common(1)

        if most_common:
            print(f"{most_common[0][1]} {most_common[0][0]}")
        else:
            print("No matches found")

    except FileNotFoundError:
        print("File not found: ./phone_location.sql")
