import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl
from astropy import table
from scipy.optimize import curve_fit
from fonctions_maison import *
from PIL import Image
from scipy.signal import find_peaks
from scipy.optimize import curve_fit 

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
        
        #Luminosity data in the y-axis down
        self.y = np.arange(self.iy_mil,self.iy_max,1)
        self.data_1D = self.data_array[self.iy_mil:,self.ix_mil,1]
        self.data_1D_pi = self.data_array_pi[self.iy_mil:,self.ix_mil,1]
        self.data_1D_sigma = self.data_array_sigma[self.iy_mil:,self.ix_mil,1]
        
        #Pics 
        #Minimums permettant de sectionner les groupes de raies 
        self.i_mins = find_peaks(-self.data_1D,height=240,distance=30)
        self.i_mins_pi = find_peaks(-self.data_1D_pi,height=240,distance=30)
        self.i_mins_sigma = find_peaks(-self.data_1D_sigma,height=240,distance=30)

        #Trouver les pics dans les sections
        self.pics_array = [] #Chaque élément sera une liste des pics d'une section
        
        for i in range(0,len(self.i_mins[0])-1): 
            pics = find_peaks(self.data_1D[self.i_mins[0][i]:self.i_mins[0][i+1]],height=20)
            y_pic = self.y[self.i_mins[0][i]:self.i_mins[0][i+1]]
            self.pics_array.append(y_pic[pics[0]])
         
        # Pour pi    
        self.pics_array_pi = [] #Chaque élément sera une liste des pics d'une section
        
        for i in range(0,len(self.i_mins_pi[0])-1): 
            pics_pi = find_peaks(self.data_1D_pi[self.i_mins_pi[0][i]:self.i_mins_pi[0][i+1]],height=20)
            y_pic_pi = self.y[self.i_mins_pi[0][i]:self.i_mins_pi[0][i+1]]
            self.pics_array_pi.append(y_pic_pi[pics_pi[0]])
            
        #Pour sigma
        self.pics_array_sigma = [] #Chaque élément sera une liste des pics d'une section
        
        for i in range(0,len(self.i_mins_sigma[0])-1): 
            pics_sigma = find_peaks(self.data_1D_sigma[self.i_mins_sigma[0][i]:self.i_mins_sigma[0][i+1]],height=20)
            y_pic_sigma = self.y[self.i_mins_sigma[0][i]:self.i_mins_sigma[0][i+1]]
            self.pics_array_sigma.append(y_pic_sigma[pics_sigma[0]])

    #Fonctions de visualisation         
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
        
    def methode_1D(self,pic=None): 
  
        if pic != None: 
            i_debut = self.i_mins[0][pic-1]
            i_fin = self.i_mins[0][pic]
            plt.plot(self.y[i_debut:i_fin],self.data_1D[i_debut:i_fin])
            plt.vlines(self.pics_array[pic-1],0,250,linestyle="--",color="g") 
            plt.title("Profil d'intensité 45 degrés (pic = {})".format(pic))
        
        if pic == None:   
            plt.plot(self.y,self.data_1D)
            plt.title("Profil d'intensité 45 degrés")
            
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.show()
        
    def methode_1D_pi(self,pic=None): 
        
        if pic != None: 
            i_debut = self.i_mins_pi[0][pic-1]
            i_fin = self.i_mins_pi[0][pic]
            plt.plot(self.y[i_debut:i_fin],self.data_1D_pi[i_debut:i_fin])
            plt.vlines(self.pics_array_pi[pic-1],0,250,linestyle="--",color="g") 
            plt.title("Profil d'intensité pi (pic = {})".format(pic))
        
        if pic == None:   
            plt.plot(self.y,self.data_1D_pi)
            plt.title("Profil d'intensité pi")
            
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.show()
        
    def methode_1D_sigma(self,pic=None): 
        
        if pic != None: 
            i_debut = self.i_mins_sigma[0][pic-1]
            i_fin = self.i_mins_sigma[0][pic]
            plt.plot(self.y[i_debut:i_fin],self.data_1D_sigma[i_debut:i_fin])
            plt.vlines(self.pics_array_sigma[pic-1],0,250,linestyle="--",color="g") 
            plt.title("Profil d'intensité sigma (pic = {})".format(pic))
        
        if pic == None:   
            plt.plot(self.y,self.data_1D_sigma)
            plt.title("Profil d'intensité sigma")
            
        plt.xlabel("y")
        plt.ylabel("Intensité")
        plt.show()
        
      
        