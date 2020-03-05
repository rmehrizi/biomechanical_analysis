# Rahil Mehrizi
# Jan 2020
# A module for performing inverse kinematics on marker data

import pandas as pd
import numpy as np


def segments(marker_data):
    
    """Returns the 3d orientation of each body segment
     
    Methods
    ==========
    Each body segment is a 3d vector, which is defined by calculating the difference between proximal and distal marker
    coordinates.
    torso(x,y,z) = neck(x,y,z) - hip_center(x,y,z)
    thigh_l(x,y,z) = hip_l(x,y,z) - knee_l(x,y,z)
    shank_l(x,y,z) = knee_l(x,y,z) - ankle_l(x,y,z)
    foot_l(x,y,z) = ankle_l(x,y,z) - toe_l(x,y,z)
    thigh_r(x,y,z) = hip_r(x,y,z) - knee_r(x,y,z)
    shank_r(x,y,z) = knee_r(x,y,z) - ankle_r(x,y,z)
    foot_r(x,y,z) = ankle_r(x,y,z) - toe_r(x,y,z)
     
    Parameters
    ==========
        marker_data : dataframe
            A dataframe with 27 columns including 3d coordinates of 9 joints
            
    Returns
    =======
        A dataframe with 18 columns including 3d orientations of 6 body segments
    """
    
    output = []
    output.append((marker_data['neck_x'] - 0.5 * (marker_data['hip_l_x'] + marker_data['hip_r_x'])).to_list())
    output.append((marker_data['neck_y'] - 0.5 * (marker_data['hip_l_y'] + marker_data['hip_r_y'])).to_list())
    output.append((marker_data['neck_z'] - 0.5 * (marker_data['hip_l_z'] + marker_data['hip_r_z'])).to_list())
    output.append((marker_data['hip_l_x'] - marker_data['knee_l_x']).to_list())
    output.append((marker_data['hip_l_y'] - marker_data['knee_l_y']).to_list())
    output.append((marker_data['hip_l_z'] - marker_data['knee_l_z']).to_list())
    output.append((marker_data['knee_l_x'] - marker_data['ankle_l_x']).to_list())
    output.append((marker_data['knee_l_y'] - marker_data['ankle_l_y']).to_list())
    output.append((marker_data['knee_l_z'] - marker_data['ankle_l_z']).to_list())
    output.append((marker_data['ankle_l_x'] - marker_data['toe2_l_x']).to_list())
    output.append((marker_data['ankle_l_y'] - marker_data['toe2_l_y']).to_list())
    output.append((marker_data['ankle_l_z'] - marker_data['toe2_l_z']).to_list())
    output.append((marker_data['hip_r_x'] - marker_data['knee_r_x']).to_list())
    output.append((marker_data['hip_r_y'] - marker_data['knee_r_y']).to_list())
    output.append((marker_data['hip_r_z'] - marker_data['knee_r_z']).to_list())
    output.append((marker_data['knee_r_x'] - marker_data['ankle_r_x']).to_list())
    output.append((marker_data['knee_r_y'] - marker_data['ankle_r_y']).to_list())
    output.append((marker_data['knee_r_z'] - marker_data['ankle_r_z']).to_list())
    output.append((marker_data['ankle_r_x'] - marker_data['toe2_r_x']).to_list())
    output.append((marker_data['ankle_r_y'] - marker_data['toe2_r_y']).to_list())
    output.append((marker_data['ankle_r_z'] - marker_data['toe2_r_z']).to_list())

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['torso_x', 'torso_y', 'torso_z', 'thigh_l_x', 'thigh_l_y', 'thigh_l_z',
                                         'shank_l_x', 'shank_l_y', 'shank_l_z', 'foot_l_x', 'foot_l_y', 'foot_l_z',
                                         'thigh_r_x', 'thigh_r_y', 'thigh_r_z', 'shank_r_x', 'shank_r_y', 'shank_r_z',
                                         'foot_r_x', 'foot_r_y', 'foot_r_z'])


def length(seg):
    
    """Returns the length of each body segment
     
    Methods
    ==========
    The segment length is defined as the Euclidean distance between the proximal and distal joints.
     
    Parameters
    ==========
    seg : dataframe
        A dataframe with 18 columns including 3d orientations of 6 body segments (output of "segment" function)
                 
    Returns
    =======
        the length of each body segment in the same unit of marker data
    """
    
    output = []
    output.append((seg['torso_x'] ** 2 + seg['torso_y'] ** 2 + seg['torso_z'] ** 2) ** 0.5)
    output.append((seg['thigh_l_x'] ** 2 + seg['thigh_l_y'] ** 2 + seg['thigh_l_z'] ** 2) ** 0.5)
    output.append((seg['shank_l_x'] ** 2 + seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2) ** 0.5)
    output.append((seg['foot_l_x'] ** 2 + seg['foot_l_y'] ** 2 + seg['foot_l_z'] ** 2) ** 0.5)
    output.append((seg['thigh_r_x'] ** 2 + seg['thigh_r_y'] ** 2 + seg['thigh_r_z'] ** 2) ** 0.5)
    output.append((seg['shank_r_x'] ** 2 + seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2) ** 0.5)
    output.append((seg['foot_r_x'] ** 2 + seg['foot_r_y'] ** 2 + seg['foot_r_z'] ** 2) ** 0.5)

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['torso', 'thigh_l', 'shank_l', 'foot_l', 'thigh_r', 'shank_r', 'foot_r'])


def angles(seg):
    
    """Returns joint angles
     
    Methods
    ==========
    The joint angle is calculated using the dot product and magnitude of the segment orientation that intersect at that
    joint sign convention for angles: hip flexion, hip abduction, knee flexion, ankle plantarflexion are positive.
     
    Parameters
    ==========
    seg : dataframe
        A dataframe with 18 columns including 3d orientations of 6 body segments (output of "segment" function)
                 
    Returns
    =======
    A dataframe with 8 columns:
        hip_l_flex_ext : left hip flexion/extension in degree
        hip_l_abd_add : left hip abduction/adduction in degree
        knee_l_flex_ext : left knee flexion/extension in degree
        ankle_l_dors_plan : left ankle plantar-flexion/Dorsiflexion in degree
        hip_r_flex_ext : right hip flexion/extension in degree
        hip_r_abd_add : right hip abduction/adduction in degree
        knee_r_flex_ext : right knee flexion/extension in degree
        ankle_r_dors_plan : right ankle plantar-flexion/Dorsiflexion in degree
   
    """
    
    output = []
    output.append(np.arccos((seg['torso_y'] * seg['thigh_l_y'] + seg['torso_z'] * seg['thigh_l_z']) /
                 ((seg['torso_y'] ** 2 + seg['torso_z'] ** 2)**0.5 *
                 (seg['thigh_l_y'] ** 2 + seg['thigh_l_z'] ** 2 ) ** 0.5)) *
                 (180 / np.pi) * (-np.sign(seg['thigh_l_z'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['thigh_l_y'] + seg['torso_x'] * seg['thigh_l_x']) /
                 ((seg['torso_y'] ** 2 + seg['torso_x'] ** 2) ** 0.5 *
                 (seg['thigh_l_y'] ** 2 + seg['thigh_l_x'] ** 2) ** 0.5)) *
                 (180 / np.pi) * (np.sign(seg['thigh_l_x'])).to_list())

    output.append(np.arccos((seg['thigh_l_y'] * seg['shank_l_y'] + seg['thigh_l_z'] * seg['shank_l_z']) /
                 ((seg['thigh_l_y'] ** 2 + seg['thigh_l_z'] ** 2)**0.5 *
                 (seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2 ) ** 0.5)) * \
                 (180 / np.pi) * (np.sign(seg['shank_l_z'])).to_list())

    output.append((np.arccos((seg['shank_l_y'] * seg['foot_l_y'] + seg['shank_l_z'] * seg['foot_l_z']) /
                 ((seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2) ** 0.5 *
                 (seg['foot_l_y'] ** 2 + seg['foot_l_z'] ** 2) ** 0.5)) - np.pi/2) * \
                 (180 / np.pi) * (np.sign(seg['foot_l_y'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['thigh_r_y'] + seg['torso_z'] * seg['thigh_r_z']) /
                 ((seg['torso_y']**2 + seg['torso_z']**2)**0.5 *
                 (seg['thigh_r_y']**2 + seg['thigh_r_z']**2)**0.5)) * \
                 (180 / np.pi) * (-np.sign(seg['thigh_r_z'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['thigh_r_y'] + seg['torso_x'] * seg['thigh_r_x']) /
                 ((seg['torso_y'] ** 2 + seg['torso_x'] ** 2) ** 0.5 *
                 (seg['thigh_r_y'] ** 2 + seg['thigh_r_x'] ** 2) ** 0.5)) *
                 (180 / np.pi) * (-np.sign(seg['thigh_r_x'])).to_list())

    output.append(np.arccos((seg['thigh_r_y'] * seg['shank_r_y'] + seg['thigh_r_z'] * seg['shank_r_z']) /
                 ((seg['thigh_r_y'] ** 2 + seg['thigh_r_z'] ** 2)**0.5 *
                 (seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2 ) ** 0.5)) * \
                 (180 / np.pi) * (np.sign(seg['shank_r_z'])).to_list())

    output.append((np.arccos((seg['shank_r_y'] * seg['foot_r_y'] + seg['shank_r_z'] * seg['foot_r_z']) /
                 ((seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2) ** 0.5 *
                 (seg['foot_r_y'] ** 2 + seg['foot_r_z'] ** 2) ** 0.5)) - np.pi/2) * \
                 (180 / np.pi) * (np.sign(seg['foot_r_y'])).to_list())

    output = [list(i) for i in zip(*output)]

    return pd.DataFrame(output, columns=['hip_l_flex_ext', 'hip_l_abd_add', 'knee_l_flex_ext', 'ankle_l_plan_dors',
                                         'hip_r_flex_ext', 'hip_r_abd_add', 'knee_r_flex_ext', 'ankle_r_plan_dors'])





