# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 11:39:07 2022

@author: Michaël Lévesque
"""

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl
from astropy import table
from scipy.optimize import curve_fit
import random

######################## FONCTIONS ############################
### Fit Gaussien
def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def fit_gaussien(x,y,p0 = [1,1,1,1],show = False): 
    
    """
    Ajuste une gaussienne sur la fonction donnée
    
    ### Paramètres
    x, y: fonction
    p0: Valeurs d'essaies
    
    ### returns
    y_fit: Fonction de la gaussienne ajustée
    p_opt: Paramètres de la gaussienne (H , A , x0, sigma)
    p_cov: Incertitudes sur ces paramètres
    """
    
    p_opt, p_cov = curve_fit(gauss, x, y, p0 = p0)
    p_err = np.sqrt(np.diag(p_cov)) #Incertitudes sur les paramètres
    
    print("H = {} +/- {}, A = {} +/- {}, x0 = {} +/- {}, sigma = {} +/- {}".format(p_opt[0], p_err[0], p_opt[1], p_err[1], p_opt[2], p_err[2], p_opt[3], p_err[3]))

    H, A, x0, sigma = p_opt[0], p_opt[1], p_opt[2], p_opt[3] # Paramètres optimisés

    y_fit = gauss(x, H, A, x0, sigma)

    if show == True:
        plt.plot(x, y)
        plt.plot(x, y_fit)
        plt.show()
    
    return y_fit, p_opt, p_err

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def find_max(array):
    v_max=np.amax(array)
    return v_max

###Créationd'une fonction test###
x_test=np.arange(-1e-2, 1e-2, 5.2e-6)
Test=gauss(x_test,1,100,0,2e-3)+(3)*(np.random.rand(len(x_test))-np.random.rand(len(x_test)))

plt.plot(x_test,Test)

D=4e-2 #Distance entre caméra et fibre optique
R=[1.75e-6, 2.2e-6, 1.8e-6] #Rayon des coeurs de fibre monomode
lamda=405e-9 #nm
k=2*np.pi/lamda #nombre d'onde
NA=0.13

#Fit
y_fit, p_opt, p_err = fit_gaussien(x_test, Test, [0,100,0,1e-2], True)
#plt.plot(x_test, y_fit)

cinq_pourcent = find_max(y_fit)*0.05
x_limite = x_test[find_nearest(y_fit,cinq_pourcent)]

NA=np.arctan(np.abs(x_limite)/D)

r=R[0] #Sélection d'une fibre
V=k*r*NA #V

print("V={}".format(V))













