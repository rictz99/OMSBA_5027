#!/usr/bin/env python
# coding: utf-8

# In[62]:


# import modules
import requests
import pandas as pd

# create request header
headers = {'User-Agent': "rictz99@gmail.com"}

# Tesla CIK
CIK_tsla = '0001318605'

# fetch company facts for Tesla
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK_tsla}.json'
response = requests.get(url, headers=headers)
companyFacts = response.json()

# helper function to extract financial data for a specific tag
def get_tag_df(tag):
    try:
        return pd.DataFrame(companyFacts['facts']['us-gaap'][tag]['units']['USD'])
    except KeyError:
        return pd.DataFrame(columns=['accn', 'end', 'val', 'form', 'fy'])

# === Income Statement Metrics ===

revenues_df = get_tag_df('Revenues')
net_income_df = get_tag_df('NetIncomeLoss')
gross_profit_df = get_tag_df('GrossProfit')

revenues_df = revenues_df[revenues_df['form'] == '10-K']
net_income_df = net_income_df[net_income_df['form'] == '10-K']
gross_profit_df = gross_profit_df[gross_profit_df['form'] == '10-K']

revenues_df = revenues_df.sort_values('end').drop_duplicates('accn', keep='last')
net_income_df = net_income_df.sort_values('end').drop_duplicates('accn', keep='last')
gross_profit_df = gross_profit_df.sort_values('end').drop_duplicates('accn', keep='last')

df = revenues_df[['accn', 'end', 'val']].rename(columns={'val': 'revenue'})
df = df.merge(net_income_df[['accn', 'end', 'val']].rename(columns={'val': 'net_income'}), on=['accn', 'end'])
df = df.merge(gross_profit_df[['accn', 'end', 'val']].rename(columns={'val': 'gross_profit'}), on=['accn', 'end'])

df['gross_profit_margin'] = df['gross_profit'] / df['revenue']
df['net_profit_margin'] = df['net_income'] / df['revenue']

print("\nTesla Income Statement Metrics:")
print(df[['end', 'revenue', 'net_income', 'gross_profit', 'gross_profit_margin', 'net_profit_margin']])

# === Quick Ratio Calculation ===

assets_df = get_tag_df('AssetsCurrent')
liabilities_df = get_tag_df('LiabilitiesCurrent')
inventory_df = get_tag_df('InventoryNet')

assets_df['label'] = 'assets'
liabilities_df['label'] = 'liabilities'
inventory_df['label'] = 'inventory'

all_df = pd.concat([assets_df, liabilities_df, inventory_df], ignore_index=True)
all_df['fy'] = pd.to_numeric(all_df['fy'], errors='coerce')

filtered_df = all_df[(all_df['form'] == '10-K') & (all_df['fy'] >= 2011)]

pivot_df = filtered_df.pivot_table(index=['accn', 'end', 'fy'], columns='label', values='val', aggfunc='first').reset_index()
pivot_df = pivot_df.dropna(subset=['assets', 'inventory', 'liabilities'])
pivot_df['quick_ratio'] = (pivot_df['assets'] - pivot_df['inventory']) / pivot_df['liabilities']

pivot_df = pivot_df.sort_values('end').drop_duplicates('fy', keep='last')

print("\nTesla Quick Ratio (2011 and onward):")
print(pivot_df[['fy', 'end', 'quick_ratio']].sort_values('fy'))




# In[65]:


import matplotlib.pyplot as plt

# Convert 'end' column to datetime
df['end'] = pd.to_datetime(df['end'])
df = df.sort_values('end')

# Plot Net Profit Margin
plt.figure(figsize=(10, 6))
plt.plot(df['end'], df['net_profit_margin'], marker='o', label='Net Profit Margin')
plt.plot(df['end'], df['gross_profit_margin'], marker='s', label='Gross Profit Margin')

plt.title('Tesla Profit Margins Over Time')
plt.xlabel('Fiscal Year')
plt.ylabel('Profit Margin')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
 


# In[66]:


# Convert 'end' column to datetime and sort
pivot_df['end'] = pd.to_datetime(pivot_df['end'])
pivot_df = pivot_df.sort_values('end')

# Plot Quick Ratio
plt.figure(figsize=(10, 6))
plt.plot(pivot_df['end'], pivot_df['quick_ratio'], marker='o', linestyle='-')

plt.title('Tesla Quick Ratio Over Time')
plt.xlabel('Fiscal Year')
plt.ylabel('Quick Ratio')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
 


# In[67]:


# Convert 'end' column to datetime and sort
df['end'] = pd.to_datetime(df['end'])
df = df.sort_values('end')

# Plot Net Income over time
plt.figure(figsize=(10, 6))
plt.plot(df['end'], df['net_income'] / 1e9, marker='o', linestyle='-')

plt.title('Tesla Net Income Over Time')
plt.xlabel('Fiscal Year')
plt.ylabel('Net Income (Billions USD)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




