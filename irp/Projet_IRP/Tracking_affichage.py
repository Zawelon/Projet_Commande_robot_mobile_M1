import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Timer


################
#Paramètre initial
v = 2.5
angle_initiale = np.radians(-90)
omega = 1.2  ###### A partir d'une certaine vitesse angulaire l'équation linéairisé n'est plus validé (5 rad/s)
pos_init = np.array([-2,-2])


###########
#Init para Robot Bleu
v2=0
angle_initiale2 = np.radians(90)
w2 = 0
pos_init2 = np.array([-1,-5])

####
#Faire varier a et am
a=2
am=0.9
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
d_final = 20
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

#Init parametre pour affichage courbe en animation
Vit1 = np.zeros_like(temps)
Vit2 = np.zeros_like(temps)

omg1 = np.zeros_like(temps)
omg2 = np.zeros_like(temps)


#Conditions initiales
x[0] = pos_init[0]
y[0] = pos_init[1]
theta[0] = angle_initiale


#Conditions initiales robot bleu
x2[0] = pos_init2[1]
y2[0] = pos_init2[0]
theta2[0] = angle_initiale2




t=0
#méthode Euler
for i in range(1, len(temps)):
    t=t+1
    """
    if(t==len(temps)*0.8):
        a=omega
        am=0.7
        k1=2*a*am
        k3=k1
        k2=((a*a)-(omega*omega))/v
    """
    x[i] = x[i-1] + delta_t * v *np.cos(theta[i-1])
    y[i] = y[i-1] + delta_t * v* np.sin(theta[i-1])
    theta[i] = theta[i-1] + delta_t * omega
    e1=np.cos(theta2[i-1])*(x[i-1]-x2[i-1])+np.sin(theta2[i-1])*(y[i-1]-y2[i-1])
    e2=-np.sin(theta2[i-1])*(x[i-1]-x2[i-1])+np.cos(theta2[i-1])*(y[i-1]-y2[i-1])
    e3=theta[i-1]-theta2[i-1]
    u1=(-k1)*e1
    u2=-k2*sign*e2-k3*e3
    v2=v*np.cos(e3)-u1
    w2=omega-u2
    x2[i] = x2[i-1] + delta_t * v2 *np.cos(theta2[i-1])
    y2[i] = y2[i-1] + delta_t * v2* np.sin(theta2[i-1])
    theta2[i] = theta2[i-1] + delta_t * w2
    
    ###Pour Plot 
    Vit1[i]=v
    Vit2[i]=v2
    
    omg1[i]=omega
    omg2[i]=w2
    
    #print("{} \t {}",theta[i],x[i])


######################################
#Plot#

plt.close('all')
plt.style.use("seaborn")
fig = plt.figure(figsize=[100,100])

#fig,ax = plt.subplots(figsize=(8,8))
#ax.plot(x, y,label="trajectoire")
plt.grid(True)

ax = plt.subplot2grid((3,3), (0,0),rowspan=2,colspan=2)
plt.title('Trajectoire du mouvement')
plt.xlabel('x')
plt.ylabel('y')

ax1 = plt.subplot2grid((3,3), (0,2))
plt.title('Vitesse des robots en fonction du temps')
plt.xlabel('t')
plt.ylabel('V (m/s)')
ax1.set_xlim(0,max(temps))

ax2 = plt.subplot2grid((3,3), (1,2))
plt.title('Vitesse Angulaire de robots en fonction du temps')
plt.xlabel('t')
plt.ylabel('W (rad/s)')
ax2.set_xlim(0,max(temps))

ax3 = plt.subplot2grid((3,3), (2,2))
plt.title('Angle des robots en fonction du temps')
plt.xlabel('t (s)')
plt.ylabel('theta (rad)')
ax3.set_xlim(0,max(temps))

ax4 = plt.subplot2grid((3,3), (2,1))
plt.title('y(t)')
plt.xlabel('t (s)')
plt.ylabel('y')
ax4.set_xlim(0,max(temps))

ax5 = plt.subplot2grid((3,3), (2,0))
plt.title('x(t)')
plt.xlabel('t (s)')
plt.ylabel('x')
ax5.set_xlim(0,max(temps))







#####################
#limite plot 
#Faire animer plot pour aller plus loin#
# ax.set_xlim(-15,15)
# ax.set_ylim(-15,15)


############################
# Animation #


#Ajout d'annotations
annotation_v = f'Vitesse: {v} m/s'
ax.text(0.05, 1, f'Pos_init_robot: {(x[0],y[0])}', transform=ax.transAxes, fontsize=10, color='black')
ax.text(0.05, 0.95, annotation_v, transform=ax.transAxes, fontsize=10, color='black')
annotation_theta = ax.text(0.05, 0.9,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_t = ax.text(0.05, 0.85,'', transform=ax.transAxes, fontsize=10, color='black')
annotation_d = ax.text(0.05, 0.8,'', transform=ax.transAxes, fontsize=10, color='black')

#robot rouge
trajectoire, = ax.plot(x,y,'r',label="trajectoire R1", linewidth = 3)
robot, = ax.plot([],[],'ro',markersize=20,label="robot")

#Robot bleu
trajectoire2, = ax.plot(x2,y2,'b',markersize=5,label="trajectoire R2")
robot2, = ax.plot([],[],'bo',markersize=20,label="robot2")

#Vitesse : v(t)
vitess1, = ax1.plot(temps,Vit1,'r',markersize=2.5,label="v1")
vitess2, = ax1.plot(temps,Vit2,'b',markersize=2.5,label="v2")

#Omega : w(t)
omega1, = ax2.plot(temps,omg1,'r',markersize=2.5,label="w1")
omega2, = ax2.plot(temps,omg2,'b',markersize=2.5,label="w2")

#theta(t)
angle1, = ax3.plot(temps,theta,'r',markersize=2.5,label="theta1")
angle2, = ax3.plot(temps,theta,'b',markersize=2.5,label="theta2")

#Position : x(t) et y(t)
pos_x1, = ax5.plot(temps,x,'r',markersize=2.5,label="x1")
pos_x2, = ax5.plot(temps,x2,'b',markersize=2.5,label="x2")

pos_y1, = ax4.plot(temps,y,'r',markersize=2.5,label="y1")
pos_y2, = ax4.plot(temps,y2,'b',markersize=2.5,label="y2")

#fct animation
def animate(i):
    trajectoire.set_data([x[:i]], [y[:i]] )
    robot.set_data([x[i]], [y[i]])
    trajectoire2.set_data([x2[:i]], [y2[:i]] )
    robot2.set_data([x2[i]], [y2[i]])
    
    vitess1.set_data([temps[:i]],[Vit1[:i]])
    vitess2.set_data([temps[:i]],[Vit2[:i]])
    
    omega1.set_data([temps[:i]],[omg1[:i]])
    omega2.set_data([temps[:i]],[omg2[:i]])
    
    angle1.set_data([temps[:i]],[theta[:i]])
    angle2.set_data([temps[:i]],[theta2[:i]])
    
    pos_x1.set_data([temps[:i]],[x[:i]])
    pos_x2.set_data([temps[:i]],[x2[:i]])
    
    pos_y1.set_data([temps[:i]],[y[:i]])
    pos_y2.set_data([temps[:i]],[y2[:i]])
    
    annotation_t.set_text(f'Temps: {round(temps[i],2)} s')
    annotation_d.set_text(f'Distance parcouru: {round(distance[i],2)} m')
    annotation_theta.set_text(f'theta: {round(theta[i],2)} rad = {round(np.degrees(theta[i]),2)} deg')
    #trajectoire2.set_data([x2[:i]], [y2[:i]])
    #robot.set_data([x2[i]], [y2[i]])
    return [trajectoire,trajectoire2,robot,robot2,annotation_t,annotation_d,annotation_theta,vitess1,vitess2,omega1,omega2,angle1,angle2,pos_x1,pos_x2,pos_y1,pos_y2]

Anima = animation.FuncAnimation(fig, animate, frames=range(len(temps)), interval=delta_t * 1000, blit=True)

ax.legend()
#ax1.legend()
plt.show()
