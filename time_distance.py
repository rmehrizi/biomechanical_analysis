import pandas as pd

def event_detection(body_mass, constant, fp_data):
    # find the first RHS
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

    output = [heel_strike_r, toe_off_r, heel_strike_l, toe_off_l]
    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output,columns=['HSR','TOR','HSL','TOL'])

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


