import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置字体为支持中文的字体
rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei' 是常见的支持中文的字体
rcParams['axes.unicode_minus'] = False  # 显示负号

# 假设数据已加载到 DataFrame
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\221549241袁烨python\Bike_data.csv")

# 将数据时间转换为 datetime 类型
df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])

# 筛选出当天的数据 (例如 2018年8月27日)
df['date'] = df['DATA_TIME'].dt.date

# 使用 .copy() 创建副本，避免修改视图
df_day = df[df['date'] == pd.to_datetime('2018-08-27').date()].copy()

# 使用 .loc 显式地修改列，提取小时信息
df_day.loc[:, 'hour'] = df_day['DATA_TIME'].dt.hour

# 按小时分组，计算每小时的订单数量
order_counts_per_hour = df_day.groupby('hour').size()

# 绘制订单趋势图（按小时）
plt.figure(figsize=(10, 6))
order_counts_per_hour.plot(kind='line', marker='o', color='skyblue')

# 设置图表标题和标签
plt.title('2018年8月27日 订单趋势（随时间变化）', fontsize=16)
plt.xlabel('小时', fontsize=12)
plt.ylabel('订单数量', fontsize=12)

# 设置x轴显示每小时
plt.xticks(range(0, 24))  # 显示每小时

# 美化图表布局，避免标签重叠
plt.xticks(rotation=45)  # x轴标签旋转45度以避免重叠
plt.grid(True)
plt.tight_layout()  # 自动调整布局

# 显示图表
plt.show()



