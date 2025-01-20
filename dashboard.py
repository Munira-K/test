import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etl import get_data

st.title('Разведочный дашборд по базе супермаркета :grinning:')

supermarket = get_data('data')
supermarket['DayOfWeek'] = supermarket['ReceiptDate'].dt.weekday + 1
supermarket

date_data = (
    supermarket.groupby('ReceiptDate')
    .agg(
        day_of_week=('DayOfWeek', 'first'),
        check_count=('ReceiptNumber', 'nunique'),
        total_sum=('Amount', 'sum'),
        total_quantity=('Quantity', 'sum')
    ).reset_index()
)

by_weekday = (date_data.groupby('day_of_week')
    .agg(total_check_count=('check_count', 'sum'), total_quantity=('total_quantity', 'sum'))
    .reset_index())


fig, axes = plt.subplots(2, 3, figsize=(15, 8))

sns.lineplot(data=date_data, x='ReceiptDate', y='total_sum', ax=axes[0, 0])
axes[0, 0].set_title('Суммы продаж по датам', fontsize=14)
axes[0, 0].set_xlabel('Дата')
axes[0, 0].set_ylabel('Сумма')

sns.lineplot(data=date_data, x='ReceiptDate', y='check_count', ax=axes[0, 1])
axes[0, 1].set_title('Количество чеков по датам', fontsize=14)
axes[0, 1].set_xlabel('Дата')
axes[0, 1].set_ylabel('Количество чеков')

sns.lineplot(data=date_data, x='ReceiptDate', y='total_quantity', ax=axes[0, 2])
axes[0, 2].set_title('Количество товаров по датам', fontsize=14)
axes[0, 2].set_xlabel('Дата')
axes[0, 2].set_ylabel('Количество товаров')

sns.barplot(data=date_data, x='day_of_week', y='total_sum', ax=axes[1, 0], palette="coolwarm")
axes[1, 0].set_title('Суммы продаж по дням недели', fontsize=14)
axes[1, 0].set_xlabel('День недели')
axes[1, 0].set_ylabel('Сумма')

sns.barplot(data=by_weekday, x='day_of_week', y='total_check_count', ax=axes[1, 1], palette="coolwarm")
axes[1, 1].set_title('Количество чеков по дням недели', fontsize=14)
axes[1, 1].set_xlabel('День недели')
axes[1, 1].set_ylabel('Количество чеков')

sns.barplot(data=by_weekday, x='day_of_week', y='total_quantity', ax=axes[1, 2], palette="coolwarm")
axes[1, 2].set_title('Количество товаров по дням недели', fontsize=14)
axes[1, 2].set_xlabel('День недели')
axes[1, 2].set_ylabel('Количество товаров')

plt.tight_layout()
st.pyplot(plt)

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'


st.write("**Доля количества чеков по сезонам**")
date_data['season'] = date_data['ReceiptDate'].apply(get_season)
season_analysis = (
    date_data.groupby('season')
    .agg(total_check_count=('check_count', 'sum')) 
    .reset_index()
)
plt.figure(figsize=(2, 3))
plt.pie(season_analysis['total_check_count'], labels=season_analysis['season'], autopct='%1.1f%%')
st.pyplot(plt)


first = date_data.head(30)
last = date_data.tail(30)

fig, axes = plt.subplots(2, 1, figsize=(15, 6))
sns.lineplot(data=first, x='ReceiptDate', y='check_count', ax=axes[0], color='blue')
axes[0].set_title('Количество чеков за январь 2024', fontsize=14)
axes[0].set_ylabel('Количество чеков')

sns.lineplot(data=last, x='ReceiptDate', y='check_count', ax=axes[1], color='orange')
axes[1].set_title('Количество чеков за декабрь 2024', fontsize=14)
axes[1].set_ylabel('Количество чеков')

plt.tight_layout()
st.pyplot(plt)

first = date_data.head(7)
last = date_data.tail(7)
fig, axes =  plt.subplots(2, 1, figsize=(15, 6))
sns.lineplot(data=first, x='ReceiptDate', y='check_count', ax=axes[0], marker='o', color='blue')
axes[0].set_title('Количество чеков по первым 10 дням)', fontsize=14)
axes[0].set_ylabel('Количество чеков')

sns.lineplot(data=last, x='ReceiptDate', y='check_count', ax=axes[1], marker='o', color='orange')
axes[1].set_title('Количество чеков последним 10 дням', fontsize=14)
axes[1].set_ylabel('Количество чеков')

plt.tight_layout()
st.pyplot(plt)

item_data = (supermarket.groupby('Item').agg(
        item_count=('Item', 'count'), 
        total_amount=('Amount', 'sum'),
        avg_price_per_unit=('Amount', lambda x: x.sum() / supermarket.loc[x.index, 'Quantity'].sum())).reset_index())

item_data['total_amount'] = item_data['total_amount'].round()
item_data['avg_price_per_unit'] = item_data['avg_price_per_unit'].round(2)

item_data['total_%'] =  item_data['total_amount']/item_data['total_amount'].sum()*100
item_data['total_%'] = item_data['total_%'].round(1)

item_data = item_data.sort_values(by=['item_count',  'avg_price_per_unit', 'total_amount'], ascending=False).head(5)

st.write("**Количество проданных товаров по продуктам**")
plt.figure(figsize=(10, 6))
sns.barplot(x='Item', y='item_count', data=item_data, palette="coolwarm")
plt.xlabel('Продукты', fontsize=14)
plt.ylabel('Количество товаров (item_count)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

plt.figure(figsize=(10, 6))
sns.barplot(x='Item', y='total_%', data=item_data, palette="coolwarm")
plt.title('Процент от общего количества продаж по продуктам', fontsize=16)
plt.xlabel('Продукты', fontsize=14)
plt.ylabel('Процент (total_%)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

cashier_num_data = (supermarket.groupby('CashierNumber').agg(check_count=('ReceiptNumber', 'nunique'), item_count=('Item', 'count'), top_item=('Item', lambda x: x.mode())).reset_index())
cashier_num_data = cashier_num_data.sort_values(by=['check_count'], ascending=False).head(5)
plt.figure(figsize=(10, 6))
sns.barplot(x='CashierNumber', y='check_count', data=cashier_num_data, palette="coolwarm")
plt.title('Количество чеков по кассиру', fontsize=16)
plt.xlabel('Номер кассы', fontsize=14)
plt.ylabel('Количество чеков (check_count)', fontsize=14)
plt.yticks(fontsize=12)
st.pyplot(plt)

plt.figure(figsize=(10, 6))
sns.barplot(x='CashierNumber', y='item_count', data=cashier_num_data, palette="coolwarm")
plt.title('Количество товаров по кассиру', fontsize=16)
plt.xlabel('Номер кассы', fontsize=14)
plt.ylabel('Количество товаров (item_count)', fontsize=14)
plt.yticks(fontsize=12)
st.pyplot(plt)

discount_data = (supermarket.groupby('Discount').agg(item_count=('Item', 'count'),total_amount=('Amount', 'sum')).reset_index())
discount_data['item_count%'] =  discount_data['item_count']/discount_data['item_count'].sum()*100
discount_data['item_count%'] = discount_data['item_count%'].round(2)
discount_data['total_amount%'] =  discount_data['total_amount']/discount_data['total_amount'].sum()*100
discount_data['total_amount%'] = discount_data['total_amount%'].round()

fig, axes = plt.subplots(2, 1, figsize=(15, 6))
sns.barplot(x='Discount', y='item_count%', data=discount_data, ax=axes[0], palette="coolwarm")
axes[0].set_title('Распределение item_count% по Discount', fontsize=16)
axes[0].set_xlabel('Скидка (%)', fontsize=14)
axes[0].set_ylabel('item_count%', fontsize=14)
sns.barplot(x='Discount', y='total_amount%', data=discount_data, ax=axes[1], palette="coolwarm")
axes[1].set_title('Распределение total_amount% по Discount', fontsize=16)
axes[1].set_xlabel('Скидка (%)', fontsize=14)
axes[1].set_ylabel('total_amount%', fontsize=14)

plt.tight_layout()
st.pyplot(plt)



cashier_stats =supermarket.groupby('Cashier') .agg(check_count=('ReceiptNumber', 'nunique'),total_amount=('Amount', 'sum')).reset_index()
cashier_stats['total_amount%'] = cashier_stats['total_amount'] / cashier_stats['total_amount'].sum() * 100
cashier_stats['total_amount%'] = cashier_stats['total_amount%'].round(2)
cashier_stats = cashier_stats.sort_values(by=['check_count'], ascending=False).head(5)
fig, axes = plt.subplots(2, 1, figsize=(15, 6))

sns.barplot(x='Cashier', y='check_count', data=cashier_stats, ax=axes[0], palette="coolwarm")
axes[0].set_title('Количество чеков по кассиру', fontsize=16)
axes[0].set_xlabel('Кассир', fontsize=14)
axes[0].set_ylabel('Количество чеков (check_count)', fontsize=14)
axes[0].tick_params(axis='y', labelsize=12)

sns.barplot(x='Cashier', y='total_amount%', data=cashier_stats, ax=axes[1], palette="coolwarm")
axes[1].set_title('Процент от суммы по кассиру', fontsize=16)
axes[1].set_xlabel('Кассир', fontsize=14)
axes[1].set_ylabel('total_amount%', fontsize=14)
axes[1].tick_params(axis='y', labelsize=12)

plt.tight_layout()
st.pyplot(plt)


receipt_data = (supermarket.groupby('ReceiptNumber').agg(total_amount=('Amount', 'sum'), item_count=('Item', 'count')).reset_index())
bins = [15, 500, 1000, 1500, 2000, 2500, 3000]
labels = ['15-500', '500-1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000']
receipt_data['Amount_bin'] = pd.cut(receipt_data['total_amount'], bins=bins, labels=labels, right=False)
bin_distribution = receipt_data['Amount_bin'].value_counts().sort_index()
plt.figure(figsize=(8, 6))
sns.barplot(x=bin_distribution.index, y=bin_distribution.values, palette="coolwarm")
plt.title('Распределение по бинсам', fontsize=16)
plt.xlabel('Интервал суммы чека', fontsize=14)
plt.ylabel('Количество чеков', fontsize=14)
plt.yticks(fontsize=12)

st.pyplot(plt)


