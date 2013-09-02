# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:41:22 2013

@author: cforster
"""


import csv
import numpy as np
import matplotlib.pyplot as plt

# tracefile
trace_name='ptam_i7_rig3'
img_prefix = '../trace/'+trace_name+'/'+trace_name+'_'

data = csv.reader(open('../trace/'+trace_name+'/logs.csv'))
fields = data.next()
D = dict()
for field in fields:
  D[field] = list()

# fill dictionary with column values
for row in data:
  for (field, value) in zip(fields, row):
    D[field].append(float(value))

# change dictionary values from list to numpy array for easier manipulation
for field, value in D.items():
  D[field] = np.array(D[field])

n_frames = np.size(D['t_tot_time']);

# plot timings
plt.figure(1)
plt.boxplot([ D['t_pyramid_creation']*1000,
              D['t_feature_extraction']*1000,
              D['t_feature_sorting']*1000,
              D['t_motion_model']*1000,
              D['t_reproject']*1000,
              D['t_coarse_search']*1000,
              D['t_fine_search']*1000,
              D['t_coarse_optimization']*1000,
              D['t_fine_optimization']*1000,
              D['t_visualization']*1000], vert=0)

boxplot_labels =['pyramid %0.3fms' % np.median(D['t_pyramid_creation']*1000),
                 'fast %0.3fms' % np.median(D['t_feature_extraction']*1000),
                 'feature sort %0.3fms' % np.median(D['t_feature_sorting']*1000),
                 'motion_model %0.3fms' % np.median(D['t_motion_model']*1000),
                 'reproject %0.3fms' % np.median(D['t_reproject']*1000),
                 'coarse search %0.3fms' % np.median(D['t_coarse_search']*1000),
                 'fine search %0.3fms' % np.median(D['t_fine_search']*1000),
                 'coarse opt. %0.3fms' % np.median(D['t_coarse_optimization']*1000),
                 'fine opt. %0.3fms' % np.median(D['t_fine_optimization']*1000),
                 'visalization %0.3fms' % np.median(D['t_visualization']*1000)]

plt.yticks(np.arange(len(boxplot_labels))+1, boxplot_labels)
plt.xlabel('Time [ms]')
plt.savefig(img_prefix+'timing_boxplot.png', bbox_inches="tight")

# plot total time for frame processing
avg_time = np.mean(D['t_tot_time'])*1000;
avg_time_tracking = np.mean(D['t_tot_tracking'])*1000;

plt.figure(2)
plt.plot(np.arange(n_frames), D['t_tot_time']*1000, 'g-', label='total time [ms]')
plt.plot(np.arange(n_frames), D['t_tot_tracking']*1000, 'r-', label='total time tracking [ms]')
plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time, 'g--', label=str('%(time).1fms avg time' % {'time': avg_time}))
plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time_tracking, 'r--', label=str('%(time).1fms avg time tracking' % {'time': avg_time_tracking}))
plt.legend()
plt.title('Total Frame Processing Time')
plt.savefig(img_prefix+'img_tot_processing_time.png', bbox_inches="tight")

plt.figure(3)
plt.boxplot([D['n_pts_l0'], D['n_pts_l1'], D['n_pts_l2'], D['n_pts_l3']], vert=0)
boxplot_labels = ['L0','L1','L2','L3']
plt.yticks(np.arange(len(boxplot_labels))+1, boxplot_labels)
plt.title('Number of tracked points per level')
plt.savefig(img_prefix+'pts_per_level.png', bbox_inches="tight")

plt.figure(4)
tot_tracked_pts = D['n_pts_l0'] + D['n_pts_l1'] + D['n_pts_l2'] + D['n_pts_l3']
plt.plot(np.arange(n_frames), tot_tracked_pts)
plt.title('Totoal number of tracked pts')
plt.savefig(img_prefix+'tot_n_pts.png', bbox_inches="tight")






