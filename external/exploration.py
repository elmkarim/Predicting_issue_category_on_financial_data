
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


class online_graph():
    
    def __init__(self):
        from helper_save_load import load_from_pickle
        _, _, self.df_v = load_from_pickle("../data/dataframes_Dollars.pickle")
        self.df_v = self.df_v.loc[:,~self.df_v.columns.duplicated()]
        self.pos_with_brands = load_from_pickle("../data/pos_with_brands.pickle")
        
    def get_brands(self):
        return self.pos_with_brands['Brand'].sort_values().unique()

    def group_by_TR_BR(self, territory, brand):
        v = self.df_v.groupby(["Territory", "Brand"]).sum().loc[territory].loc[brand]
        return v

    def plot_variance(self, variance):
        plt.figure(figsize=(30,10))
        plt.plot(variance)

        plt.xticks(rotation=90, fontsize=18)
        plt.yticks(fontsize=18)
        plt.title(variance.name, fontsize=24)
        plt.grid(axis='x')
        plt.hlines(0, 0, len(variance)-1)
        plt.xlim(0, len(variance)-1)
        plt.ylabel('Variance')

        plt.show()


    def plot_graph(self, brand, period):
        group_by_day = self.pos_with_brands.groupby([self.pos_with_brands["POSDate"].dt.to_period(period), "Brand"]).                   agg({"TotalSales":"sum", "TotalQty":"sum"}).reset_index()
        group_by_day["MonthlyUnitPrice"] = group_by_day["TotalSales"]/group_by_day["TotalQty"]
        to_plot = group_by_day[group_by_day["Brand"] == brand]

        plt.rcParams.update({'font.size': 22})

        ax = to_plot.plot(x="POSDate", y="TotalQty", figsize=(30,10), linewidth=2, label="Sales (Qty)")
        ax2 = to_plot.plot(x="POSDate", y="MonthlyUnitPrice", ax=ax, secondary_y=True, linewidth=2, label="Unit Price")

        ax.set_ylabel("Sales", fontsize=28, labelpad=20)
        ax2.set_ylabel("Average unit price of brand ($)", fontsize=28, labelpad=40 ,rotation=-90)
        ax.set_xlabel("Date", fontsize=28)

        ax.set_title(brand, fontsize=30)
        ax.grid(axis='x')

        from matplotlib.ticker import MultipleLocator, FormatStrFormatter
        import matplotlib.dates as dates

        ax.xaxis.set_major_locator(dates.MonthLocator(bymonth=None, bymonthday=1, interval=1))

        v = self.group_by_TR_BR("M7400 - WALMART", brand)
        self.plot_variance(v)

        plt.show()


