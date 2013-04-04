'''
Created on Mar 8, 2013

@author: audehofleitner
'''

import pandas as pd
from pandas import DataFrame, Series
import os

FIELDS = (['veh_id', 'frame_id', 'epoch_time', 'local_x', 'local_y',
                     'veh_vel', 'lane_id', 'o_zone', 'd_zone', 'intersection',
                     'section', 'direction', 'mvmt'])

def get_data(direction, network='Peachtree', time='0400pm-0415pm'):
    """
    direction: 2 - north-bound (NB) or 4 - south-bound (SB)
    network: Peachtree
    time: 0400pm-0415pm
    """
    fname = '{0}/NGSIM/{1}/vehicle-trajectory-data/{2}/trajectories-{2}.csv'.format(data_dir(), network, time)
    data = pd.read_csv(fname)
    data = data[FIELDS]
    data = data[data['mvmt'] == 1]
    data = data[data['direction'] == direction]
    data['time'] = (data['epoch_time'] - data['epoch_time'].min()) / 1000.0
    data['local_y'] = data['local_y'] / 0.3048
    data['local_x'] = data['local_x'] / 0.3048
    return data

def get_travel_times(df):
    df = df[df['section'] != 0]
    g = df['time'].groupby([df['veh_id'], df['section']])
    res = DataFrame([g.max() - g.min(), g.min()]).T
    res.columns = ['tt', 'time']
    res = res.reset_index()
    return res

def data_dir():
    """ Directory that contains the local data.

    The default value is overriden if the environment variable
    MM_DATA_DIR is defined. In this case, the value of this variable
    is returned instead.
    """
    if 'MM_DATA_DIR' in os.environ:
        return os.environ['MM_DATA_DIR']
    raise Exception('Check that the environment variable MM_DATA_DIR is setup')
