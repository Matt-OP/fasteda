import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from scipy.stats import skew, kurtosis
import missingno as msno
from colorama import Fore, Back, Style

plt.style.use("fivethirtyeight")
pd.set_option("display.max_columns", 500)


def fast_eda(df, target=None, correlation=True, pairplot=True, hist_box_plot=True, countplot=True):
    
    if df.shape > (1, 1):
        
        # Head
        
        print(f"{Fore.GREEN}{Style.BRIGHT}DataFrame Head:{Style.RESET_ALL}")
        display(df.head(3))
        
        # Tail
        
        print(f"{Fore.GREEN}{Style.BRIGHT}DataFrame Tail:{Style.RESET_ALL}")
        display(df.tail(3))
        print("-" * 100)
        
        # Missing values
        
        print(f"{Fore.RED}{Style.BRIGHT}Missing values:{Style.RESET_ALL}")

        null_cols = [i for i in df.columns if df[i].isna().sum() > 0]
        df0 = df[null_cols]

        display(df0.isna().sum().to_frame().style \
                .set_properties(**{"background-color": "#000000", "color": "#ff0000", "font-weight": "bold"}))
        print("-" * 100)
        
        # MSNO Matrix

        if df.shape[1] < 100:
            if len(null_cols) > 0:
                print(f"{Fore.RED}{Style.BRIGHT}MSNO Matrix:{Style.RESET_ALL}")
                print()
                ax = msno.matrix(df, color = (0, 0.5, 0), figsize = (12, 8))
                plt.show()
                print("-" * 100)
        
        # Shape
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}Shape of DataFrame:{Style.RESET_ALL}")
        print()
        print(df.shape)
        print()
        print("-" * 100)
        
        # Info
        
        print(f"{Fore.GREEN}{Style.BRIGHT}DataFrame Info:{Style.RESET_ALL}") 
        print()
        df.info()
        print("-" * 100)
        
        # Describe
        
        print(f"{Fore.BLUE}{Style.BRIGHT}Describe DataFrame:{Style.RESET_ALL}")
        print()
        
        def color_negative_red(value):
            if value < 0: color = "#ff0000"
            elif value > 0: color = "#00ff00"
            else: color = "#FFFFFF"
            return "color: %s" % color
        
        skew_ = df._get_numeric_data().dropna().apply(lambda x: skew(x)).to_frame(name = "skewness")
        kurt_ = df._get_numeric_data().dropna().apply(lambda x: kurtosis(x)).to_frame(name = "kurtosis")
        skew_kurt = pd.concat([skew_, kurt_], axis = 1)

        desc_df = df.describe().T
        
        full_info = pd.concat([desc_df, skew_kurt], ignore_index = True, axis = 1)
        full_info.columns = list(desc_df.columns) + list(skew_kurt.columns)
        full_info.insert(loc = 2, column = "median", value = df.median(skipna = True, numeric_only = True))
        
        full_info.iloc[:,:-2] = full_info.iloc[:,:-2].applymap(lambda x: format(x, '.3f') \
                                         .rstrip('0').rstrip('.') if isinstance(x, (int, float)) else x)
        
        info_cols = ["skewness", "kurtosis"]
        
        display(full_info.style.background_gradient(cmap = "Spectral", subset = full_info.columns[:-2])
                         .applymap(color_negative_red, subset = info_cols)
                         .set_properties(**{"background-color": "#000000", "font-weight": "bold"}, subset = info_cols)
                         .set_properties(**{"font-weight": "bold"}, subset = full_info.columns[:-2]))
        print("-" * 100)
        
        # categorical variables
        
        cat_cols = [col for col in df.columns if df[col].dtypes == 'O']

        num_but_cat = [col for col in df.columns if
                       df[col].nunique() <= 15 and df[col].dtypes != 'O']

        cat_but_car = [col for col in df.columns if
                       df[col].nunique() > 15 and df[col].dtypes == 'O']

        cat_cols = cat_cols + num_but_cat
        cat_cols = [col for col in cat_cols if col not in cat_but_car]

        # numerical variables
        
        num_cols = [col for col in df.columns if df[col].dtypes != 'O']
        num_cols = [col for col in num_cols if col not in num_but_cat]
        
        # Correlation
        
        if correlation:
            print(f"{Fore.BLUE}{Style.BRIGHT}DataFrame Correlation:{Style.RESET_ALL}")
            print()

            plt.figure(figsize = (12, 8))

            if df.columns.nunique() < 10:    
                sns.heatmap(df.corr(), annot = True, cmap = "Spectral", linewidths = 2, linecolor = "#000000", fmt='.3f')
                plt.show()
            elif df.columns.nunique() < 15:    
                sns.heatmap(df.corr(), annot = True, cmap = "Spectral", linewidths = 2, linecolor = "#000000", fmt='.2f')
                plt.show()    
            elif df.columns.nunique() < 25:   
                sns.heatmap(df.corr(), annot = True, cmap = "Spectral", linewidths = 2, linecolor = "#000000", fmt='.1f')
                plt.show()
            else:
                sns.heatmap(df.corr(), annot = False, cmap = "Spectral")
                plt.show()
        
        # Pairplot
        
        if pairplot:
            if df.columns.nunique() < 15:
                print("-" * 100)    

                print(f"{Fore.BLUE}{Style.BRIGHT}DataFrame Pairplot:{Style.RESET_ALL}")
                print()
                
                not_bool = [col for col in df.columns if df[col].dtypes != bool]
                df_bool = df[not_bool]
                
                if target:
                    sns.pairplot(df_bool, hue = target, palette = sns.color_palette("hls", df[target].nunique()))
                    plt.show()
                else:
                    sns.pairplot(df_bool)
                    plt.show()
        
        # Hist & Box
        
        if hist_box_plot:
            print("-" * 100)    
            print(f"{Fore.YELLOW}{Style.BRIGHT}Histogram(s) & Boxplot(s):{Style.RESET_ALL}")
            print()
            
            if not target:
            
                for idx, col in enumerate(num_cols):

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))

                    sns.histplot(df, x = df[col], kde = True,
                                 color = sns.color_palette("hls", len(num_cols))[idx], ax = ax1)

                    sns.boxplot(x = df[col], width = 0.4, linewidth = 3, fliersize = 2.5,
                                color = sns.color_palette("hls", len(num_cols))[idx], ax = ax2)

                    fig.suptitle(f"Histogram and Boxplot of {col}", size = 20, y = 1.02)
                    plt.show()
                    
            elif target and df[target].nunique() == 2:
                
                for idx, col in enumerate(num_cols):

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))

                    sns.histplot(df, x = df[col], kde = True, hue = target,
                                 color = sns.color_palette("hls", len(num_cols))[idx], ax = ax1)
                    
                    box_dict =  {"boxprops":     dict(color = "#000000", linewidth = 2),
                                 "capprops":     dict(color = "#000000", linewidth = 1.5),
                                 "medianprops":  dict(color = "#000000", linewidth = 1.5),
                                 "whiskerprops": dict(color = "#000000", linewidth = 1.5),
                                 "flierprops":   dict(markeredgecolor = "#ff9900"),
                                 "meanprops":    dict(markeredgecolor = "#000000")}

                    df.boxplot(by = target, column = [col], widths = 0.5, showmeans = True,
                               patch_artist = True, vert = False, **box_dict, ax = ax2)
                    
                    ax2.set_ylim(ax2.get_ylim()[::-1])
                    ax2.set_title(None)
                    ax2.set_xlabel(col)
                    
                    boxes = ax2.findobj(matplotlib.artist.Artist)
                    
                    if df[target].dtypes == 'O':
                        for i, box in enumerate(boxes):
                            if isinstance(box, matplotlib.patches.PathPatch): 
                                if i < 3: box.set_facecolor("#ea4b33")
                                if i > 3: box.set_facecolor("#3490d6")
                    else:
                        for i, box in enumerate(boxes):
                            if isinstance(box, matplotlib.patches.PathPatch): 
                                if i < 3: box.set_facecolor("#3490d6")
                                if i > 3: box.set_facecolor("#ea4b33")
                        
                    fig.suptitle(f"Histogram and Boxplot of {col}", size = 20, y = 1.02)
                    plt.show()
                    
            else:
                
                for idx, col in enumerate(num_cols):

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))

                    sns.histplot(df, x = df[col], kde = True, hue = target,
                                 color = sns.color_palette("hls", len(num_cols))[idx], ax = ax1)

                    sns.boxplot(x = df[col], width = 0.4, linewidth = 3, fliersize = 2.5,
                                color = sns.color_palette("hls", len(num_cols))[idx], ax = ax2)

                    fig.suptitle(f"Histogram and Boxplot of {col}", size = 20, y = 1.02)
                    plt.show()

        # Countplot
        
        if countplot:
            
            if len(cat_cols) > 0:
                
                print("-" * 100)    
                print(f"{Fore.YELLOW}{Style.BRIGHT}Countplot(s):{Style.RESET_ALL}")
                print()

                for col in cat_cols:
                    
                    plt.figure(figsize = (12, 8))

                    for i in df[col].value_counts().keys():
                        if len(str(i)) > 15:
                            plt.xticks(fontsize = 8)
                            plt.yticks(fontsize = 8)
                            
                    large_to_small = df.groupby(col).size().sort_values().index[::-1]        

                    if len(df[col].value_counts()) >= 10:

                        ax = sns.countplot(y = df[col], edgecolor = "#000000", order = large_to_small)

                        for container in ax.containers:
                            ax.bar_label(container, padding = 5)

                        plt.title(f"Countplot of {col}", fontsize = 20)      
                        plt.show()

                    elif len(df[col].value_counts()) > 1:

                        ax = sns.countplot(x = df[col], edgecolor = "#000000", order = large_to_small)

                        for container in ax.containers:
                            ax.bar_label(container, padding = 5)

                        plt.title(f"Countplot of {col}", fontsize = 20)      
                        plt.show()
                
    else:
        raise Exception("Dataframe is too small to examine")
