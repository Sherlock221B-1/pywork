import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体
matplotlib.rc("font", family="SimHei")  # 使用中文字体 SimHei
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 读取数据
file_path = r"C:\Users\Lenovo\Desktop\221549241袁烨python\Bike_data.csv"
df = pd.read_csv(file_path)

# 2. 数据预处理
# 将时间戳转换为日期时间格式
df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])

# 筛选需求数据：车辆状态为0时，表示单车正在被骑行，代表需求发生的地点
df_demand = df[df['LOCK_STATUS'] == 0].copy()  # 使用 .copy() 创建子数据框的副本

# 提取骑行的经纬度数据
coordinates = df_demand[['LATITUDE', 'LONGITUDE']].values

# 3. 创建热力图
# 上海的经纬度范围
south_lat = 30.6500
north_lat = 31.3000
west_lon = 120.8500
east_lon = 122.1000

# 创建 Folium 地图，设置初始视角为上海，并使用 OpenStreetMap
bike_map = folium.Map(location=[(north_lat + south_lat) / 2, (west_lon + east_lon) / 2],
                      zoom_start=11,
                      tiles='OpenStreetMap')  # 使用 OpenStreetMap 作为底图

# 添加热力图层，设置透明度参数
HeatMap(
    coordinates,
    radius=15,
    blur=10,
    max_zoom=1,
    opacity=0.9  # 设置透明度为 0.6
).add_to(bike_map)

# 保存地图为HTML文件
bike_map.save("bike_demand_heatmap.html")
print("\n热力图已保存为 'bike_demand_heatmap.html'，请在浏览器中查看。")

# 4. 时间段需求分析
# 按小时提取需求数据
df_demand['hour'] = df_demand['DATA_TIME'].dt.hour  # 直接操作副本，不会触发警告
hourly_demand = df_demand.groupby('hour').size()

# 绘制柱状图展示每小时的需求量
plt.figure(figsize=(10, 6))
hourly_demand.plot(kind='bar', color='skyblue')
plt.title('共享单车需求量（每小时）')
plt.xlabel('小时')
plt.ylabel('需求量')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("hourly_demand.png")  # 保存为图片
plt.show()

print("\n每小时的需求量：")
print(hourly_demand)

# 识别需求量最高的时段
peak_hour = hourly_demand.idxmax()
print(f"\n需求量最高的时段是 {peak_hour} 点，需求量为 {hourly_demand.max()} 次。")



