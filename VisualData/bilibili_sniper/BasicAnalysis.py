import pandas as pd
import numpy as np
from pyecharts.charts import Bar, Boxplot, Timeline, Line, Page
from pyecharts.options import TitleOpts, ToolboxOpts, LegendOpts, TooltipOpts, AxisOpts, VisualMapOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=['播放数', '评论数', '弹幕数', '发布时间'])

# 转换时间戳
df['发布时间_dt'] = pd.to_datetime(df['发布时间'], unit='s', errors='coerce')
df = df.dropna(subset=['发布时间_dt'])

# 播放数分布柱状图（分组）
bins = [0, 1000, 10000, 100000, 1000000, 10000000, 1e9]
labels = ['<1K', '1K-10K', '10K-100K', '100K-1M', '1M-10M', '10M+']
df['播放数区间'] = pd.cut(df['播放数'], bins=bins, labels=labels)
view_count_bar = (
    Bar(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(labels)
    .add_yaxis("视频数", df['播放数区间'].value_counts().reindex(labels).fillna(0).astype(int).tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="播放数分布"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="播放数区间"),
        yaxis_opts=AxisOpts(name="视频数量")
    )
)

# 评论数分布（同上）
bins2 = [0, 10, 100, 1000, 5000, 10000, 1e6]
labels2 = ['<10', '10-100', '100-1K', '1K-5K', '5K-10K', '10K+']
df['评论数区间'] = pd.cut(df['评论数'], bins=bins2, labels=labels2)
comment_bar = (
    Bar(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(labels2)
    .add_yaxis("视频数", df['评论数区间'].value_counts().reindex(labels2).fillna(0).astype(int).tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="评论数分布"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="评论数区间"),
        yaxis_opts=AxisOpts(name="视频数量")
    )
)

# 播放/评论/弹幕的箱型图
box_data = df[['播放数', '评论数', '弹幕数']].values.T.tolist()
boxplot = Boxplot()
boxplot.add_xaxis(["播放数", "评论数", "弹幕数"])
boxplot.add_yaxis("分布", boxplot.prepare_data(box_data))
boxplot.set_global_opts(title_opts=TitleOpts(title="播放数/评论数/弹幕数 箱型图"))

# 发布时间分布（Line图）
df['日期'] = df['发布时间_dt'].dt.date
date_stats = df.groupby('日期').size().sort_index()
pub_line = (
    Line()
    .add_xaxis(date_stats.index.astype(str).tolist())
    .add_yaxis("视频发布数量", date_stats.tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="视频发布时间趋势"),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="日期"),
        yaxis_opts=AxisOpts(name="发布数量"),
        datazoom_opts={"type": "slider"}
    )
)

# 汇总页面
page = Page(layout=Page.SimplePageLayout)
page.add(view_count_bar, comment_bar, boxplot, pub_line)
page.render("step1_基础分析.html")
print("已生成 step1_基础分析.html")