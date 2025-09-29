import pandas as pd

# 读取CSV文件中的弹幕数据
file_path = "BV1wbpRzaEhz_danmu.csv"
df = pd.read_csv(file_path, encoding="utf-8-sig")

# 显示所有弹幕数据的基本信息
print("弹幕数据基本信息:")
print(f"总弹幕数量: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")
print("\n数据类型:")
print(df.dtypes)

# 显示所有弹幕内容
print("\n\n所有弹幕内容:")
for index, row in df.iterrows():
    print(f"第{index+1}条弹幕: {row['content']}")

# 或者如果您只想查看所有弹幕内容而不带序号:
print("\n\n所有弹幕内容(纯文本):")
for content in df['content']:
    print(content)
