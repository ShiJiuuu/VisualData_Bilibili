import pandas as pd
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, ToolboxOpts, TooltipOpts, AxisOpts, DataZoomOpts
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("combined_all.csv")
df = df.drop_duplicates(subset='BV号')
df = df.dropna(subset=['发布时间'])

# 时间戳转换为日期
df['发布时间_dt'] = pd.to_datetime(df['发布时间'], unit='s', errors='coerce')
df = df.dropna(subset=['发布时间_dt'])

# 按天统计视频数量
df['日期'] = df['发布时间_dt'].dt.date
date_count = df.groupby('日期').size().sort_index()

# 构造折线图
line = (
    Line(init_opts={"theme": ThemeType.LIGHT})
    .add_xaxis(date_count.index.astype(str).tolist())
    .add_yaxis("视频数", date_count.tolist())
    .set_global_opts(
        title_opts=TitleOpts(title="视频上传数量时间趋势（按日）"),
        toolbox_opts=ToolboxOpts(),
        tooltip_opts=TooltipOpts(trigger="axis"),
        xaxis_opts=AxisOpts(name="日期", axislabel_opts={"rotate": 45}),
        yaxis_opts=AxisOpts(name="上传数量"),
        datazoom_opts=[DataZoomOpts(type_="slider")]
    )
)

line.render("step4_时间趋势.html")
print("step4_时间趋势.html 已生成")