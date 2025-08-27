import pandas as pd
from pyecharts.charts import Bar
from pyecharts.options import TitleOpts, ToolboxOpts, TooltipOpts, AxisOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.dropna(subset=['播放数', '时长'])

# 处理时长
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
df = df[(df['播放数'] > 0) & (df['时长_sec'] > 0) & (df['时长_sec'] < 7200)]

# 定义时长区间
def get_duration_range(sec):
    if sec <= 60:
        return "超短视频"
    elif sec <= 300:
        return "短视频"
    elif sec <= 900:
        return "中视频"
    elif sec <= 1800:
        return "长视频"
    else:
        return "超长视频"

df['时长区间'] = df['时长_sec'].apply(get_duration_range)

# 计算每个区间的平均播放数
avg_play = df.groupby('时长区间')['播放数'].mean().reindex(['超短视频', '短视频', '中视频', '长视频', '超长视频'])

# 构建柱状图
bar = (
    Bar(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(avg_play.index.tolist())
    .add_yaxis("平均播放量", avg_play.values.round(2).tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="不同时长区间的平均播放量"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="时长区间"),
        yaxis_opts=AxisOpts(name="平均播放数")
    )
)

bar.render("step8_时长区间平均播放量.html")
print("step8_时长区间平均播放量.html 已生成")