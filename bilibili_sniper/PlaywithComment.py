import pandas as pd
from pyecharts.charts import Scatter
from pyecharts.options import TitleOpts, TooltipOpts, ToolboxOpts, VisualMapOpts, AxisOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.dropna(subset=['播放数', '评论数'])

# 筛掉异常值（播放数过大或评论数为NaN）
df = df[(df['播放数'] > 0) & (df['评论数'] > 0)]

# 准备数据
data = list(zip(df['播放数'].astype(int), df['评论数'].astype(int)))

# 散点图
scatter = (
    Scatter(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis([x for x, y in data])
    .add_yaxis("视频", [y for x, y in data])
    .set_global_opts(
        title_opts=TitleOpts(title="播放数与评论数的关系"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="item", formatter="播放: {@[0]}<br/>评论: {@[1]}"),
        xaxis_opts=AxisOpts(name="播放数", type_="value"),
        yaxis_opts=AxisOpts(name="评论数", type_="value"),
        visualmap_opts=VisualMapOpts(type_="size", max_=max(df['评论数']), min_=min(df['评论数']), dimension=1)
    )
)

scatter.render("step5_播放与评论关系图.html")
print("step5_播放与评论关系图.html 已生成")