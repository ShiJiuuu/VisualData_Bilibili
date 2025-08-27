import pandas as pd
from pyecharts.charts import Scatter
from pyecharts.options import TitleOpts, TooltipOpts, ToolboxOpts, VisualMapOpts, AxisOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.dropna(subset=['播放数', '时长'])

# 时长单位换算（有些平台返回为 xx:yy 格式，要先转化）
def parse_duration(s):
    try:
        if isinstance(s, str) and ':' in s:
            parts = list(map(int, s.split(':')))
            return parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0]
        else:
            return float(s)
    except:
        return None

df['时长_sec'] = df['时长'].apply(parse_duration)
df = df.dropna(subset=['时长_sec'])

# 筛选极端值（例如播放数 > 0 且视频时长合理）
df = df[(df['播放数'] > 0) & (df['时长_sec'] > 0) & (df['时长_sec'] < 7200)]  # 小于2小时
df = df.sort_values(by='时长_sec')

# 构建数据
data = list(zip(df['时长_sec'].astype(int), df['播放数'].astype(int)))

# 生成散点图
scatter = (
    Scatter(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis([x for x, y in data])
    .add_yaxis("视频", [y for x, y in data])
    .set_global_opts(
        title_opts=TitleOpts(title="视频时长与播放量的关系"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="item", formatter="时长: {@[0]}秒<br/>播放: {@[1]}"),
        xaxis_opts=AxisOpts(name="视频时长（秒）"),
        yaxis_opts=AxisOpts(name="播放量"),
        visualmap_opts=VisualMapOpts(type_="size", dimension=1,
                                     max_=max(df['播放数']),
                                     min_=min(df['播放数']))
    )
)

scatter.render("step7_时长与播放关系.html")
print("step7_时长与播放关系.html 已生成")