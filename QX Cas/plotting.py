
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
import numpy as np
import sys

#%%

file_positions_A = pd.read_csv("apositions"+sys.argv[1]+".csv", sep=';')
file_positions_B = pd.read_csv("bpositions"+sys.argv[1]+".csv", sep=';')
file_positions_C = pd.read_csv("cpositions"+sys.argv[1]+".csv", sep=';')

t = range(0, len(file_positions_A.x))

xA, yA, zA = file_positions_A.x, file_positions_A.y,file_positions_A.z
xB, yB, zB = file_positions_B.x, file_positions_B.y,file_positions_B.z
xC, yC, zC = file_positions_C.x, file_positions_C.y,file_positions_C.z

dataSetA = np.array([xA, yA, zA])
dataSetB = np.array([xB, yB, zB])
dataSetC = np.array([xC, yC, zC])
numDataPoints = len(t)

def animate_func(num):
    x = 5 #x as speed multiplier
    num =  num*x
   
    if num < len(file_positions_A.x):
        ax.clear()  
    
        ax.plot3D(dataSetA[0, :num+1], dataSetA[1, :num+1],dataSetA[2, :num+1], c='red', label='A')
        ax.plot3D(dataSetB[0, :num+1], dataSetB[1, :num+1],dataSetB[2, :num+1], c='green', label='B')
        ax.plot3D(dataSetC[0, :num+1], dataSetC[1, :num+1],dataSetC[2, :num+1], c='blue', label='C')
        # Updating Point Location 
        ax.scatter(dataSetA[0, num], dataSetA[1, num], dataSetA[2, num],c='red', marker='o',label='A')
        ax.scatter(dataSetB[0, num], dataSetB[1, num], dataSetB[2, num],c='green', marker='o',label='B')
        ax.scatter(dataSetC[0, num], dataSetC[1, num], dataSetC[2, num],c='blue', marker='o',label='C')
        # Adding Constant Origin
        ax.plot3D(dataSetA[0, 0], dataSetA[1, 0], dataSetA[2, 0],c='black', marker='o',label='A_s')
        ax.plot3D(dataSetB[0, 0], dataSetB[1, 0], dataSetB[2, 0],c='black', marker='o',label='B_s')
        ax.plot3D(dataSetC[0, 0], dataSetC[1, 0], dataSetC[2, 0],c='black', marker='o',label='C_s')


    # Adding Figure Labels
    ax.set_title('Trajectory - ' + sys.argv[1]+ '\nTime = ' + str(np.round(t[num],    
                 decimals=2)) + ' sec')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

tickrate=5

fig = plt.figure()

ax = plt.axes(projection='3d')
line_ani = FuncAnimation(fig, animate_func, interval=1, frames=int(numDataPoints/tickrate))
plt.legend()
plt.show()
# Saving the Animation
f = r"animation.gif"
writergif = PillowWriter(fps=20)
line_ani.save(f, writer=writergif, dpi=300)
##
##ax.plot3D(file_positions_A.x, file_positions_A.y,file_positions_A.z)
##ax.plot3D(file_positions_B.x, file_positions_B.y,file_positions_B.z)
##ax.plot3D(file_positions_C.x, file_positions_C.y,file_positions_C.z)
##
##
##
### %%
##plt.plot(file_positions_A.x,file_positions_A.y, '-o', markersize='1')
##plt.plot(file_positions_B.x,file_positions_B.y, '-o', markersize='1')
##plt.title(sys.argv[1])
##plt.plot(file_positions_C.x,file_positions_C.y, '-o', markersize='1')
##plt.xlabel('x')
##plt.ylabel('y')
##plt.show()
##
##plt.plot(file_positions_A.z,file_positions_A.x, '-o', markersize='1')
##plt.plot(file_positions_B.z,file_positions_B.x, '-o', markersize='1')
##plt.plot(file_positions_C.z,file_positions_C.x, '-o', markersize='1')
##plt.xlabel('z')
##plt.ylabel('x')
##plt.show()
##
##plt.plot(file_positions_A.y,file_positions_A.z, '-o', markersize='1')
##plt.plot(file_positions_B.y,file_positions_B.z, '-o', markersize='1')
##plt.plot(file_positions_C.y,file_positions_C.z, '-o', markersize='1')
##plt.xlabel('y')
##plt.ylabel('z')
##plt.show()
### # %%
##plt.plot(file_positions_A.x, '-o')
##plt.plot(file_positions_B.x, '-o')
##plt.plot(file_positions_C.x, '-o')
##plt.xlabel('time')
##plt.ylabel('x')
##plt.show()

# %%
