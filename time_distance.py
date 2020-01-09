# Rahil Mehrizi
# Jan 2020
# A moduale for calculating gait events and time-distance features

import pandas as pd

def event_detection(fp_data, body_mass, constant = 0.05):
    
     """Returns the times at which heel strikes and toe offs happen based on the forca plate data.
     Methods
     ==========
     A treshhold is being defined as a percentage of total body weight (constant * body_mass * 9.81) and heel strike 
     happens when the vertical ground reaction force goes above a treshhold after being below the treshhold. Toe off 
     happens when the vertical ground reaction force goes below a treshhold after being above the treshhold.   
     Parameters
     ==========
        fp_data : dataframe
            A dataframe with two columns including left and right vertical ground reaction force in N
        body_mass : float
            body mass in kg
        constant : float
            predifed percentage to detect heel strike and toe off           
        Returns
        =======
        A dataframe with four columns:
        HSL : All indices at which fp_data['for_l_y'] is greater than constant * body_weight and it was less than 
              constant * body_weight at the preceding time index.
        TOL : All indices at which fp_data['for_l_y'] is less than constant * body_weight and it was greater than 
              constant * body_weight at the preceding time index.
        HSR : All indices at which fp_data['for_r_y'] is greater than constant * body_weight and it was less than 
              constant * body_weight at the preceding time index.
        TOR : All indices at which fp_data['for_r_y'] is less than constant * body_weight and it was greater than 
              constant * body_weight at the preceding time index.        
    """
      
    # left leg
    i = 0
    heel_strike_l = []
    toe_off_l = []
    while i < len(fp_data) - 1:
        if fp_data.loc[i,'for_l_y'] >= constant * body_mass * 9.81:
            i += 1
        else:
            toe_off_l.append(i)
            while (fp_data.loc[i,'for_l_y'] < constant * body_mass * 9.81) and (i < len(fp_data) - 1):
                i += 1
            heel_strike_l.append(i)
            
    # right leg
    i = 0
    heel_strike_r = []
    toe_off_r = []
    while i < len(fp_data) - 1:
        if fp_data.loc[i,'for_r_y'] >= constant * body_mass * 9.81:
            i += 1
        else:
            toe_off_r.append(i)
            while (fp_data.loc[i,'for_r_y'] < constant * body_mass * 9.81) and (i < len(fp_data) - 1):
                i += 1
            heel_strike_r.append(i)

    output = [heel_strike_l, toe_off_l, heel_strike_r, toe_off_r]
    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output,columns=['HSL','TOL','HSR','TOR'])

def cadence(events, total_time, delta):
    return (events.HSL.count() + events.HSR.count()) / (total_time * delta / 60)

def stance_ratio(events):
    if events.loc[0, 'HSL'] > events.loc[0, 'TOL']:
        events['TOL'] = events['TOL'].shift(periods=-1)

    stance_l = events['TOL'] - events['HSL']
    cycle_l = events['HSL'].diff(periods=-1)
    ratio_l = stance_l / cycle_l

    if events.loc[0,'HSR'] > events.loc[0,'TOR']:
        events['TOR'] = events['TOR'].shift(periods=-1)

    stance_r = events['TOR'] - events['HSR']
    cycle_r = events['HSR'].diff(periods=-1)
    ratio_r = stance_r / cycle_r

    return [-ratio_l.mean(), -ratio_r.mean()]


