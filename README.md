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
Use the following command to run Importance sampling:
```
python3 setup_experiment.py --exp_dir test
```

To run inverse sampling:
```
 python3 inverse_sampling.py --exp_dir test
```

`exp_dir` argument should list a directory name which is inside the code directory (Directory will be created if not present). This argument is optional and if 
its not used a directory by the name of `exp/` will be created in the code directory.


### Description of figures
* heatmap\_small\_inverse\_calvliq.png:
    A heatmap of esl for different values of calvliq.
* heatmap\_small\_inverse\_cliffmax.png:
    A heatmap of esl for different values of cliffmax.
* violin\_calvliq\_converged.png:
    A violin plot of the distribution of the calvliq parameter after convergence.
* violin\_cliffmax\_converged.png:
    A violin plot of the distribution of the cliffmax parameter after convergence.
* calvliq\_esl\_small.png:
    A scatter plot of calvliq vs esl.
* cliffmax\_esl\_small.png:
    A scatter plot of cliffmax vs esl.
* calvliqcliffvmax\_small.png:
    A scatter plot of calvliq vs cliffmax.

