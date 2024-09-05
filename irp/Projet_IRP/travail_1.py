from math import*
from numpy import *
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import *
#import tkinter as tk


#fenetre = Tk()
#mo = Button(fenetre, text = "Bouton1")
#mol = Label(fenetre, text = "Bouton1")


def discretisation(v,w,distance):
    x=array([float()]*200)
    y=array([float()]*200)
    teta=array([float()]*200)
    x[0]=0
    y[0]=0
    nbre=50
    deltat_te= (2*pi)/(nbre-1)
    deltatx= distance/(nbre-1)
    deltaty=deltatx
    teta[0]=0
    teta[1]=0
    #x[1]=1
    #y[1]=1
    for i in range(1,distance-1):
        teta[i+1]=teta[i-1] + w*deltat_te
        x[i+1]=x[i-1] + v*cos(teta[i+1])*deltatx
        y[i+1]=y[i-1] + v*sin(teta[i+1])*deltaty
        print("x[{}]={}\t y[{}]= {}".format(i+1,x[i+1],i+1,y[i+1]))
        print("teta[{}]= {}".format(i+1,teta[i+1]))

     
    #fig = plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.plot3D(x, y, teta, 'gray')
    
    #######
    plt.plot(x,y,'.r')
    plt.show()
    ###########
       



v=int(input("Entrez la vitesse: "))
w=float(input("Entrez la vitesse angulaire: "))
dist=200
discretisation(v,w,dist)

#mol.pack()
#mo.pack()
#fenetre.mainloop()

