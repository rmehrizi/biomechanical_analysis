# Rahil Mehrizi
# Jan 2020
# A module for performing inverse kinetics on marker and force plate data

import pandas as pd


def mass(body_mass, gender):
    
    """Returns segment's mass as a fraction of total body mass

    Methods
    ==========
    De Leva, Paolo. "ADJUSTMENTS TO ZATSIORSKY-SELUYANOV" S SEGMENT IN ERTIA PARAMETERS."
    J biomech 29.9 (1996): 1223-1230.
     
    Parameters
    ==========
    body_mass : float
        total body mass in kg
    gender: bool
        0 : male
        1 : female
            
    Returns
    =======
        A dictionary with mass of each body segment in kg
    """

    if gender == 0:
        c1 = 14.16
        c2 = 4.33
        c3 = 1.37
    if gender == 1:
        c1 = 14.78
        c2 = 4.81
        c3 = 1.29
    thigh_l_mass = c1 * 0.01 * body_mass
    shank_l_mass = c2 * 0.01 * body_mass
    foot_l_mass = c3 * 0.01 * body_mass
    thigh_r_mass = c1 * 0.01 * body_mass
    shank_r_mass = c2 * 0.01 * body_mass
    foot_r_mass = c3 * 0.01 * body_mass

    return dict({'thigh_l': thigh_l_mass, 'shank_l': shank_l_mass, 'foot_l': foot_l_mass,
                 'thigh_r': thigh_r_mass, 'shank_r': shank_r_mass, 'foot_r': foot_r_mass})


def center_of_mass(marker_data, gender):
    
    """Returns segment's center of mass coordinates based on the fraction of length
     
    Methods
    ==========
    De Leva, Paolo. "ADJUSTMENTS TO ZATSIORSKY-SELUYANOV" S SEGMENT IN ERTIA PARAMETERS."
    J biomech 29.9 (1996): 1223-1230.
     
    Parameters
    ==========
    marker_data : dataframe
        A dataframe with 27 columns including 3d coordinates of 9 joints
    gender: bool
        0 : male
        1 : female
            
    Returns
    =======
        A dataframe with 18 columns including 3d coordinates of 6 body segment center of mass
    """ 
    
    if gender == 0:
        c1 = 40.95
        c2 = 44.59
        c3 = 44.15
    if gender == 1:
        c1 = 36.9
        c2 = 27.1
        c3 = 29.9

    output = []
    output.append(marker_data['hip_l_x'] - c1 * 0.01 * (marker_data['hip_l_x'] - marker_data['knee_l_x']))
    output.append(marker_data['hip_l_y'] - c1 * 0.01 * (marker_data['hip_l_y'] - marker_data['knee_l_y']))
    output.append(marker_data['hip_l_z'] - c1 * 0.01 * (marker_data['hip_l_z'] - marker_data['knee_l_z']))

    output.append(marker_data['knee_l_x'] - c2 * 0.01 * (marker_data['knee_l_x'] - marker_data['ankle_l_x']))
    output.append(marker_data['knee_l_y'] - c2 * 0.01 * (marker_data['knee_l_y'] - marker_data['ankle_l_y']))
    output.append(marker_data['knee_l_z'] - c2 * 0.01 * (marker_data['knee_l_z'] - marker_data['ankle_l_z']))

    output.append(marker_data['ankle_l_x'] - c3 * 0.01 * (marker_data['ankle_l_x'] - marker_data['toe2_l_x']))
    output.append(marker_data['ankle_l_y'] - c3 * 0.01 * (marker_data['ankle_l_y'] - marker_data['toe2_l_y']))
    output.append(marker_data['ankle_l_z'] - c3 * 0.01 * (marker_data['ankle_l_z'] - marker_data['toe2_l_z']))

    output.append(marker_data['hip_r_x'] - c1 * 0.01 * (marker_data['hip_r_x'] - marker_data['knee_r_x']))
    output.append(marker_data['hip_r_y'] - c1 * 0.01 * (marker_data['hip_r_y'] - marker_data['knee_r_y']))
    output.append(marker_data['hip_r_z'] - c1 * 0.01 * (marker_data['hip_r_z'] - marker_data['knee_r_z']))

    output.append(marker_data['knee_r_x'] - c2 * 0.01 * (marker_data['knee_r_x'] - marker_data['ankle_r_x']))
    output.append(marker_data['knee_r_y'] - c2 * 0.01 * (marker_data['knee_r_y'] - marker_data['ankle_r_y']))
    output.append(marker_data['knee_r_z'] - c2 * 0.01 * (marker_data['knee_r_z'] - marker_data['ankle_r_z']))

    output.append(marker_data['ankle_l_x'] - c3 * 0.01 * (marker_data['ankle_l_x'] - marker_data['toe2_l_x']))
    output.append(marker_data['ankle_r_y'] - c3 * 0.01 * (marker_data['ankle_r_y'] - marker_data['toe2_r_y']))
    output.append(marker_data['ankle_r_z'] - c3 * 0.01 * (marker_data['ankle_r_z'] - marker_data['toe2_r_z']))

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['thigh_l_x', 'thigh_l_y', 'thigh_l_z',
                                         'shank_l_x', 'shank_l_y', 'shank_l_z',
                                         'foot_l_x', 'foot_l_y', 'foot_l_z',
                                         'thigh_r_x', 'thigh_r_y', 'thigh_r_z',
                                         'shank_r_x', 'shank_r_y', 'shank_r_z',
                                         'foot_r_x', 'foot_r_y', 'foot_r_z'])


def derivative(df, delta=0.01, order=2):
    
    """Returns 1st and 2nd derivatives of a dataframe
     
     Methods
     ==========
     numerical calculating of derivative for each column 
     df/dx = (f(t) - f(t-1)) / delta_t
     d2f/dx2 = (f(t) - 2*f(t-1) + f(t-2)) / (delta_t)^2
     
     Parameters
     ==========
     df: dataframe
     delta: float
        delta_t in s
     order: [1,2]
        1: first derivative
        2: second derivative
            
     Returns
     =======
        A dataframe with values equal to the derivative of the input dataframe
    """

    if order == 1:
        deriv = (df - df.diff()) / delta
    if order == 2:
        deriv = (df - 2 * df.diff() + df.diff(periods=2)) / delta ** 2

    return deriv


def force(fp, mass, cm_dd):
    
    """Returns force at each joint in N
     
    Methods
    ==========
    Newton-Euler equations
    (Hof, At L. "An explicit expression for the moment in multibody systems."
    Journal of biomechanics 25.10 (1992): 1209-1211.)
     
    Parameters
    ==========
    fp: dataframe
        A dataframe with 6 columns including 3d components of the force applied to the left and right force plates in N
    mass: float
        total body mass in kg
    cm_dd: dataframe
        second derivative of each segment center of mass (output of derivative function)
              
    Returns
    =======
    A dataframe with 18 columns:
        ankle_l_x : x component of force applied on the left ankle
        ankle_l_y : y component of force applied on the left ankle
        ankle_l_z : z component of force applied on the left ankle
        knee_l_x : x component of force applied on the left knee
        knee_l_y : y component of force applied on the left knee
        knee_l_z : z component of force applied on the left knee
        hip_l_x : x component of force applied on the left hip
        hip_l_y : y component of force applied on the left hip
        hip_l_z : z component of force applied on the left hip
        ankle_r_x : x component of force applied on the right ankle
        ankle_r_y : y component of force applied on the right ankle
        ankle_r_z : z component of force applied on the right ankle
        knee_r_x : x component of force applied on the right knee
        knee_r_y : y component of force applied on the right knee
        knee_r_z : z component of force applied on the right knee
        hip_r_x : x component of force applied on the right hip
        hip_r_y : y component of force applied on the right hip
        hip_r_z : z component of force applied on the right hip

    """
        
    g_x, g_y, g_z = [0, -9.81, 0]
    cm_dd = cm_dd.dropna()

    output = []
    output.append(- fp['for_l_x'] - mass['foot_l'] * g_x + mass['foot_l'] * cm_dd['foot_l_x'])
    output.append(- fp['for_l_y'] - mass['foot_l'] * g_y + mass['foot_l'] * cm_dd['foot_l_y'])
    output.append(- fp['for_l_z'] - mass['foot_l'] * g_z + mass['foot_l'] * cm_dd['foot_l_z'])

    output.append(- output[0] - mass['shank_l'] * g_x + mass['shank_l'] * cm_dd['shank_l_x'])
    output.append(- output[1] - mass['shank_l'] * g_y + mass['shank_l'] * cm_dd['shank_l_y'])
    output.append(- output[2] - mass['shank_l'] * g_z + mass['shank_l'] * cm_dd['shank_l_z'])

    output.append(- output[3] - mass['thigh_l'] * g_x + mass['thigh_l'] * cm_dd['thigh_l_x'])
    output.append(- output[4] - mass['thigh_l'] * g_y + mass['thigh_l'] * cm_dd['thigh_l_y'])
    output.append(- output[5] - mass['thigh_l'] * g_z + mass['thigh_l'] * cm_dd['thigh_l_z'])

    output.append(- fp['for_r_x'] - mass['foot_r'] * g_x + mass['foot_r'] * cm_dd['foot_r_x'])
    output.append(- fp['for_r_y'] - mass['foot_r'] * g_y + mass['foot_r'] * cm_dd['foot_r_y'])
    output.append(- fp['for_r_z'] - mass['foot_r'] * g_z + mass['foot_r'] * cm_dd['foot_r_z'])

    output.append(- output[9] - mass['shank_r'] * g_x + mass['shank_r'] * cm_dd['shank_r_x'])
    output.append(- output[10] - mass['shank_r'] * g_x + mass['shank_r'] * cm_dd['shank_r_y'])
    output.append(- output[11] - mass['shank_r'] * g_x + mass['shank_r'] * cm_dd['shank_r_z'])

    output.append(- output[12] - mass['thigh_r'] * g_x + mass['thigh_r'] * cm_dd['thigh_r_x'])
    output.append(- output[13] - mass['thigh_r'] * g_y + mass['thigh_r'] * cm_dd['thigh_r_y'])
    output.append(- output[14] - mass['thigh_r'] * g_z + mass['thigh_r'] * cm_dd['thigh_r_z'])

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['ankle_l_x', 'ankle_l_y', 'ankle_l_z',
                                         'knee_l_x', 'knee_l_y', 'knee_l_z',
                                         'hip_l_x', 'hip_l_y', 'hip_l_z',
                                         'ankle_r_x', 'ankle_r_y', 'ankle_r_z',
                                         'knee_r_x', 'knee_r_y', 'knee_r_z',
                                         'hip_r_x', 'hip_r_y', 'hip_r_z'])


def moment(fp, marker, mass, cm, cm_dd, force):
    
    """Returns moment at each joint in Nm
     
    Methods
    ==========
    Newton-Euler equations
    (Hof, At L. "An explicit expression for the moment in multibody systems."
    Journal of biomechanics 25.10 (1992): 1209-1211.)
     
    Parameters
    ==========
    fp: dataframe
        A dataframe with 18 columns including 3d coordinates of center of pressure and 3d components of the force and
        moment applied to the left and right force plates in N
    marker_data : dataframe
        A dataframe with 27 columns including 3d coordinates of 9 joint    
    mass: float
        total body mass in kg
    cm: dataframe
        A dataframe with 18 columns including 3d coordinates of 6 body segment center of mass (output of center_of_mass function)
    cm_dd: dataframe
        second derivative of each segment center of mass (output of derivative function)
    force: dataframe
        A dataframe with 18 columns including 3d components of force at each joint  (output of force function)
              
    Returns
    =======
    A dataframe with 18 columns:
        ankle_l_x : x component of moment applied on the left ankle
        ankle_l_y : y component of moment applied on the left ankle
        ankle_l_z : z component of moment applied on the left ankle
        knee_l_x : x component of moment applied on the left knee
        knee_l_y : y component of moment applied on the left knee
        knee_l_z : z component of moment applied on the left knee
        hip_l_x : x component of moment applied on the left hip
        hip_l_y : y component of moment applied on the left hip
        hip_l_z : z component of moment applied on the left hip
        ankle_r_x : x component of moment applied on the right ankle
        ankle_r_y : y component of moment applied on the right ankle
        ankle_r_z : z component of moment applied on the right ankle
        knee_r_x : x component of moment applied on the right knee
        knee_r_y : y component of moment applied on the right knee
        knee_r_z : z component of moment applied on the right knee
        hip_r_x : x component of moment applied on the right hip
        hip_r_y : y component of moment applied on the right hip
        hip_r_z : z component of moment applied on the right hip

    """
        
    g_x, g_y, g_z = [0, -9.81, 0]
    cm_dd = cm_dd.dropna()

    output = []
    output.append(- fp['mom_l_x'] - (fp['cop_l_y'] - marker['ankle_l_y']) * fp['for_l_z'] - \
                 (fp['cop_l_z'] - marker['ankle_l_z']) * fp['for_l_y'] - \
                 (cm['foot_l_y'] - marker['ankle_l_y']) * mass['foot_l'] * g_z -\
                 (cm['foot_l_z'] - marker['ankle_l_z']) * mass['foot_l'] * g_y +\
                 (cm['foot_l_y'] - marker['ankle_l_y']) * mass['foot_l'] * cm_dd['foot_l_z'] +\
                 (cm['foot_l_z'] - marker['ankle_l_z']) * mass['foot_l'] * cm_dd['foot_l_y'])

    output.append(- fp['mom_l_y'] - (fp['cop_l_z'] - marker['ankle_l_z']) * fp['for_l_x'] - \
                 (fp['cop_l_x'] - marker['ankle_l_x']) * fp['for_l_z'] - \
                 (cm['foot_l_z'] - marker['ankle_l_z']) * mass['foot_l'] * g_x -\
                 (cm['foot_l_x'] - marker['ankle_l_x']) * mass['foot_l'] * g_z +\
                 (cm['foot_l_z'] - marker['ankle_l_z']) * mass['foot_l'] * cm_dd['foot_l_x'] +\
                 (cm['foot_l_x'] - marker['ankle_l_x']) * mass['foot_l'] * cm_dd['foot_l_z'])

    output.append(- fp['mom_l_z'] - (fp['cop_l_x'] - marker['ankle_l_x']) * fp['for_l_y'] - \
                 (fp['cop_l_y'] - marker['ankle_l_y']) * fp['for_l_x'] - \
                 (cm['foot_l_x'] - marker['ankle_l_x']) * mass['foot_l'] * g_y - \
                 (cm['foot_l_y'] - marker['ankle_l_y']) * mass['foot_l'] * g_x + \
                 (cm['foot_l_x'] - marker['ankle_l_x']) * mass['foot_l'] * cm_dd['foot_l_y'] + \
                 (cm['foot_l_y'] - marker['ankle_l_y']) * mass['foot_l'] * cm_dd['foot_l_x'])

    temp = - (marker['ankle_l_y'] - marker['knee_l_y']) * force['ankle_l_z'] - \
           (marker['ankle_l_z'] - marker['knee_l_z']) * force['ankle_l_y'] -\
           (cm['shank_l_y'] - marker['knee_l_y']) * mass['shank_l'] * g_z -\
           (cm['shank_l_z'] - marker['knee_l_z']) * mass['shank_l'] * g_y +\
           (cm['shank_l_y'] - marker['knee_l_y']) * mass['shank_l'] * cm_dd['shank_l_z'] +\
           (cm['shank_l_z'] - marker['knee_l_z']) * mass['shank_l'] * cm_dd['shank_l_y']

    output.append(- output[0] + temp)

    temp = - (marker['ankle_l_z'] - marker['knee_l_z']) * force['ankle_l_x'] -\
           (marker['ankle_l_x'] - marker['knee_l_x']) * force['ankle_l_z'] -\
           (cm['shank_l_z'] - marker['knee_l_z']) * mass['shank_l'] * g_x -\
           (cm['shank_l_x'] - marker['knee_l_x']) * mass['shank_l'] * g_z +\
           (cm['shank_l_z'] - marker['knee_l_z']) * mass['shank_l'] * cm_dd['shank_l_x'] +\
           (cm['shank_l_x'] - marker['knee_l_x']) * mass['shank_l'] * cm_dd['shank_l_z']

    output.append(- output[1] + temp)

    temp = - (marker['ankle_l_x'] - marker['knee_l_x']) * force['ankle_l_y'] - \
           (marker['ankle_l_y'] - marker['knee_l_y']) * force['ankle_l_x'] -\
           (cm['shank_l_x'] - marker['knee_l_x']) * mass['shank_l'] * g_y - \
           (cm['shank_l_y'] - marker['knee_l_y']) * mass['shank_l'] * g_x + \
           (cm['shank_l_x'] - marker['knee_l_x']) * mass['shank_l'] * cm_dd['shank_l_y'] + \
           (cm['shank_l_y'] - marker['knee_l_y']) * mass['shank_l'] * cm_dd['shank_l_x']

    output.append(- output[2] + temp)

    temp = - (marker['knee_l_y'] - marker['hip_l_y']) * force['knee_l_z'] -\
           (marker['knee_l_z'] - marker['hip_l_z']) * force['knee_l_y'] -\
           (cm['thigh_l_y'] - marker['hip_l_y']) * mass['thigh_l'] * g_z -\
           (cm['thigh_l_z'] - marker['hip_l_z']) * mass['thigh_l'] * g_y +\
           (cm['thigh_l_y'] - marker['hip_l_y']) * mass['thigh_l'] * cm_dd['thigh_l_z'] +\
           (cm['thigh_l_z'] - marker['hip_l_z']) * mass['thigh_l'] * cm_dd['thigh_l_y']

    output.append(- output[3] + temp)

    temp = - (marker['knee_l_z'] - marker['hip_l_z']) * force['knee_l_x'] -\
           (marker['knee_l_x'] - marker['hip_l_x']) * force['knee_l_z'] -\
           (cm['thigh_l_z'] - marker['hip_l_z']) * mass['thigh_l'] * g_x -\
           (cm['thigh_l_x'] - marker['hip_l_x']) * mass['thigh_l'] * g_z +\
           (cm['thigh_l_z'] - marker['hip_l_z']) * mass['thigh_l'] * cm_dd['thigh_l_x'] +\
           (cm['thigh_l_x'] - marker['hip_l_x']) * mass['thigh_l'] * cm_dd['thigh_l_z']

    output.append(- output[4] + temp)

    temp = - (marker['knee_l_x'] - marker['hip_l_x']) * force['knee_l_y'] -\
           (marker['knee_l_y'] - marker['hip_l_y']) * force['knee_l_x'] -\
           (cm['thigh_l_x'] - marker['hip_l_x']) * mass['thigh_l'] * g_y - \
           (cm['thigh_l_y'] - marker['hip_l_y']) * mass['thigh_l'] * g_x + \
           (cm['thigh_l_x'] - marker['hip_l_x']) * mass['thigh_l'] * cm_dd['thigh_l_y'] + \
           (cm['thigh_l_y'] - marker['hip_l_y']) * mass['thigh_l'] * cm_dd['thigh_l_x']

    output.append(- output[5] + temp)

    output.append(- fp['mom_r_x'] - (fp['cop_r_y'] - marker['ankle_r_y']) * fp['for_r_z'] - \
                 (fp['cop_r_z'] - marker['ankle_r_z']) * fp['for_r_y'] - \
                 (cm['foot_r_y'] - marker['ankle_r_y']) * mass['foot_r'] * g_z -\
                 (cm['foot_r_z'] - marker['ankle_r_z']) * mass['foot_r'] * g_y +\
                 (cm['foot_r_y'] - marker['ankle_r_y']) * mass['foot_r'] * cm_dd['foot_r_z'] +\
                 (cm['foot_r_z'] - marker['ankle_r_z']) * mass['foot_r'] * cm_dd['foot_r_y'])

    output.append(- fp['mom_r_y'] - (fp['cop_r_z'] - marker['ankle_r_z']) * fp['for_r_x'] - \
                 (fp['cop_r_x'] - marker['ankle_r_x']) * fp['for_r_z'] - \
                 (cm['foot_r_z'] - marker['ankle_r_z']) * mass['foot_l'] * g_x -\
                 (cm['foot_r_x'] - marker['ankle_r_x']) * mass['foot_l'] * g_z +\
                 (cm['foot_r_z'] - marker['ankle_r_z']) * mass['foot_l'] * cm_dd['foot_r_x'] +\
                 (cm['foot_r_x'] - marker['ankle_r_x']) * mass['foot_l'] * cm_dd['foot_r_z'])

    output.append(- fp['mom_r_z'] - (fp['cop_r_x'] - marker['ankle_r_x']) * fp['for_r_y'] - \
                 (fp['cop_r_y'] - marker['ankle_r_y']) * fp['for_r_x'] - \
                 (cm['foot_r_x'] - marker['ankle_r_x']) * mass['foot_l'] * g_y - \
                 (cm['foot_r_y'] - marker['ankle_r_y']) * mass['foot_l'] * g_x + \
                 (cm['foot_r_x'] - marker['ankle_r_x']) * mass['foot_l'] * cm_dd['foot_r_y'] + \
                 (cm['foot_r_y'] - marker['ankle_r_y']) * mass['foot_l'] * cm_dd['foot_r_x'])

    temp = - (marker['ankle_r_y'] - marker['knee_r_y']) * force['ankle_r_z'] - \
           (marker['ankle_r_z'] - marker['knee_r_z']) * force['ankle_r_y'] -\
           (cm['shank_r_y'] - marker['knee_r_y']) * mass['shank_l'] * g_z -\
           (cm['shank_r_z'] - marker['knee_r_z']) * mass['shank_l'] * g_y +\
           (cm['shank_r_y'] - marker['knee_r_y']) * mass['shank_l'] * cm_dd['shank_r_z'] +\
           (cm['shank_r_z'] - marker['knee_r_z']) * mass['shank_l'] * cm_dd['shank_r_y']

    output.append(- output[9] + temp)

    temp = - (marker['ankle_r_z'] - marker['knee_r_z']) * force['ankle_r_x'] -\
           (marker['ankle_r_x'] - marker['knee_r_x']) * force['ankle_r_z'] -\
           (cm['shank_r_z'] - marker['knee_r_z']) * mass['shank_l'] * g_x -\
           (cm['shank_r_x'] - marker['knee_r_x']) * mass['shank_l'] * g_z +\
           (cm['shank_r_z'] - marker['knee_r_z']) * mass['shank_l'] * cm_dd['shank_r_x'] +\
           (cm['shank_r_x'] - marker['knee_r_x']) * mass['shank_l'] * cm_dd['shank_r_z']

    output.append(- output[10] + temp)

    temp = - (marker['ankle_r_x'] - marker['knee_r_x']) * force['ankle_r_y'] - \
           (marker['ankle_r_y'] - marker['knee_r_y']) * force['ankle_r_x'] -\
           (cm['shank_r_x'] - marker['knee_r_x']) * mass['shank_l'] * g_y - \
           (cm['shank_r_y'] - marker['knee_r_y']) * mass['shank_l'] * g_x + \
           (cm['shank_r_x'] - marker['knee_r_x']) * mass['shank_l'] * cm_dd['shank_r_y'] + \
           (cm['shank_r_y'] - marker['knee_r_y']) * mass['shank_l'] * cm_dd['shank_r_x']

    output.append(- output[11] + temp)

    temp = - (marker['knee_r_y'] - marker['hip_r_y']) * force['knee_r_z'] -\
           (marker['knee_r_z'] - marker['hip_r_z']) * force['knee_r_y'] -\
           (cm['thigh_r_y'] - marker['hip_r_y']) * mass['thigh_l'] * g_z -\
           (cm['thigh_r_z'] - marker['hip_r_z']) * mass['thigh_l'] * g_y +\
           (cm['thigh_r_y'] - marker['hip_r_y']) * mass['thigh_l'] * cm_dd['thigh_r_z'] +\
           (cm['thigh_r_z'] - marker['hip_r_z']) * mass['thigh_l'] * cm_dd['thigh_r_y']

    output.append(- output[12] + temp)

    temp = - (marker['knee_r_z'] - marker['hip_r_z']) * force['knee_r_x'] -\
           (marker['knee_r_x'] - marker['hip_r_x']) * force['knee_r_z'] -\
           (cm['thigh_r_z'] - marker['hip_r_z']) * mass['thigh_l'] * g_x -\
           (cm['thigh_r_x'] - marker['hip_r_x']) * mass['thigh_l'] * g_z +\
           (cm['thigh_r_z'] - marker['hip_r_z']) * mass['thigh_l'] * cm_dd['thigh_r_x'] +\
           (cm['thigh_r_x'] - marker['hip_r_x']) * mass['thigh_l'] * cm_dd['thigh_r_z']

    output.append(- output[13] + temp)

    temp = - (marker['knee_r_x'] - marker['hip_r_x']) * force['knee_r_y'] -\
           (marker['knee_r_y'] - marker['hip_r_y']) * force['knee_r_x'] -\
           (cm['thigh_r_x'] - marker['hip_r_x']) * mass['thigh_l'] * g_y - \
           (cm['thigh_r_y'] - marker['hip_r_y']) * mass['thigh_l'] * g_x + \
           (cm['thigh_r_x'] - marker['hip_r_x']) * mass['thigh_l'] * cm_dd['thigh_r_y'] + \
           (cm['thigh_r_y'] - marker['hip_r_y']) * mass['thigh_l'] * cm_dd['thigh_r_x']

    output.append(- output[14] + temp)

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['ankle_l_x', 'ankle_l_y', 'ankle_l_z',
                                         'knee_l_x', 'knee_l_y', 'knee_l_z',
                                         'hip_l_x', 'hip_l_y', 'hip_l_z',
                                         'ankle_r_x', 'ankle_r_y', 'ankle_r_z',
                                         'knee_r_x', 'knee_r_y', 'knee_r_z',
                                         'hip_r_x', 'hip_r_y', 'hip_r_z'])


#to_do (power)








