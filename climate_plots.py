import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from IPython import embed

def plot3d(output):
    data = json.load(open(output))
    df = pd.DataFrame(data).astype(float)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = df.calvliq.values
    y = df.cliffvmax.values
    z = df.esl.values
   
    ax.scatter(x, y, z)

    ax.set_xlabel('CALVLIQ')
    ax.set_ylabel('CLIFFVMAX')
    ax.set_zlabel('ESL')

    plt.savefig('final_result.png')   
 
    plt.show()


plot3d('final_result.out')


