import Sampler
import RandomSampler as rs
import numpy as np


class ImportanceSampler(Sampler):
    '''
    Class for performing sampling according to the following algorithm:
    
    1. Generate a set of n points and return
    2. If sampling is called again, build a distribution using the points generated
    previously and sample k points from it. 
    3. For each of the k points sampled, build a gaussian distribution with that point as the
    mean and some predefined variance. Sample a point from this Gaussian distribution.
    4. Return these k points and add them to the distribution.
    5. Some efficiency tweaks:
        a. After every i iterations, introduce p completely random samples into the distribution
        b. After every r iterations, remove q lowest points from the distribution


    --------------------------------------------------
    A typical workflow would be as follows:
    1. Initialize the object
    2. Call sample() 
    3. Run the model on the sampled points
    4. Call update_scores() to update the scores for the sampled points
    5. Repeat steps 2-5 if desired
    
    '''

    def __init__(self, param_names, param_ranges, covar_matrix, random_every=5, random_sample_count=10, remove_every=5,
                 remove_sample_count=5):
        '''
        Constructor

        Args:
        ----
        param_names: A list of parameter names
        param_ranges: A list of parameter valid ranges. Each element of this 
        list must be a tuple of the form (r_beg, r_end) where r_beg and r_end denote
        the minimum and maximum values respectively for the parameter range

        covar_matrix: A covariance matrix of shape (len(parameter_names),len(parameter_names))
        random_every: The number of iterations after which random samples are to be introduced
        random_sample_count= The number of random samples to introduce
        remove_every: Th enumber of iterations after which poor samples are removed
        remove_sample_count: The number of poor samples to remove 
        '''
        super().__init__(param_names, param_ranges)
        self.covar_matrix = covar_matrix
        self.random_every = random_every
        self.random_sample_count = random_sample_count
        self.remove_every = remove_every
        self.remove_sample_count = remove_sample_count

        self.sample_scores = dict()  # dictionary of sample, score
        return

    def sample(self, num_samples):
        '''
        Method to sample num_sample points
        
        Args:
        ----
        num_samples: The number of samples to get

        Return: 
        ----
        A list of num_samples samples
        '''

        # check if we have done sampling before
        if len(self.samples.keys()) == 0:

            # perform random sampling
            sampler = rs.RandomSampler(self.param_names, self.param_ranges)
            points = sampler.sample(num_samples)
            return points

        else:
            # sample by creating a distribution
            dist = _create_dist()

            # sample n points based on the distribution. I'll be sampling the indices of the
            # points here
            points = dist.keys()
            prob = dist.values()
            indices = np.random.choice(np.arange(0, len(points)), num_samples, p=prob)

            new_points = set()  # using set to handle duplicate detection
            low = np.array([x[0] for x in self.param_ranges])
            high = np.array([x[1] for x in self.param_ranges])

            # For each index, create a gaussian with the point at the index as the mean
            # and sample a new point            
            for idx in indices:
                sample = np.random.multivariate_normal(points[idx], self.covar_matrix)
                sample = sample.reshape(-1)  # turn it into a row vector
                # Probably would be computationally efficient if we remove duplicate
                # handling
                while sample in new_points or (all(low <= sample) and all(sample <= high)):
                    sample = np.random.multivariate_normal(points[idx], self.covar_matrix)

                new_points.add(list(sample))
            return new_points
        return

    def update_scores(self, score_dict):
        '''
        Method to update self.sample_scores dictionary

        Args:
        ----
        score_dict: A dictionary with samples as keys and scores as values
        '''
        self.sample_scores.update(score_dict)

    def _create_dist(self):
        '''
        Method to create a distribution based upon the sample scores stored
        
        This method creates the distribution by performing softmax normalization over the scores

        Return:
        ----
        A dictionary with samples as keys and their corresponding probability as the value
        '''

        # The order of the samples and scores will be consistent
        # see: https://stackoverflow.com/questions/835092/python-dictionary-are-keys-and-values-always-the-same-order

        samples = self.sample_scores.keys()
        scores = self.sample_scores.values()
        distr = _softmax(scores)
        dist = dict()
        for i, sample in enumerate(samples):
            dist[sample] = distr[i]
        return dist

    def _softmax(scores):
        '''
        Method to perform softmax normalization over the scores

        Args:
        ----
        scores: The list of scores to normalize

        Return:
        ----
        A list of same size as scores where each element represents the normalized
        value of the corresponding value in scores
        '''
        max_val = np.amax(scores)
        scores = np.array(scores)
        scores = np.exp(scores - max_val)
        return list(scores / np.sum(scores))