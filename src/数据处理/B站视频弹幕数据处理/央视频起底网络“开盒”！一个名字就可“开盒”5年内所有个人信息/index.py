import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# 读取CSV文件中的弹幕数据
file_path = "BV1wbpRzaEhz_danmu.csv"
df = pd.read_csv(file_path, encoding="utf-8-sig")

# 显示所有弹幕数据的基本信息
print("弹幕数据基本信息:")
print(f"总弹幕数量: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")

# 提取所有弹幕内容
contents = df['content'].astype(str).tolist()

# 合并所有弹幕为一个大文本
all_text = ' '.join(contents)

# 使用jieba进行中文分词
words = jieba.lcut(all_text)

# 过滤掉单字符和无意义的词
stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]

# 统计词频
word_freq = Counter(filtered_words)

# 显示高频词
print("\n高频词汇 Top 20:")
for word, freq in word_freq.most_common(20):
    print(f"{word}: {freq}")

# 生成词云
# 需要指定中文字体路径，如果没有默认字体可能无法显示中文
wordcloud = WordCloud(
    width=800,
    height=600,
    background_color='white',
    font_path='simhei.ttf',  # Windows系统黑体
    max_words=200,
    relative_scaling=0.5,
    random_state=42
).generate_from_frequencies(word_freq)

# 显示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('弹幕词云图')
plt.show()

# 保存词云图
plt.savefig('danmu_wordcloud.png', dpi=300, bbox_inches='tight')
print("\n词云图已保存为 danmu_wordcloud.png")
