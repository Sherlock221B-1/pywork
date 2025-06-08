## 概述：
这个仓库包含一组Python脚本，用于分析共享单车使用数据，包括骑行时长分布、里程分布、时间趋势分析、高峰期停车位置分布以及骑行需求热力图等。


# 环境配置：
依赖安装
pip install pandas matplotlib pyecharts geopy folium
或使用国内镜像源加速安装
pip install -i https://mirrors.aliyun.com/pypi/simple/ pandas matplotlib pyecharts geopy folium
文件说明
文件名	功能描述	输出文件
data1.py	订单时长分布分析	显示Matplotlib图表
data2.py	订单里程分布分析	order_distance_distribution.html
data3.py	每日订单时间趋势分析	显示Matplotlib图表
data4.py	高峰期停车位置分布地图	bike_peak_parking_distribution_shanghai.html
data5.py	骑行需求热力图与时间分析	bike_demand_heatmap.html 和 hourly_demand.png


# 使用说明：
将共享单车数据文件命名为 Bike_data.csv 放在项目目录
运行所需分析脚本：
订单时长分析
python data1.py

订单里程分析
python data2.py

每日订单时间趋势分析
python data3.py

高峰期停车位置分布
python data4.py

骑行需求热力图分析
python data5.py
