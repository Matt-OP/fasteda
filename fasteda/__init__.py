import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt #graphing
import seaborn as sns #graphing
import missingno as msno
from colorama import Fore, Back, Style

plt.style.use("fivethirtyeight")


def fast_eda(df, target=None, correlation=True, pairplot=True, hist_box_plot=True, countplot=True):
    
    if df.shape > (1, 1):
        
        # Head
        
        print(f"{Fore.GREEN}{Style.BRIGHT}DataFrame Head:{Style.RESET_ALL}")
        print()
        display(df.head(3))
        
        # Tail
        
        print(f"{Fore.GREEN}{Style.BRIGHT}DataFrame Tail:{Style.RESET_ALL}")
        print()
        display(df.tail(3))
        print("-" * 100)
        
        # Missing values
        
        print(f"{Fore.RED}{Style.BRIGHT}Missing values:{Style.RESET_ALL}")
        print()

        null_cols = [i for i in df.columns if df[i].isna().sum() > 0]
        df0 = df[null_cols]

        display(df0.isna().sum().to_frame().style \
                .set_properties(**{"background-color": "#000000", "color": "#ff0000"}))
        print("-" * 100)
        
        # MSNO Matrix

        if df.shape[1] < 100:
            if len(null_cols) > 0:
                print(f"{Fore.RED}{Style.BRIGHT}MSNO Matrix:{Style.RESET_ALL}")
                print()
                ax = msno.matrix(df, figsize = (12, 8))
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

        if df.columns.nunique() < 12:
            display(df.describe().style.background_gradient(cmap = "Spectral"))
            print("-" * 100)
        else:
            display(df.describe().T.style.background_gradient(cmap = "Spectral"))
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
            
            for index, col in enumerate(num_cols):
              #  if i == "Id":
              #      pas    
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))

                sns.histplot(df, x = df[col], kde = True, hue = target,
                             color = sns.color_palette("hls", df.shape[1])[index], ax = ax1)

                sns.boxplot(x = df[col], width = 0.4, linewidth = 4, fliersize = 2.5,
                            color = sns.color_palette("hls", df.shape[1])[index], ax = ax2)

                fig.suptitle(f"Histogram and Boxplot of {col}", size = 20, y = 1.02)
                plt.show()
        
        # Countplot
        
        if countplot:
            
            if len(cat_cols) > 0:
                
                print("-" * 100)    
                print(f"{Fore.YELLOW}{Style.BRIGHT}Countplot(s):{Style.RESET_ALL}")
                print()

                for i in cat_cols:
                    
                    plt.figure(figsize = (12, 8))

                    for j in df[i].value_counts().keys():
                        if len(str(j)) > 15:
                            plt.xticks(fontsize = 8)
                            plt.yticks(fontsize = 8)
                            
                    large_to_small = df.groupby(i).size().sort_values().index[::-1]        

                    if len(df[i].value_counts()) >= 10:

                        ax = sns.countplot(y = df[i], edgecolor = "#000000", order = large_to_small)

                        for container in ax.containers:
                            ax.bar_label(container, padding = 5)

                        plt.title(f"Countplot of {i}", fontsize = 20)      
                        plt.show()

                    elif len(df[i].value_counts()) > 1:

                        ax = sns.countplot(x = df[i], edgecolor = "#000000", order = large_to_small)

                        for container in ax.containers:
                            ax.bar_label(container, padding = 5)

                        plt.title(f"Countplot of {i}", fontsize = 20)      
                        plt.show()
                
    else:
        raise Exception("Dataframe is too small to examine")