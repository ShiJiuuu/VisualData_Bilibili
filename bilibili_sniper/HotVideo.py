import pandas as pd
import numpy as np
from pyecharts.charts import Bar
from pyecharts.options import TitleOpts, ToolboxOpts, TooltipOpts, AxisOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_data_with_category.csv")
df = df.drop_duplicates(subset='BV号')
df = df.replace([np.inf, -np.inf], pd.NA)
df = df.dropna(subset=['播放数', 'category'])

# 原始顺序手动指定（避免打乱）
type_order = ["动画", "音乐", "游戏", "生活", "知识", "Vlog", "娱乐", "鬼畜", "科普", "电影", "纪录片", "舞蹈"]

# 分区平均播放量
avg_views = df.groupby("category")["播放数"].mean().reindex(type_order)

# 清除没出现的分区
avg_views = avg_views.dropna()

# 绘图
bar = (
    Bar(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(avg_views.index.tolist())
    .add_yaxis("平均播放量", avg_views.round(0).astype(int).tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="不同视频类型的平均播放量"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="视频类型", axislabel_opts={"rotate": 30}),
        yaxis_opts=AxisOpts(name="平均播放数")
    )
)

bar.render("step2_视频类型热度分析.html")
print("step2_视频类型热度分析.html 已生成")