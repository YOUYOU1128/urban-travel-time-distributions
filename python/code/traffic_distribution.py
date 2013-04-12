'''
Created on Mar 20, 2013

@author: audehofleitner
'''
import numpy as np
from scipy.stats import norm
from sklearn.utils.extmath import logsumexp

class traffic_distribution:
    
    def __init__(self, components):
        self.components = components
        self.n_components = len(components)
        self.weights = np.array([c.weight for c in components])
        self.ff_tt_dist = components[0].ff_tt_dist
        
    def log_pdf(self, x, nargout=1):
        lpr = np.empty((len(x), self.n_components))
        for i, c in enumerate(self.components):
            lpr[:, i] = c.log_pdf(x) + np.log(c.weight)
        logprob = logsumexp(lpr, axis=1)
        if nargout > 1:
            component_posterior = np.exp(lpr - logprob[:, np.newaxis])
            return logprob, component_posterior
        return logprob
        
        
class traffic_component:
    def __init__(self, weight, ff_tt_dist, mass_param=0.0, unif_param=None):
        assert (mass_param is None) ^ (unif_param is None)
        if mass_param is None:
            assert unif_param[1] - unif_param[0] > - 0.01
        if mass_param is None and abs(unif_param[1] - unif_param[0]) < 0.01:
            mass_param =  (unif_param[1] + unif_param[0]) / 2
            unif_param = None
        self.uniform = mass_param is None
        self.unif_param = unif_param
        self.mass_param = mass_param
        self.ff_tt_dist = ff_tt_dist
        self.weight = weight
        
    def log_pdf(self, x):
        if self.uniform:
            return self.log_pdf_uniform(x)
        return np.log(self.pdf_mass(x))
    
    def pdf(self, x):
        if self.uniform:
            return self.pdf_uniform(x)
        return self.pdf_mass(x)
        
    def log_pdf_mass(self, x):
        return self.ff_tt_dist.logpdf(x)
    
    def pdf_mass(self, x):
        return self.ff_tt_dist.pdf(x)
    
    def log_pdf_uniform(self, x):
        cdf_val_min = self.ff_tt_dist.cdf(x - self.unif_param[1])
        cdf_val_max = self.ff_tt_dist.cdf(x - self.unif_param[0])
        diff = cdf_val_max - cdf_val_min
        diff[diff < 1e-6] = 1e-6
        return (np.log(diff) -
                np.log(self.unif_param[1] - self.unif_param[0]))
        
    def pdf_uniform(self, x):
        return np.exp(self.log_pdf_uniform(x))
        
