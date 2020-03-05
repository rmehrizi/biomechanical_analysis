# Rahil Mehrizi
# Feb 2020
# A module for plotting gait parameters

import matplotlib.pyplot as plt


def events_plot(fp_data, events, event_type, n=200):

    # Plotting gait events
    plt.figure(figsize=(12, 5))
    plt.plot(fp_data.loc[:n, ['for_l_y']], label='Left Leg')
    plt.plot(fp_data.loc[:n, ['for_r_y']], label='Right Left')
    plt.legend(loc="lower right")
    
    if event_type == 'HSL' or event_type == 'all':
        i = 0
        while events['HSL'][i] <= n:
            plt.axvline(x=events['HSL'][i],color='g')
            plt.text(events['HSL'][i] + 0.5, 3, 'Heel Strike Left', rotation=90, fontsize=10)
            i += 1
            
    if event_type == 'TOL' or event_type == 'all':
        i = 0
        while events['TOL'][i] <= n:
            plt.axvline(x=events['TOL'][i], color='c')
            plt.text(events['TOL'][i] + 0.5, 3, 'Toe Off Left', rotation=90, fontsize=10)
            i += 1
    
    if event_type == 'HSR' or event_type == 'all':
        i = 0
        while events['HSR'][i] <= n:
            plt.axvline(x=events['HSR'][i],color='r')
            plt.text(events['HSR'][i] + 0.5, 3, 'Heel Strike Right', rotation=90, fontsize=10)
            i += 1
            
    if event_type == 'TOR' or event_type == 'all':
        i = 0
        while events['TOR'][i] <= n:
            plt.axvline(x=events['TOR'][i],color='m')
            plt.text(events['TOR'][i] + 0.5, 3, 'Toe Off Right', rotation=90, fontsize=10)
            i += 1
            
    plt.title('Gait events shown on vertical ground reaction force data')
    plt.show()


def angles_plot(angles, n=200, smooth=True):
    
    # Plotting joint angels
    if smooth:
        angles = angles.rolling(window=50).mean()
        
    plt.figure(figsize=(15, 8))
    for i, col in enumerate(angles.columns):
        ax = plt.subplot(2, 4, i+1)
        plt.plot(angles.loc[:n, col], label=col)
        plt.title(col)
        if i == 0 or i == 4:
            plt.ylabel('angel (degree)')

    plt.show()


def forces_plot(forces, body_mass, n=200, smooth=True):
    
    # Plotting joint forces
    forces = forces/body_mass # normalizing the force w.r.t. body mass
    if smooth:
        forces = forces.rolling(window=50).mean()
    plt.figure(figsize=(15, 5))
    j = 1
    for i in range(0, forces.shape[1],3):
        ax = plt.subplot(2,3,j)
        plt.plot(forces.iloc[:n,i], label=forces.columns[i])  
        plt.plot(forces.iloc[:n,i+1], label=forces.columns[i+1])  
        plt.plot(forces.iloc[:n,i+2], label=forces.columns[i+2])  
        plt.legend()
        if j == 1 or j == 4:
            plt.ylabel('force (N/kg)')
        j += 1

    plt.show()


def moments_plot(moments, body_mass, height, n=200, smooth=True):
    
    # Plotting joint moments
    # normalizing the moment w.r.t. body mass and height
    moments = moments/(body_mass*height)
    if smooth:
        moments = moments.rolling(window=50).mean()
    plt.figure(figsize=(15,5))
    j = 1
    for i in range(0,moments.shape[1],3):
        ax = plt.subplot(2,3,j)
        plt.plot(moments.iloc[:n,i], label=moments.columns[i])  
        plt.plot(moments.iloc[:n,i+1], label=moments.columns[i+1])  
        plt.plot(moments.iloc[:n,i+2], label=moments.columns[i+2])  
        plt.legend()
        if j == 1 or j == 4:
            plt.ylabel('moment (Nm/(kg*m)')
        j += 1

    plt.show()
