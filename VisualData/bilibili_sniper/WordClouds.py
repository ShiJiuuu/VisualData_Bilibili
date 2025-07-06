import pandas as pd
import jieba
from collections import Counter
from pyecharts.charts import WordCloud
from pyecharts.options import TitleOpts, TooltipOpts

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.dropna(subset=['标题'])

# 提取所有标题
titles = df['标题'].astype(str).tolist()

# 中文分词
all_words = []
for title in titles:
    words = jieba.lcut(title)
    all_words.extend(words)

# 常见停用词列表（可以根据需要扩充）
stopwords = set(['的', '了', '是', '我们', '你', '我', '他', '她', '也', '都', '很', '就', '在', '和', '一个', '上', '下', '啊'])

# 统计词频
words_filtered = [w for w in all_words if w.strip() and w not in stopwords and len(w) > 1]
counter = Counter(words_filtered)
top_words = counter.most_common(100)

# 构建词云
wc = (
    WordCloud()
    .add(series_name="关键词", data_pair=top_words, word_size_range=[15, 100])
    .set_global_opts(
        title_opts=TitleOpts(title="视频标题词云"),
        tooltip_opts=TooltipOpts(is_show=True)
    )
)

wc.render("step6_视频标题词云.html")
print("step6_视频标题词云.html 已生成")