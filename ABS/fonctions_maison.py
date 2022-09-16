import numpy as np 
import matplotlib.pyplot as plt 
from astropy import table
from scipy.optimize import curve_fit

#####################################################################################################################################################################
### Fit Gaussien
def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def fit_gaussien(x,y,p0 = [1,1,1,1]): 
    
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

    plt.plot(x, y)
    plt.plot(x, y_fit)
    plt.show()
    
    return y_fit, p_opt, p_err


######################################################################################################################################
### Régression linéaire

def droite(x, a, b): 
    return a*x + b

def reg_lin(x,y, p0 = [1,1]): 
    
    """
    Régression linéaire
    
    ### Paramètres
    x, y: fonction
    p0: Valeurs d'essaies
    
    ### returns
    y_fit: Fonction de la droite ajustée
    p_opt: Paramètres de la droite (a,b)
    p_cov: Incertitudes sur ces paramètres
    
    """
    
    p_opt, p_cov = curve_fit(droite, x, y, p0 = p0)
    p_err = np.sqrt(np.diag(p_cov)) #Incertitudes sur les paramètres
    
    print("a = {} +/- {} et b = {} +/- {}".format(p_opt[0], p_err[0], p_opt[1], p_err[1]))
    
    a, b = p_opt[0], p_opt[1]
    
    y_fit = droite(x, a, b)
    
    plt.plot(x, y)
    plt.plot(x, y_fit)
    plt.show()
    
    return y_fit, p_opt, p_err
    
#############################################################################################################################################################
### Trouver l'indice d'un point proche d'une valeur dans un array

def find_nearest(array, value):
    
    """
    Trouve l'indice du point le plus près d'une valeur donnée dans un array donné

    ### Paramètres
    array: Le array dans lequel chercher l'indice
    value: La valeur pour laquelle on veut trouver le point le plus proche
    
    ### Retourne
    idx: L'indice du point le plus près de la valeur donnée
    
    """
    
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    
    return idx