# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:41:22 2013

@author: cforster
"""


import csv
import numpy as np
import matplotlib.pyplot as plt

# tracefile
data = csv.reader(open('../trace/ptam_FAST10_0.csv'))
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
plt.figure(7)
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
plt.savefig('timing_boxplot.png', bbox_inches="tight")

# plot total time for frame processing
avg_time = np.mean(D['t_tot_time'])*1000;
avg_time_tracking = np.mean(D['t_tot_tracking'])*1000;

plt.figure(4)
plt.plot(np.arange(n_frames), D['t_tot_time']*1000, 'g-', label='total time [ms]')
plt.plot(np.arange(n_frames), D['t_tot_tracking']*1000, 'r-', label='total time tracking [ms]')
plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time, 'g--', label=str('%(time).1fms avg time' % {'time': avg_time}))
plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time_tracking, 'r--', label=str('%(time).1fms avg time tracking' % {'time': avg_time_tracking}))
plt.legend()
plt.title('Total Frame Processing Time')
plt.savefig('img_tot_processing_time.png', bbox_inches="tight")

#
#
#timings = [ np.median(D['t_pyramid_creation'])*1000,
#            np.median(D['t_feature_extraction'])*1000,
#            np.median(D['t_feature_sorting'])*1000,
#            np.median(D['t_coarse_search'])*1000,
#            np.median(D['t_fine_search'])*1000,
#            np.median(D['t_coarse_optimization'])*1000,
#            np.median(D['t_fine_optimization'])*1000,
#            np.median(D['t_make_keyframe'][np.argwhere(D['t_make_keyframe'] >= 0)])*1000]
#
#timings_pos = np.arange(len(timings))+0.5
#
#timings_labels = [ str('pyramid_creation %(time).1fms ' % {'time': timings[0]}),
#                   str('p3p  %(time).1fms ' % {'time': timings[1]}),
#                   str('reproject  %(time).1fms ' % {'time': timings[2]}),
#                   str('pose optimizer  %(time).1fms ' % {'time': timings[3]}),
#                   str('triangulation  %(time).1fms ' % {'time': timings[4]}),
#                   str('find more obs  %(time).1fms ' % {'time': timings[5]}),
#                   str('make kf  %(time).1fms ' % {'time': timings[6]}),
#                   str('local ba  %(time).1fms ' % {'time': timings[7]}),
#                   str('seed init %.1fms'%timings[8])]
#
#plt.figure(2)
#
#plt.barh(timings_pos, timings, ecolor='r', align='center')
#plt.yticks( timings_pos, timings_labels)
#plt.xlabel('[ms]')
#plt.title('NanoSLAM Timings (' + str(len(is_kf[:,0])) + ' kfs / ' + str(len(is_frame[:,0])) + ' frames)')
#plt.grid(True)
#plt.savefig(trace_name+'_img_timings.png', bbox_inches="tight")
#
## plot total time for frame processing
#avg_time = np.mean(D['t_tot_time'][is_frame])*1000;
#avg_time_kf = np.mean(D['t_tot_time'][is_kf])*1000;
#avg_time_no_kf = np.mean(D['t_tot_time'][is_nokf])*1000;
#
#plt.figure(4)
#plt.plot(np.arange(n_frames), D['t_tot_time'][is_frame]*1000, 'g-', label='total time [ms]')
#plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time, 'b--', label=str('%(time).1fms avg time' % {'time': avg_time}))
#plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time_kf, 'r--', label=str('%(time).1fms avg time keyframe' % {'time': avg_time_kf}))
#plt.plot(np.arange(n_frames), np.ones(n_frames)*avg_time_no_kf, 'm--', label=str('%(time).1fms avg time no keyframe' % {'time': avg_time_no_kf}))
#plt.plot(is_kf-is_frame[1], D['t_tot_time'][is_kf]*1000, 'r.')
#plt.legend()
#plt.title('Total Frame Processing Time')
#plt.savefig(trace_name+'_img_tot_processing_time.png', bbox_inches="tight")
#
# 
#plt.figure(6)
#plt.plot(D['sfba_n_edges_init'], D['t_local_ba']*1000, '.')
#plt.ylabel('time [ms]'), plt.xlabel('number of p')
#plt.title('number of points vs ba time')
#
#plt.figure(7)
#plt.boxplot([ D['t_klt'][is_frame]*1000,
#              D['t_reproject'][is_frame]*1000,
#              D['t_pose_optimizer'][is_frame]*1000,
#              D['t_local_ba'][is_kf]*1000,
#              D['t_seed_init'][is_kf]*1000 ], vert=0)
#boxplot_labels =['klt','reproject','pose optimizer', 'local ba', 'seed init']
#plt.yticks(np.arange(len(boxplot_labels))+1, boxplot_labels)
#plt.xlabel('Time [ms]')
#plt.savefig(trace_name+'_timing_boxplot.png', bbox_inches="tight")
#
#
#
#
