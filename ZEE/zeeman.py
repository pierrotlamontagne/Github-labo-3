import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl
from astropy import table
from scipy.optimize import curve_fit
from fonctions_maison import *
from PIL import Image

class zeeman:
    
    def __init__(self, input_file, input_file_pi, input_file_sigma): 
        
        # Fichiers de input
        self.input_file = input_file
        self.input_file_pi = input_file_pi
        self.input_file_sigma= input_file_sigma
        
        #Données
        self.data = Image.open(self.input_file)
        self.data_pi = Image.open(self.input_file_pi)
        self.data_sigma = image = Image.open(self.input_file_sigma)
        
        #Arrays de données
        self.data_array = np.array(self.data)
        self.data_array_pi = np.array(self.data_pi)
        self.data_array_sigma = np.array(self.data_sigma)
        
        #Indices de l'image
        #Milieu
        self.ix_mil = int(np.shape(self.data_array)[1]/2) +45
        self.iy_mil = int(np.shape(self.data_array)[0]/2) +5
        
        #Min
        self.ix_min = 0
        self.iy_min = 0
        
        #Max
        self.ix_max = int(np.shape(self.data_array)[1])
        self.iy_max = int(np.shape(self.data_array)[0])
        
    def image(self): 
        plt.imshow(self.data)
        plt.hlines(self.iy_mil, self.ix_min, self.ix_max)
        plt.vlines(self.ix_mil, self.iy_min, self.iy_max)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Polarisation 45 degrés")
        plt.show()
        
    def image_pi(self): 
        plt.imshow(self.data_pi)
        plt.hlines(self.iy_mil, self.ix_min, self.ix_max)
        plt.vlines(self.ix_mil, self.iy_min, self.iy_max)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Polarisation pi")
        plt.show()
        
    def image_sigma(self): 
        plt.imshow(self.data_sigma)
        plt.hlines(self.iy_mil, self.ix_min, self.ix_max)
        plt.vlines(self.ix_mil, self.iy_min, self.iy_max)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Polarisation sigma")
        plt.show()
        
    def methode_1D(self,zoom=None): 
        data_1D = self.data_array[self.iy_mil:,self.ix_mil,1]
        y = np.arange(self.iy_mil,self.iy_max,1)
            
        if zoom != None: 
            i_debut = zoom[0]
            i_fin = zoom[1]
            data_1D = self.data_array[i_debut:i_fin,self.ix_mil,1]
            y = np.arange(i_debut,i_fin,1)
            
        plt.plot(y,data_1D)
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.title("Profil d'intensité 45 degrés")
        plt.show()
        
    def methode_1D_pi(self,zoom=None): 
        data_1D = self.data_array_pi[self.iy_mil:,self.ix_mil,1]
        y = np.arange(self.iy_mil,self.iy_max,1)
        
        if zoom != None: 
            i_debut = zoom[0]
            i_fin = zoom[1]
            data_1D = self.data_array_pi[i_debut:i_fin,self.ix_mil,1]
            y = np.arange(i_debut,i_fin,1)
        
        plt.plot(y,data_1D)
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.title("Profil d'intensité pi")
        plt.show()
        
    def methode_1D_sigma(self,zoom=None): 
        data_1D = self.data_array_sigma[self.iy_mil:,self.ix_mil,1]
        y = np.arange(self.iy_mil,self.iy_max,1)
        
        if zoom != None: 
            i_debut = zoom[0]
            i_fin = zoom[1]
            data_1D = self.data_array_sigma[i_debut:i_fin,self.ix_mil,1]
            y = np.arange(i_debut,i_fin,1)
        
        plt.plot(y,data_1D)
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.title("Profil d'intensité sigma")
        plt.show()
        
      
        