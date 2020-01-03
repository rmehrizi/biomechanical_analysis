import pandas as pd
import numpy as np

def segments(marker_data):
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
    return pd.DataFrame(output, columns=['torso_x', 'torso_y', 'torso_z', 'tigh_l_x', 'tigh_l_y', 'tigh_l_z',
                                         'shank_l_x', 'shank_l_y', 'shank_l_z', 'foot_l_x', 'foot_l_y', 'foot_l_z',
                                         'tigh_r_x', 'tigh_r_y', 'tigh_r_z', 'shank_r_x', 'shank_r_y', 'shank_r_z',
                                         'foot_r_x', 'foot_r_y', 'foot_r_z'])

def length(seg):
    output = []
    output.append((seg['torso_x'] ** 2 + seg['torso_y'] ** 2 + seg['torso_z'] ** 2) ** 0.5)
    output.append((seg['tigh_l_x'] ** 2 + seg['tigh_l_y'] ** 2 + seg['tigh_l_z'] ** 2) ** 0.5)
    output.append((seg['shank_l_x'] ** 2 + seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2) ** 0.5)
    output.append((seg['foot_l_x'] ** 2 + seg['foot_l_y'] ** 2 + seg['foot_l_z'] ** 2) ** 0.5)
    output.append((seg['tigh_r_x'] ** 2 + seg['tigh_r_y'] ** 2 + seg['tigh_r_z'] ** 2) ** 0.5)
    output.append((seg['shank_r_x'] ** 2 + seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2) ** 0.5)
    output.append((seg['foot_r_x'] ** 2 + seg['foot_r_y'] ** 2 + seg['foot_r_z'] ** 2) ** 0.5)

    output = [list(i) for i in zip(*output)]
    return pd.DataFrame(output, columns=['torso', 'tigh_l', 'shank_l', 'foot_l', 'tigh_r', 'shank_r', 'foot_r'])

def angles(seg):
    output = []
    output.append(np.arccos((seg['torso_y'] * seg['tigh_l_y'] + seg['torso_z'] * seg['tigh_l_z']) /
                 ((seg['torso_y'] ** 2 + seg['torso_z'] ** 2)**0.5 *
                 (seg['tigh_l_y'] ** 2 + seg['tigh_l_z'] ** 2 ) ** 0.5)) *
                 (180 / np.pi) * (-np.sign(seg['tigh_l_z'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['tigh_l_y'] + seg['torso_x'] * seg['tigh_l_x']) /
                 ((seg['torso_y'] ** 2 + seg['torso_x'] ** 2) ** 0.5 *
                 (seg['tigh_l_y'] ** 2 + seg['tigh_l_x'] ** 2) ** 0.5)) *
                 (180 / np.pi) * (np.sign(seg['tigh_l_x'])).to_list())

    output.append(np.arccos((seg['tigh_l_y'] * seg['shank_l_y'] + seg['tigh_l_z'] * seg['shank_l_z']) /
                 ((seg['tigh_l_y'] ** 2 + seg['tigh_l_z'] ** 2)**0.5 *
                 (seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2 ) ** 0.5)) * \
                 (180 / np.pi) * (-np.sign(seg['shank_l_z'])).to_list())

    output.append((np.arccos((seg['shank_l_y'] * seg['foot_l_y'] + seg['shank_l_z'] * seg['foot_l_z']) /
                 ((seg['shank_l_y'] ** 2 + seg['shank_l_z'] ** 2) ** 0.5 *
                 (seg['foot_l_y'] ** 2 + seg['foot_l_z'] ** 2) ** 0.5)) - np.pi/2) * \
                 (180 / np.pi) * (-np.sign(seg['foot_l_y'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['tigh_r_y'] + seg['torso_z'] * seg['tigh_r_z']) /
                 ((seg['torso_y']**2 + seg['torso_z']**2)**0.5 *
                 (seg['tigh_r_y']**2 + seg['tigh_r_z']**2)**0.5)) * \
                 (180 / np.pi) * (-np.sign(seg['tigh_r_z'])).to_list())

    output.append(np.arccos((seg['torso_y'] * seg['tigh_r_y'] + seg['torso_x'] * seg['tigh_r_x']) /
                 ((seg['torso_y'] ** 2 + seg['torso_x'] ** 2) ** 0.5 *
                 (seg['tigh_r_y'] ** 2 + seg['tigh_r_x'] ** 2) ** 0.5)) *
                 (180 / np.pi) * (-np.sign(seg['tigh_r_x'])).to_list())

    output.append(np.arccos((seg['tigh_r_y'] * seg['shank_r_y'] + seg['tigh_r_z'] * seg['shank_r_z']) /
                 ((seg['tigh_r_y'] ** 2 + seg['tigh_r_z'] ** 2)**0.5 *
                 (seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2 ) ** 0.5)) * \
                 (180 / np.pi) * (-np.sign(seg['shank_r_z'])).to_list())

    output.append((np.arccos((seg['shank_r_y'] * seg['foot_r_y'] + seg['shank_r_z'] * seg['foot_r_z']) /
                 ((seg['shank_r_y'] ** 2 + seg['shank_r_z'] ** 2) ** 0.5 *
                 (seg['foot_r_y'] ** 2 + seg['foot_r_z'] ** 2) ** 0.5)) - np.pi/2) * \
                 (180 / np.pi) * (-np.sign(seg['foot_r_y'])).to_list())

    output = [list(i) for i in zip(*output)]

    return pd.DataFrame(output, columns=['hip_l_flex_ext', 'hip_l_abd_add', 'knee_l_flex_ext', 'ankle_l_dors_plan',
                                         'hip_r_flex_ext', 'hip_r_abd_add', 'knee_r_flex_ext', 'ankle_r_dors_plan'])





