'''
Created on Apr 10, 2013

@author: audehofleitner
'''

import traffic_distribution as td
import numpy as np
from scipy.stats import norm
import scipy.optimize as opt



def fit_traffic_distribution(tt, n_component):
    tt.sort()
    mean = slice(tt[0], tt[0] + 10, 2.0)
    std = slice(2, 10, 2.0)
    eta = [slice(.1, .7, .1)] * (n_component - 1)
    delays = [slice(30, 60, 10)]
    for _ in range(1, n_component - 1):
        delays.append(slice(max(5, delays[-1].start - 5),
                            max(5, delays[-1].stop - 5),
                            delays[-1].step))
    
    ranges = (mean, std) + tuple(eta) + tuple(delays)
    (x0, fval, grid, Jout) = opt.brute(func=obj_fun, ranges=ranges, args=[tt], full_output=True)
    return x0, fval, grid, Jout
    

def obj_fun(param, *args):
    """ Opposite of the log-likelihood
    param: parameters of the distribution
    args: tuple with the travel time observations
    """
    tt = args[0]
    n_component = 1 + (len(param) - 2) / 2
    m, s = param[0], param[1]
    eta = param[2: 2 + n_component - 1]
    eta = [max(e, 0.01) for e in eta]
    if sum(eta) > .9:
        eta[1:] = [(1 - (eta[0] + 0.1)) / (len(eta) - 1)] * (len(eta) - 1)
    delays = np.concatenate((param[2 + n_component - 1:], [0]))
    for i in range(1, len(delays)):
        delays[i] = max(min(delays[i - 1] - 5, delays[i]), 0)
    ff_tt_dist = norm(m, s)
    components = [td.traffic_component(1-sum(eta),
                                       ff_tt_dist,
                                       mass_param=0.0,
                                       unif_param=None)]
    
    for i in range(len(eta)):
        components.append(td.traffic_component(eta[i],
                                               ff_tt_dist,
                                               mass_param=None,
                                               unif_param=[delays[i + 1], delays[i]]
                                               ))
        
    tt_dist = td.traffic_distribution(components)
    return - np.mean(tt_dist.log_pdf(tt, nargout=1))
        
tt = [ 40. ,  18.9 , 53.4 , 14.3 , 11. ,  12.3 , 14.4 , 14.4 , 12.8 , 14.7 ,  8.1 , 16.2, 55.3,  21.1,  44. ]    
(x0, fval, grid, Jout) = fit_traffic_distribution(tt, 3)
print x0
import matplotlib.pyplot as plt
        