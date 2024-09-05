import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Timer
from math import*

################################
#Paramètre initial
################################

v = 5
angle_initiale = np.radians(-90)
omega = 0
pos_init = np.array([-1,0])


###########
#Init para Robot Bleu
v2=5
angle_initiale2 = np.radians(90)
w2 = 0
pos_init2 = np.array([-1,0])

####
#Faire varier a et am
a=4
am=2
k2=a*a
k3=2*am*a
##############

#temps
delta_d = 0.01
delta_t = delta_d
d_final = 50
temps = np.arange(0, (d_final+delta_d)/v, delta_t)
distance = temps * v


#Initialisation
x = np.zeros_like(temps)
y = np.zeros_like(temps)
theta = np.zeros_like(temps)


#Init Robot Bleu
x2 = np.zeros_like(temps)
y2 = np.zeros_like(temps)
theta2 = np.zeros_like(temps)
thetae = np.zeros_like(temps)
l = np.zeros_like(temps)
s = np.zeros_like(temps)
if omega== 0:
    c=0
    r=0
else:
    r=v/omega
    c=1/r

#Conditions initiales
x[0] = pos_init2[1]
y[0] = pos_init2[0]
theta[0] = angle_initiale


#Conditions initiales robot bleu
x2[0] = pos_init[0]
y2[0] = pos_init[1]
theta2[0] = angle_initiale2
thetae[0] = theta2[0] - theta[0] 

#####
vx=abs(x[0]-x2[0])
vy=abs(y[0]-y2[0])
dist= sqrt(vx*vx+vy*vy)
l[0]=dist-r

#méthode Euler
for i in range(1, len(temps)):
    x[i] = x[i-1] + delta_t * v *np.cos(theta[i-1])
    y[i] = y[i-1] + delta_t * v* np.sin(theta[i-1])
    theta[i] = theta[i-1] + delta_t * omega
    ###
    s[i]= s[i-1]+ delta_t*(v*np.cos(thetae[i-1]))/(1-c*l[i])
    l[i]=l[i-1]+ v2*thetae[i-1]*delta_t
    u= -k2*v2*l[i] - k3*v2*thetae[i-1]
    w2=u - s[i]
    ####
    x2[i] = x2[i-1] + delta_t * v2 *np.cos(theta2[i-1])
    y2[i] = y2[i-1] + delta_t * v2* np.sin(theta2[i-1])
    theta2[i] = theta2[i-1] + delta_t * w2
    thetae[i]= theta2[i] - theta[i]

    
    
    
    #print("{} \t {}",theta[i],x[i])
    

fig,ax = plt.subplots(figsize=(8,8))
#ax.plot(x, y,label="trajectoire")
plt.title('Trajectoire du mouvement')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

#####################
#limite plot
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)

#Ajout d'annotations
annotation_v = f'Vitesse: {v} m/s'
ax.text(0.05, 1, f'Pos_init_robot: {(x[0],y[0])}', transform=ax.transAxes, fontsize=10, color='black')
ax.text(0.05, 0.95, annotation_v, transform=ax.transAxes, fontsize=10, color='black')
annotation_theta = ax.text(0.05, 0.9,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_t = ax.text(0.05, 0.85,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_d = ax.text(0.05, 0.8,'', transform=ax.transAxes, fontsize=10, color='black')

trajectoire, = ax.plot(x,y,label="trajectoire")
#robot, = ax.plot([],[],'ro',markersize=20,label="robot")
#####Robot bleu
trajectoire2, = ax.plot(x2,y2,label="trajectoire")
robot2, = ax.plot([],[],'bo',markersize=20,label="robot2")

#animation
def animate(i):
    trajectoire.set_data([x[:i]], [y[:i]] )
    #robot.set_data([x[i]], [y[i]])
    trajectoire2.set_data([x2[:i]], [y2[:i]] )
    robot2.set_data([x2[i]], [y2[i]])
    annotation_t.set_text(f'Temps: {round(temps[i],2)} s')
    annotation_d.set_text(f'Distance parcouru: {round(distance[i],2)} m')
    annotation_theta.set_text(f'theta: {round(theta[i],2)} rad = {round(np.degrees(theta[i]),2)} deg')
    #trajectoire2.set_data([x2[:i]], [y2[:i]])
    #robot.set_data([x2[i]], [y2[i]])
    return [trajectoire2,trajectoire,robot2,annotation_t,annotation_d,annotation_theta]

Anima = animation.FuncAnimation(fig, animate, frames=range(len(temps)), interval=delta_t * 1000, blit=True)

ax.legend()
plt.show()
