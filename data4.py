import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 1. 配置相应地图库
# 假设数据已加载到 DataFrame
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\221549241袁烨python\Bike_data.csv")

# 将数据时间转换为 datetime 类型
df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])

# 2. 统计每辆共享单车当日每次停车时间段及当时位置
# 添加一列 'hour' 来提取小时信息
df['hour'] = df['DATA_TIME'].dt.hour

# 以每个单车的 'id' 和时间进行排序，确保每次停车记录是按时间顺序排列的
df = df.sort_values(by=['id', 'DATA_TIME'])

# 假设数据中已经包含 'LAT' 和 'LON' 列，分别表示停车位置的经纬度
# 计算停车记录：对于同一辆车，如果位置相同并且停车时长大于一段时间，则认为它是停放的状态
# 假设 'LOCK_STATUS' = 1 为停放状态

# 标记停放状态
df['is_parking'] = df['LOCK_STATUS'] == 1

# 对每个单车的停车记录按时间段分类
df['parking_time_slot'] = None  # 添加停车时间段列
df.loc[df['hour'].between(7, 9), 'parking_time_slot'] = 'morning_peak'
df.loc[df['hour'].between(17, 19), 'parking_time_slot'] = 'evening_peak'

# 3. 将停车记录与高峰期时间段进行比较，符合条件则取该条记录停车位置显示在地图上

# 筛选早高峰和晚高峰数据
peak_df = df[df['parking_time_slot'].isin(['morning_peak', 'evening_peak'])]

# 上海的经纬度范围
south_lat = 30.6500
north_lat = 31.3000
west_lon = 120.8500
east_lon = 122.1000

# 创建 Folium 地图，设置初始视角为上海，并使用 OpenStreetMap
m = folium.Map(location=[(north_lat + south_lat) / 2, (west_lon + east_lon) / 2],
               zoom_start=11,
               tiles='OpenStreetMap')  # 使用 OpenStreetMap 作为底图

# 可以通过添加其他图层来进一步自定义地图

# 创建 MarkerCluster 用于聚合标记
marker_cluster = MarkerCluster().add_to(m)

# 在地图上添加停车位置的标记
for _, row in peak_df.iterrows():
    # 提取停车记录的经纬度
    lat, lon = row['LATITUDE'], row['LONGITUDE']
    time_slot = row['parking_time_slot']

    # 根据停车时间段选择不同的标记颜色
    icon_color = 'blue' if time_slot == 'morning_peak' else 'red'

    folium.Marker(
        location=[lat, lon],
        popup=f"停车时间段: {time_slot}<br>时间: {row['DATA_TIME']}",
        icon=folium.Icon(color=icon_color)
    ).add_to(marker_cluster)

# 显示地图
m.save('bike_peak_parking_distribution_shanghai.html')
