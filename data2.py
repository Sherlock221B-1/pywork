import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from geopy.distance import geodesic


# 假设数据已加载到 DataFrame
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\221549241袁烨python\Bike_data.csv" )

# 将数据时间转换为 datetime 类型
df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])

# 假设数据中有经纬度信息
# 计算每两个连续记录的地理距离（以公里为单位）
def calculate_distance(row1, row2):
    coords_1 = (row1['LATITUDE'], row1['LONGITUDE'])
    coords_2 = (row2['LATITUDE'], row2['LONGITUDE'])
    return geodesic(coords_1, coords_2).km

# 计算每个订单的里程，假设每条记录属于同一订单的连续位置点
df['distance'] = df.apply(lambda row: calculate_distance(df.iloc[row.name - 1], row) if row.name > 0 else 0, axis=1)

# 删除无效值
df = df.dropna(subset=['distance'])

# 将里程数据分组（例如：0-1公里，1-2公里等）
bins = [0, 1, 2, 3, 5, 10, 20, 50]
labels = ['0-1 km', '1-2 km', '2-3 km', '3-5 km', '5-10 km', '10-20 km', '20+ km']

df['distance_range'] = pd.cut(df['distance'], bins=bins, labels=labels, right=False)

# 统计各个里程区间的订单数量
distance_counts = df['distance_range'].value_counts().sort_index()

# 使用 pyecharts 绘制柱状图
bar = (
    Bar()
    .add_xaxis(distance_counts.index.tolist())
    .add_yaxis("订单数量", distance_counts.tolist(), color="skyblue")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="订单里程分布图"),
        xaxis_opts=opts.AxisOpts(name="里程范围（公里）"),
        yaxis_opts=opts.AxisOpts(name="订单数量")
    )
)

# 渲染图表到 HTML 文件
bar.render("order_distance_distribution.html")