import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import numpy as np

# 读取CSV文件中的弹幕数据
file_path = "BV1wbpRzaEhz_danmu.csv"
df = pd.read_csv(file_path, encoding="utf-8-sig")

# 数据清洗和预处理
df['send_time'] = pd.to_datetime(df['send_time'], unit='s')
df['content'] = df['content'].astype(str)

# 显示所有弹幕数据的基本信息
print("弹幕数据基本信息:")
print(f"总弹幕数量: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")

# 1. 时间分布图
plt.figure(figsize=(12, 8))

# 创建子图
plt.subplot(2, 2, 1)
df['hour'] = df['send_time'].dt.hour
hourly_counts = df['hour'].value_counts().sort_index()
plt.bar(hourly_counts.index, hourly_counts.values, color='skyblue')
plt.xlabel('小时')
plt.ylabel('弹幕数量')
plt.title('弹幕时间分布（按小时）')
plt.xticks(range(0, 24))

# 2. 词云图
plt.subplot(2, 2, 2)
# 提取所有弹幕内容
contents = df['content'].tolist()

# 合并所有弹幕为一个大文本
all_text = ' '.join(contents)

# 使用jieba进行中文分词
words = list(jieba.cut(all_text))

# 过滤掉单字符和无意义的词
stopwords = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '个', '那', '被', '被开', '开盒', '信息', '可以', '什么', '我们',
    '他们', '就是', '还是', '应该', '因为', '所以', '然后', '但是', '这个', '那个',
    '还有', '已经', '现在', '时候', '可能', '不能', '不要', '开始', '出来', '出来',
    '一下', '一些', '一样', '一直', '一起', '一点', '一定', '一种', '一直', '一种'
}
filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]

# 统计词频
word_freq = Counter(filtered_words)

# 显示高频词
print("\n高频词汇 Top 20:")
for word, freq in word_freq.most_common(20):
    print(f"{word}: {freq}")

# 生成词云
try:
    wordcloud = WordCloud(
        width=400,
        height=300,
        background_color='white',
        font_path='simhei.ttf',  # Windows系统黑体
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(word_freq)
except OSError:
    # 如果找不到指定字体，使用默认设置
    wordcloud = WordCloud(
        width=400,
        height=300,
        background_color='white',
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(word_freq)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('弹幕词云图')

# 3. 关键词统计图
plt.subplot(2, 2, 3)
# 定义关键词
keywords = ['开盒', '个人信息', '电报', '缓刑', '犯罪', '法律', '处罚', '网络', '平台', '主播']
keyword_counts = {}

for keyword in keywords:
    keyword_counts[keyword] = df['content'].str.contains(keyword, na=False).sum()

# 绘制关键词统计图
plt.barh(list(keyword_counts.keys()), list(keyword_counts.values()), color='lightcoral')
plt.xlabel('出现次数')
plt.title('关键词统计')

# 4. 弹幕长度分布
plt.subplot(2, 2, 4)
df['content_length'] = df['content'].apply(len)
length_counts = df['content_length'].value_counts().sort_index()
plt.hist(df['content_length'], bins=30, color='lightgreen', edgecolor='black')
plt.xlabel('弹幕长度（字符数）')
plt.ylabel('弹幕数量')
plt.title('弹幕长度分布')

# 调整布局
plt.tight_layout()
plt.show()

# 保存图表
plt.savefig('danmu_analysis.png', dpi=300, bbox_inches='tight')
print("\n分析图表已保存为 danmu_analysis.png")

# 输出一些统计信息
print(f"\n弹幕统计信息:")
print(f"平均每条弹幕长度: {df['content_length'].mean():.2f} 字符")
print(f"最长弹幕: {df['content_length'].max()} 字符")
print(f"最短弹幕: {df['content_length'].min()} 字符")

# 输出时间分布信息
print(f"\n时间分布信息:")
print(f"最早弹幕: {df['send_time'].min()}")
print(f"最晚弹幕: {df['send_time'].max()}")
