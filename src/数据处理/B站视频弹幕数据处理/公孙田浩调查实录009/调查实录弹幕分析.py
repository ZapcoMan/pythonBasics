import logging
from collections import Counter

import jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# 减少jieba日志输出
jieba.setLogLevel(logging.INFO)
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取CSV文件中的弹幕数据
file_path = "公孙田浩弹幕_BV19R4y1K7yc_danmu.csv"
df = pd.read_csv(file_path, encoding="utf-8-sig")

# 数据清洗和预处理
df['send_time'] = pd.to_datetime(df['send_time'], unit='s')
df['content'] = df['content'].astype(str)

# 显示所有弹幕数据的基本信息
print("弹幕数据基本信息:")
print(f"总弹幕数量: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")

# 提取所有弹幕内容
contents = df['content'].tolist()
all_text = ' '.join(contents)

# 使用jieba进行中文分词
words = list(jieba.cut(all_text))

# 过滤掉单字符和无意义的词 (使用和之前一致的停用词)
stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]

# 统计词频
word_freq = Counter(filtered_words)

# 显示高频词 (恢复到Top 30)
print("\n高频词汇 Top 30:")
for word, freq in word_freq.most_common(30):
    print(f"{word}: {freq}")

# 1. 时间分布图
plt.figure(figsize=(10, 6))
df['hour'] = df['send_time'].dt.hour
hourly_counts = df['hour'].value_counts().sort_index()
plt.bar(hourly_counts.index, hourly_counts.values, color='skyblue')
plt.xlabel('小时')
plt.ylabel('弹幕数量')
plt.title('弹幕时间分布（按小时）')
plt.xticks(range(0, 24))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('danmu_time_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n时间分布图已保存为 danmu_time_distribution.png")

# 2. 词云图 (使用相同的词频数据)
plt.figure(figsize=(10, 8))
try:
    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color='white',
        font_path='simhei.ttf',  # Windows系统黑体
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(word_freq)
except OSError:
    # 如果找不到指定字体，使用默认设置
    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color='white',
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(word_freq)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('弹幕词云图')
plt.tight_layout()
plt.savefig('danmu_wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n词云图已保存为 danmu_wordcloud.png")

# 3. 关键词统计图
plt.figure(figsize=(10, 6))
# 定义关键词
keywords = ['开盒', '个人信息', '电报', '缓刑', '犯罪', '法律', '处罚', '网络', '平台', '主播']
keyword_counts = {}

for keyword in keywords:
    keyword_counts[keyword] = df['content'].str.contains(keyword, na=False).sum()

# 绘制关键词统计图
bars = plt.bar(keywords, list(keyword_counts.values()), color='lightcoral')
plt.xlabel('关键词')
plt.ylabel('出现次数')
plt.title('关键词统计')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

# 在柱状图上添加数值标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('danmu_keyword_statistics.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n关键词统计图已保存为 danmu_keyword_statistics.png")

# 4. 弹幕长度分布
plt.figure(figsize=(10, 6))
df['content_length'] = df['content'].apply(len)
plt.hist(df['content_length'], bins=30, color='lightgreen', edgecolor='black')
plt.xlabel('弹幕长度（字符数）')
plt.ylabel('弹幕数量')
plt.title('弹幕长度分布')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('danmu_length_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print("\n弹幕长度分布图已保存为 danmu_length_distribution.png")

# 输出统计信息
print(f"\n弹幕统计信息:")
print(f"平均每条弹幕长度: {df['content_length'].mean():.2f} 字符")
print(f"最长弹幕: {df['content_length'].max()} 字符")
print(f"最短弹幕: {df['content_length'].min()} 字符")

# 输出时间分布信息
print(f"\n时间分布信息:")
print(f"最早弹幕: {df['send_time'].min()}")
print(f"最晚弹幕: {df['send_time'].max()}")
