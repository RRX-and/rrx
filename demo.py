import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


# 加载数据
def load_data():
    california_data = pd.read_excel('Disneyland_California.xlsx')
    hongkong_data = pd.read_excel('Disneyland_HongKong.xlsx')
    paris_data = pd.read_excel('Disneyland_Paris.xlsx')
    reviews_data = pd.read_excel('Sampled_DisneylandReviews.xlsx')
    return {'California': california_data, 'HongKong': hongkong_data, 'Paris': paris_data}, reviews_data


data, reviews_data = load_data()

# Streamlit 页面布局
st.title("Disneyland 评价分析")

st.image('pic.png')

# 用户选择
region = st.selectbox("选择园区", ["California", "HongKong", "Paris"])
month = st.selectbox("选择月份", data[region]['Month'].unique())

# 获取选择地区的数据
region_data = data[region]

# 绘制好评率和差评率曲线
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# 好评率和差评率曲线
ax[0].plot(region_data['Month'], region_data['positive_rate'], label='好评率', marker='o')
ax[0].plot(region_data['Month'], region_data['negative_rate'], label='差评率', marker='o')
ax[0].set_xlabel('月份')
ax[0].set_ylabel('百分比')
ax[0].set_title(f'{region}园区 评价曲线')
ax[0].legend()

# 选择月份的评价分布饼图
month_data = region_data[region_data['Month'] == month].iloc[0]
labels = '正面评价', '负面评价', '中立评价'
sizes = [month_data['positive'], month_data['negative'], month_data['neutral']]
colors = ['#ff9999','#66b3ff','#99ff99']
explode = (0.1, 0, 0)

ax[1].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax[1].axis('equal')
ax[1].set_title(f'{month} 月份评价分布')

# 在 Streamlit 页面中显示图表
st.pyplot(fig)

# 显示随机评论
st.subheader("随机抽取的评论")

# 筛选评论数据
filtered_reviews = reviews_data[(reviews_data['Branch'] == 'Disneyland_' + region) & (reviews_data['Month'] == month)]
random_reviews = filtered_reviews.sample(min(10, len(filtered_reviews)), random_state=42)

# 显示评论
for i, review in enumerate(random_reviews['Review_Text'].tolist()):
    st.write(f"{i+1}. {review}")
