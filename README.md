# Parameter sampling for climate change models
## Authors
- Abhay Mittal (abhaymittal@cs.umass.edu)
- Abhiram Eswaran (aeswaran@cs.umass.edu)
- Ryan Mckenna (rmckenna@cs.umass.edu)

## Advisors
- J. Eliot B. Moss (moss@cs.umass.edu)
- Rob Deconto (deconto@geo.umass.edu)

### Installation
- Clone the repository
- Place comicegrid.h, crhmelfilein,  and restartin into the bootstrap directory


### Steps to run
Use the following command to run:
```
python3 setup_experiment.py --exp_dir test
```

To run inverse sampling:
```
 python3 inverse_sampling.py --exp_dir test
```

`exp_dir` argument should list a directory name which is inside the code directory (Directory will be created if not present). This argument is optional and if 
its not used a directory by the name of `exp/` will be created in the code directory.
