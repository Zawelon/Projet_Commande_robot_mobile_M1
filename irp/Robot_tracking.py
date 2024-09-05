import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Timer


################
#Paramètre initial
v = 5
angle_initiale = np.radians(-90)
omega = 3
pos_init = np.array([-1,0])


###########
#Init para Robot Bleu
v2=1
angle_initiale2 = np.radians(90)
w2 = 1
pos_init2 = np.array([-1,0])

####
#Faire varier a et am
a=1
am=1
k1=2*a*am
k3=k1
k2=((a*a)-(omega*omega))/v
sign=1
if(v<0):
    sign=-1
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



#Conditions initiales
x[0] = pos_init2[0]
y[0] = pos_init2[1]
theta[0] = angle_initiale


#Conditions initiales robot bleu
x2[0] = pos_init[1]
y2[0] = pos_init[0]
theta2[0] = angle_initiale2




t=0
#méthode Euler
for i in range(1, len(temps)):
    t=t+1
    if(t==len(temps)*0.8):
        a=omega
        am=0.7
        k1=2*a*am
        k3=k1
        k2=((a*a)-(omega*omega))/v
    
    x[i] = x[i-1] + delta_t * v *np.cos(theta[i-1])
    y[i] = y[i-1] + delta_t * v* np.sin(theta[i-1])
    theta[i] = theta[i-1] + delta_t * omega
    e1=np.cos(theta2[i-1])*(x[i-1]-x2[i-1])+np.sin(theta2[i-1])*(y[i-1]-y2[i-1])
    e2=-np.sin(theta2[i-1])*(x[i-1]-x2[i-1])+np.cos(theta2[i-1])*(y[i-1]-y2[i-1])
    e3=theta[i-1]-theta2[i-1]
    u1=-k1*e1
    u2=-k2*sign*e2-k3*e3
    v2=v*np.cos(e3)-u1
    w2=omega-u2
    x2[i] = x2[i-1] + delta_t * v2 *np.cos(theta2[i-1])
    y2[i] = y2[i-1] + delta_t * v2* np.sin(theta2[i-1])
    theta2[i] = theta2[i-1] + delta_t * w2
    
    
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
robot, = ax.plot([],[],'ro',markersize=20,label="robot")
#####Robot bleu
trajectoire2, = ax.plot(x2,y2,label="trajectoire")
robot2, = ax.plot([],[],'bo',markersize=20,label="robot2")

#animation
def animate(i):
    trajectoire.set_data([x[:i]], [y[:i]] )
    robot.set_data([x[i]], [y[i]])
    trajectoire2.set_data([x2[:i]], [y2[:i]] )
    robot2.set_data([x2[i]], [y2[i]])
    annotation_t.set_text(f'Temps: {round(temps[i],2)} s')
    annotation_d.set_text(f'Distance parcouru: {round(distance[i],2)} m')
    annotation_theta.set_text(f'theta: {round(theta[i],2)} rad = {round(np.degrees(theta[i]),2)} deg')
    #trajectoire2.set_data([x2[:i]], [y2[:i]])
    #robot.set_data([x2[i]], [y2[i]])
    return [trajectoire2,trajectoire,robot2,robot,annotation_t,annotation_d,annotation_theta]

Anima = animation.FuncAnimation(fig, animate, frames=range(len(temps)), interval=delta_t * 1000, blit=True)

ax.legend()
plt.show()
