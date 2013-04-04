'''
Created on Mar 8, 2013

@author: audehofleitner
'''

import matplotlib.pyplot as plt
import matplotlib
import io as io


def plot_trajectories(data):
    x = data['time']
    y = data['local_y']
    z = data['veh_vel']
    cm = matplotlib.cm.get_cmap('gray')
    p = plt.scatter(x, y, c=z, marker='.', edgecolor='none', cmap=cm)
    plt.colorbar(p)
    plt.xlabel('Time (s)')
    plt.ylabel('Offset (m)')
    
def plot_tt_ts(data):
    tt = io.get_travel_times(data)
    tt = tt.sort_index(by='time')
    sections = tt['section'].unique()
    plt.figure()
    n = (len(sections) + 1) / 2
    for s in sections:
        sec_tt = tt[tt['section'] == s]
        plt.subplot(n, 2, s)
        plt.plot(sec_tt['time'], sec_tt['tt'])
        plt.title('Section {0}'.format(s))
    plt.show()        
        
d = io.get_data(2)
plot_tt_ts(d)
