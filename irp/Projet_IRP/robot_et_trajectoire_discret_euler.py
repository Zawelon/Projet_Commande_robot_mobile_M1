# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 01:31:09 2024

@author: Thomas Ets
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

################
#Paramètre initial
v = 4
angle_initiale = np.radians(0)
omega = 4
pos_init = np.array([0,0])
###########


#temps
delta_d = 0.01
delta_t = delta_d
d_final = 9
temps = np.arange(0, (d_final+delta_d)/v, delta_t)
distance = temps * v
#print(distance)

#Initialisation
x = np.zeros_like(temps)
y = np.zeros_like(temps)
theta = np.zeros_like(temps)

#Conditions initiales
x[0] = pos_init[0]
y[0] = pos_init[1]
theta[0] = angle_initiale


#méthode Euler
for i in range(1, len(temps)):
    x[i] = x[i-1] + delta_t * v *np.cos(theta[i-1])
    y[i] = y[i-1] + delta_t * v* np.sin(theta[i-1])
    theta[i] = theta[i-1] + delta_t * omega

fig,ax = plt.subplots(figsize=(8,8))
#ax.plot(x, y,label="trajectoire")
plt.title('Trajectoire du mouvement')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

#Ajout d'annotations
annotation_v = f'Vitesse: {v} m/s'
ax.text(0.05, 1, f'Pos_init_robot: {(x[0],y[0])}', transform=ax.transAxes, fontsize=10, color='black')
ax.text(0.05, 0.95, annotation_v, transform=ax.transAxes, fontsize=10, color='black')
annotation_theta = ax.text(0.05, 0.9,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_t = ax.text(0.05, 0.85,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_d = ax.text(0.05, 0.8,'', transform=ax.transAxes, fontsize=10, color='black')

trajectoire, = ax.plot(x,y,label="trajectoire")
robot, = ax.plot([],[],'ro',markersize=20,label="robot")

#animation
def animate(i):
    trajectoire.set_data([x[:i]], [y[:i]])
    robot.set_data([x[i]], [y[i]])
    annotation_t.set_text(f'Temps: {round(temps[i],2)} s')
    annotation_d.set_text(f'Distance parcouru: {round(distance[i],2)} m')
    annotation_theta.set_text(f'theta: {round(theta[i],2)} rad = {round(np.degrees(theta[i]),2)} deg')
    return [trajectoire,robot,annotation_t,annotation_d,annotation_theta]

Anima = animation.FuncAnimation(fig, animate, frames=range(len(temps)), interval=delta_t * 1000, blit=True)

ax.legend()
plt.show()
