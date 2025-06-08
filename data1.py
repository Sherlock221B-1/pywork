import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 设置字体为支持中文的字体，避免出现字体缺失问题
plt.rcParams['font.family'] = 'Microsoft YaHei'  # 适用于Windows系统

# 数据已加载到DataFrame
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\221549241袁烨python\Bike_data.csv ')

# 将数据时间转换为 datetime 类型
df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])

# 这里假设每条记录代表一次停车操作，我们计算停车时长（单位：分钟）
df['time_duration'] = df.groupby('id')['DATA_TIME'].diff().shift(-1).dt.total_seconds() / 60  # 转换为分钟

# 删除空值
df = df.dropna(subset=['time_duration'])

# 设定时长区间
bins = [0, 5, 10, 15, 20, 30, 60, 120, 180, 240, 300]  # 这里可以自定义时长范围
labels = ['0-5', '5-10', '10-15', '15-20', '20-30', '30-60', '60-120', '120-180', '180-240', '240+']

# 将时长分组
df['time_range'] = pd.cut(df['time_duration'], bins=bins, labels=labels, right=False)

# 统计各个时长范围的订单数量
order_counts = df['time_range'].value_counts().sort_index()

# 绘制柱状图
plt.figure(figsize=(10, 6))
order_counts.plot(kind='bar', color='skyblue', edgecolor='black')

# 设置图表标题和标签
plt.title('订单时长分布图', fontsize=16)
plt.xlabel('时长范围（分钟）', fontsize=12)
plt.ylabel('订单数量', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# 显示图表
plt.show()

