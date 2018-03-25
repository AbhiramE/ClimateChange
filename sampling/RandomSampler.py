from . import Sampler
import numpy as np


class RandomSampler(Sampler.Sampler):
    '''
    Class for performing random sampling
    '''

    def __init__(self, param_names, param_ranges):
        '''Constructor

        Args: ---- param_names: A list of parameter names
        param_ranges: A list of parameter valid ranges. Each element
        of this list must be a tuple of the form (r_beg, r_end) where
        r_beg and r_end denote the minimum and maximum values
        respectively for the parameter range

        '''

        super().__init__(param_names, param_ranges)
        return

    def sample(self, num_samples):
        '''Constructor

        This method assumes a uniform distribution over the parameter
        space. The samples generated are unique.
        Args:
        ----
        num_samples: The number of samples to retrieve

        '''

        result = list()
        low = [x[0] for x in self.param_ranges]
        high = [x[1] for x in self.param_ranges]

        while len(result) < num_samples:
            rand = np.random.uniform(
                low,
                high,
                size=(num_samples - len(result), len(self.param_ranges)))
            rand = np.unique(rand, axis=0)
            for i in range(0, rand.shape[0]):
                result.append(list(rand[i]))

        return result
