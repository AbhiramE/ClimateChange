from abc import abstractmethod


class Sampler(object):
    '''
    Base class for all the different sampling methods
    '''

    def __init__(self, param_names, param_ranges):
        '''
        Constructor
        
        Args:
        ----
        param_names:  A list of parameter names
        param_ranges: A list of parameter valid ranges. Each element of this 
        list must be a tuple of the form (r_beg, r_end) where r_beg and r_end denote
        the minimum and maximum values respectively for the parameter range
        '''
        self.param_names = param_names
        self.param_ranges = param_ranges
        super().__init__()
        return

    @abstractmethod
    def sample(self, num_samples):
        '''
        Method which returns a set of samples

        Args:
        ----
        num_samples: The number of samples to return 
        '''
        pass
