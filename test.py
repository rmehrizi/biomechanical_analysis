# Rahil Mehrizi
# Feb 2020

import pandas as pd
import inverse_kinematics as ik
import time_distance as td
import numpy as np
import math
import inverse_dynamics as id
import plots 

# reading data
marker_data=pd.read_csv('marker_data.txt',sep='\t')
fp_data=pd.read_csv('fp_data.txt',sep='\t')
body_mass = 68
height = 1.6

# time distance moduale
events = td.event_detection(fp_data, body_mass)
plots.events_plot(fp_data, 'all', 100)
cad = cadence(events)
print('Cadence average is {0:.2f} steps per minute'.format(cad, 2))
ratio = stance_ratio(events)
print('Swing phase consists {0:0.2f} and {1:.2f} percent of gait cycle for left and right leg, respectively'.format(ratio[0], ratio[1]))

# inverse kinematics moduale
segs = ik.segments(marker_data)
l = ik.length(segs)
angs = ik.angles(segs)
plots.angles_plot(angs)

# inverse dynamics moduale
m = id.mass(body_mass, 1)
com = id.center_of_mass(marker_data, 1)
cm_dd = id.derivative(com, 0.01, 2)
f = id.force(fp_data, m, cm_dd)
plots.forces_plot(f, body_mass)
m = id.moment(fp_data, marker_data, m, com, cm_dd, f)
plots.moments_plot(f, body_mass, height)
