import matplotlib.pyplot as plt

def events_plot(fp_data, event, n = 200):
    
    # Plotting gait events
    plt.figure(figsize=(12,5))
    plt.plot(fp_data.loc[:n,['for_l_y']], label='Left Leg')
    plt.plot(fp_data.loc[:n,['for_r_y']], label='Right Left')
    plt.legend(loc="lower right")
    
    if event == 'HSL' or event == 'all':    
        i = 0
        while events['HSL'][i]<=n:
            plt.axvline(x = events['HSL'][i],color='g')
            plt.text(events['HSL'][i] + 0.5, 3, 'Heel Strike Left', rotation=90, fontsize=10)
            i += 1
            
    if event == 'TOL' or event == 'all':    
        i = 0
        while events['TOL'][i]<=n:
            plt.axvline(x = events['TOL'][i],color='c')
            plt.text(events['TOL'][i] + 0.5, 3, 'Toe Off Left', rotation=90, fontsize=10)
            i += 1
    
    if event == 'HSR' or event == 'all':    
        i = 0
        while events['HSR'][i]<=n:
            plt.axvline(x = events['HSR'][i],color='r')
            plt.text(events['HSR'][i] + 0.5, 3, 'Heel Strike Right', rotation=90, fontsize=10)
            i += 1
            
    if event == 'TOR' or event == 'all':    
        i = 0
        while events['TOR'][i]<=n:
            plt.axvline(x = events['TOR'][i],color='m')
            plt.text(events['TOR'][i] + 0.5, 3, 'Toe Off Right', rotation=90, fontsize=10)
            i += 1
            
    plt.title('Gait events shown on vertical ground reaction force data')
    
def angles_plot(angles, n = 200, smooth=True):
    
    # Plotting joint angels
    if smooth:
        angles = angles.rolling(window=50).mean()
        
    plt.figure(figsize=(15,8))
    for i, col in enumerate(angles.columns):
        ax = plt.subplot(2,4,i+1)
        plt.plot(angles.loc[:n,col], label=col)  
        plt.title(col)
        if i==0 or i==4:
            plt.ylabel('angel (degree)')
