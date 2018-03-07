import  Sampler 
import numpy as np 

class GridSampler(Sampler.Sampler):
    '''
    Class for performing grid sampling
    '''

    def __init__(self, param_names, param_ranges):
        super().__init__(param_names, param_ranges)
        return

    
    def sample(self, num_samples):
        '''
        Method which returns a set of samples


        Args:
        ----
        num_samples: The number of samples to return 
        The num_samples should ideally be <num_params>^<num_splits for each parameter>. 
        If it doesn't match that, the value <num_params>^<num_splits> immediately greater
        than the num_samples will be selected and sum samples will be trimmed from the end
        '''
        num_params=len(self.param_names)
         
        # determine the number of  splits for the parameters
        # This could be done in a better way using binary search and doubling
        # but since its a one time thing and mostly we'll be doing less than
        # 10000 parameter samples in a single run (< 2^14 for 2 params) we 
        # can get away with this linear search implementation
        
        num_splits=1
        while(num_params**num_splits < num_samples):
            num_splits+=1
            
        # split each parameter
        # create the split grid 
        param_splits=[]
        
        for i in range(0,num_params):
            param_splits.append(np.linspace(self.param_ranges[i][0], self.param_ranges[i][1], num_splits))
    
        # create a 2d grid for the parameters
        grid=np.meshgrid(*param_splits)
        grid=[x.flatten() for x in grid]
        grid=np.vstack(grid)
        
        # written a list for the parameters
        param_list=[];
        for i in range(0,num_samples):
            param_list.append(list(grid[:,i]))
        return param_list
        



        
        
