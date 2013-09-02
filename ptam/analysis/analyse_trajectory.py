#!/usr/bin/python

import sys
import numpy
import argparse
import associate
import math
import compare_two_trajectories
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc

# config -------------------------------------------------------------------------

trace_name='ptam_i7_rig3'
n_align_frames = 300

img_prefix = '../trace/'+trace_name+'/'+trace_name+'_'
traj_groundtruth = '../trace/'+trace_name+'/traj_groundtruth.txt'
traj_estimate = '../trace/'+trace_name+'/traj_estimate.txt'

#---------------------------------------------------------------------------------

first_list = associate.read_file_list(traj_groundtruth)
second_list = associate.read_file_list(traj_estimate)

matches = associate.associate(first_list, second_list,float(0.0),float(0.02))
if len(matches)<2:
    sys.exit("Couldn't find matching timestamp pairs between groundtruth and estimated trajectory! Did you choose the correct sequence?")

# read data in nupmy matrix
first_xyz = numpy.matrix([[float(value) for value in first_list[a][0:3]] for a,b in matches]).transpose()
second_xyz = numpy.matrix([[float(value) for value in second_list[b][0:3]] for a,b in matches]).transpose()

# align Sim3
scale,rot,trans,trans_error = compare_two_trajectories.alignSim3(first_xyz,second_xyz, n_align_frames)

second_xyz_aligned = scale*rot*second_xyz+trans
alignment_error = second_xyz_aligned - first_xyz
trans_error = numpy.sqrt(numpy.sum(numpy.multiply(alignment_error,alignment_error),0)).A[0]

print 's='+str(scale)
print 'R='+str(rot)
print 't='+str(trans)

first_stamps = first_list.keys()
first_stamps.sort()
first_xyz_full = numpy.matrix([[float(value) for value in first_list[b][0:3]] for b in first_stamps]).transpose()

second_stamps = second_list.keys()
second_stamps.sort()
second_xyz_full = numpy.matrix([[float(value) for value in second_list[b][0:3]] for b in second_stamps]).transpose()
second_xyz_full_aligned = scale*rot*second_xyz_full+trans

# output
rms_error = numpy.sqrt(numpy.dot(trans_error,trans_error) / len(trans_error))
print "compared_pose_pairs %d pairs"%(len(trans_error))
print "absolute_translational_error.rmse %f m"%rms_error
print "absolute_translational_error.mean %f m"%numpy.mean(trans_error)
print "absolute_translational_error.median %f m"%numpy.median(trans_error)
print "absolute_translational_error.std %f m"%numpy.std(trans_error)
print "absolute_translational_error.min %f m"%numpy.min(trans_error)
print "absolute_translational_error.max %f m"%numpy.max(trans_error)

# tell matplotlib to use latex font
rc('font',**{'family':'serif','serif':['Cardo']})
rc('text', usetex=True)

#plot trajectory
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
compare_two_trajectories.plot_traj(ax,first_stamps,first_xyz_full.transpose().A,'-',"red","ground truth")
compare_two_trajectories.plot_traj(ax,second_stamps,second_xyz_full_aligned.transpose().A,'-',"blue","estimated")
compare_two_trajectories.plot_traj(ax,second_stamps[0:n_align_frames],second_xyz_full_aligned[:,0:n_align_frames].transpose().A,'-','green','aligned part', 2.5)
ax.legend()
plt.title('RMS Error = %(time).3fm'%{'time':rms_error})
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
plt.savefig(img_prefix+"trajectory_analysis.pdf", dpi=80)

#plot error
fig = plt.figure(figsize=(8, 3))
ax = fig.add_subplot(111)
ax.plot(trans_error)
ax.legend()
plt.title('Translation error over time')
ax.set_xlabel('Frame Id')
ax.set_ylabel('Error [m]')
plt.savefig(img_prefix+"trajectory_analysis.pdf", dpi=80)



