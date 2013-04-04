'''
Created on Mar 20, 2013

@author: audehofleitner
'''
import numpy as np
from scipy.stats import gamma

class traffic_distribution:
    def __init__(self, nb_components):
        self.nb_components = nb_components
        self.unif_param = None
        self.gamma_dist = None
        self.weights = None
        
    def log_probabilities(self, x):
        
        
class traffic_component:
    def __init__(self, unif_param, gamma_dist):
        self.unif_param = unif_param
        self.gamma_dist = gamma_dist
        
    def log_probabilities(self, x):
        
        
        
    
