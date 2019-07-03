import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec

get_ipython().run_line_magic('matplotlib', 'inline')

from helper_save_load import load_from_pickle

df_c, BR_TR_timeseries_windows, BR_TR_labels = load_from_pickle('plot_data.pkl')

WINDOW_SIZE = 13
territory_label_cols = df_c.columns[18:31].tolist()
label_cols = df_c.columns[12:18].tolist()


def plot_brand_month(brand, month):
    
    brand_month = df_c[(df_c["Brand_1"]==brand) & (df_c["Month"]==month)]["Num"]
    
    if brand_month.empty:
        print("*No data available*")
        
    else:
        num = brand_month.iloc[0]
        df_c[(df_c["Brand_1"]==brand) & (df_c["Month"]==month)]["Num"].iloc[0]
    
        num_indices = df_c["Num"].unique()
        num_idx = np.where(num_indices==num)[0][0]

        data = BR_TR_timeseries_windows[num_idx*13:num_idx*13+13]
        labels = np.argmax(BR_TR_labels[num_idx*13:num_idx*13+13], axis=1)
        commentaries = df_c[df_c["Num"] == num][["Brand_1", "Month", "Commentaries", "Territory", "Class"]]
        ylim = (np.min(data)-0.1, np.max(data)+0.1)
        
        
        xmonths = pd.date_range(end=pd.to_datetime(month, format='%b_%Y'), 
                                periods=13, freq='MS').strftime('%b_%y').to_list()
        
        colour_dict = {0:'r', 1:'g', 2:'m', 3:'c', 4:'grey', 5:'b'}
        
        gs00 = GridSpec(5, 3, hspace=0.7)

        fig = plt.figure(figsize=(30,20))
        axs = []

        ax = fig.add_subplot(gs00[0,1])
        axs.append(ax)
        for i in range(1, 5):
            for j in range(3):
                ax = fig.add_subplot(gs00[i,j])
                axs.append(ax)
                
        for i, ax in enumerate(axs):
            ax.hlines(0, -1, WINDOW_SIZE, linewidth=0.5)
            ax.plot(data[i], colour_dict[labels[i]], linewidth=3)
            ax.set_xlim(-1, WINDOW_SIZE)
            ax.set_ylim(ylim)
            ax.tick_params(labelsize=16)
            ax.set_xticks(np.arange(0, WINDOW_SIZE))
            ax.set_xticklabels(xmonths, rotation=45)
            ax.set_title(territory_label_cols[i], fontsize=22)
        
        fig.suptitle("Data for ({}, {})".format(brand, month), fontsize=30, y=0.95)
        markers = [plt.Line2D([0,0],[0,0],color=c, marker='o', linestyle='') for c in colour_dict.values()] 
        fig.legend(markers, label_cols, numpoints=1, markerscale=6, 
                   prop={'size': 30}, title='Commentary Type', title_fontsize=32)
        plt.show()
        
        with pd.option_context('display.max_colwidth', -1):
             display(commentaries)