import pandas as pd
from pyecharts.charts import Bar
from pyecharts.options import TitleOpts, ToolboxOpts, TooltipOpts, AxisOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.replace([float('inf'), -float('inf')], pd.NA)
df = df.dropna(subset=['播放数', '标题'])

# 获取播放量Top 20
top_videos = df.sort_values(by="播放数", ascending=False).head(20)

# 横坐标：视频标题（截断避免太长）
titles = [title if len(title) < 20 else title[:17] + '...' for title in top_videos['标题']]
views = top_videos['播放数'].astype(int).tolist()

# 构建柱状图
bar = (
    Bar(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(titles)
    .add_yaxis("播放数", views)
    .set_global_opts(
        title_opts=TitleOpts(title="播放量排行榜 Top 20"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(axislabel_opts={"rotate": 45}, name="视频标题"),
        yaxis_opts=AxisOpts(name="播放数")
    )
)

bar.render("step3_播放排行榜.html")
print("step3_播放排行榜.html 已生成")