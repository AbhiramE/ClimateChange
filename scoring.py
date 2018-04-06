import numpy as np
from scipy.stats import norm


def binary_score(esl_values, desired_range):
    '''Method to generate a binary score for ESL values
    
    
    Args:
    ----

    esl_values: A list / array of ESL values

    desired_range: Range in which the ESL value gets a score of 1
    
    Returns:
    ----

    An array x of same shape as esl_values where x[i] denotes the
    score of esl_values[i]

    '''
    scores = np.array(esl_values)
    scores[scores < desired_range[0] or scores > desired_range[1]] = 0
    scores[scores >= desired_range[0] and scores <= desired_range[1]] = 1
    return scores


def gaussian_score(esl_values, mean=0.00038, sigma=0.00008):
    '''
    Method to calculate the gaussian score of esl values
    
    Args:
    ----
    
    esl_values: A list / array of ESL values

    mean: The mean for the normal distribution

    sigma: The standard deviation for the normal distribution

    Returns:
    ----

    An array x of same shape as esl_values where x[i] denotes the
    score of esl_values[i]
    '''
    scores = np.array(esl_values)
    return norm.pdf(scores, mean, sigma)
