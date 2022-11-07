import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl
from astropy import table
from scipy.optimize import curve_fit
from fonctions_maison import *
from PIL import Image
from scipy.signal import find_peaks
from scipy.optimize import curve_fit 
from skimage.draw import circle_perimeter

class zeeman:
    
    def __init__(self, input_file, input_file_pi, input_file_sigma,bleu=False): 
        
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
        if bleu == True: 
            self.y = np.arange(self.iy_mil,self.iy_max,1)
            self.data_1D = self.data_array[self.iy_mil:,self.ix_mil,2]
            self.data_1D_pi = self.data_array_pi[self.iy_mil:,self.ix_mil,2]
            self.data_1D_sigma = self.data_array_sigma[self.iy_mil:,self.ix_mil,2]
            
        else:
            self.y = np.arange(self.iy_mil,self.iy_max,1)
            self.data_1D = self.data_array[self.iy_mil:,self.ix_mil,1]
            self.data_1D_pi = self.data_array_pi[self.iy_mil:,self.ix_mil,1]
            self.data_1D_sigma = self.data_array_sigma[self.iy_mil:,self.ix_mil,1]
        
        #Pics 
        #Minimums permettant de sectionner les groupes de raies 
        if bleu == True:
            self.i_mins = find_peaks(-self.data_1D,height=240,distance=30)
            self.i_mins_pi = find_peaks(-self.data_1D_pi,height=240,distance=30)
            self.i_mins_sigma = find_peaks(-self.data_1D_sigma,height=240,distance=30) 
            
        else: 
            
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
        
    def methode_1D(self,pic=False): 
  
        if pic == True: 
            n_pics = len(self.pics_array)
            fig,axes = plt.subplots(n_pics,figsize=(10,35),squeeze=True)
            for p in range(n_pics):
                ax = axes[p]
                i_debut = self.i_mins[0][p]
                i_fin = self.i_mins[0][p+1]
                ax.plot(self.y[i_debut:i_fin],self.data_1D[i_debut:i_fin],label="pic = {}".format(p+1))
                ax.vlines(self.pics_array[p],0,250,linestyle="--",color="g") 
                ax.set_xlabel("y")
                ax.set_ylabel("Intensité")
                ax.legend()
        
        if pic == False:   
            plt.plot(self.y,self.data_1D)
            plt.title("Profil d'intensité")
            plt.xlabel("y")
            plt.ylabel("Intensité")
        
        plt.show()
        
    def methode_1D_pi(self,pic=False): 
        
        if pic == True: 
            n_pics = len(self.pics_array_pi)
            fig,axes = plt.subplots(n_pics,figsize=(10,35),squeeze=True)
            for p in range(n_pics):
                ax = axes[p]
                i_debut = self.i_mins_pi[0][p]
                i_fin = self.i_mins_pi[0][p+1]
                ax.plot(self.y[i_debut:i_fin],self.data_1D_pi[i_debut:i_fin],label="pic = {}".format(p+1))
                ax.vlines(self.pics_array_pi[p],0,250,linestyle="--",color="g") 
                ax.set_xlabel("y")
                ax.set_ylabel("Intensité")
                ax.legend()
        
        if pic == False:   
            plt.plot(self.y,self.data_1D_pi)
            plt.title("Profil d'intensité pi")
            plt.xlabel("y")
            plt.ylabel("Intensité")
        
        plt.show()
        
    def methode_1D_sigma(self,pic=False): 
        
        if pic == True: 
            n_pics = len(self.pics_array_sigma)
            fig,axes = plt.subplots(n_pics,figsize=(10,35),squeeze=True)
            for p in range(n_pics):
                ax = axes[p]
                i_debut = self.i_mins_sigma[0][p]
                i_fin = self.i_mins_sigma[0][p+1]
                ax.plot(self.y[i_debut:i_fin],self.data_1D_sigma[i_debut:i_fin],label="pic = {}".format(p+1))
                ax.vlines(self.pics_array_sigma[p],0,250,linestyle="--",color="g") 
                ax.set_xlabel("y")
                ax.set_ylabel("Intensité")
                ax.legend()
    
        if pic == False:   
            plt.plot(self.y,self.data_1D_sigma)
            plt.title("Profil d'intensité sigma")
            plt.xlabel("y")
            plt.ylabel("Intensité")
    
        plt.show()
        
    def dessin_cercle_1D(self,num_cercle=1):
        
        fig,ax = plt.subplots(1,figsize=(30,30))
        ax.imshow(self.data)
        
        intensites = []
        cercles = []
        
        n=0
        for pic_prin in self.pics_array:
            cercles_sec = []
            for pic_sec in pic_prin: 
                #On dessine le cercle
                cercle = circle_perimeter(self.ix_mil, self.iy_mil,np.abs(pic_sec-self.iy_mil))
                cercles_sec.append(cercle)
                
                if n==num_cercle:
                    ax.plot(cercle[0],cercle[1],'ro',markersize=0.5)
                n+=1
            cercles.append(cercles_sec)
            
        return cercles
        
    def methode_cercle(self): 
        
        intensites = []
        n=0
        for radius in np.abs(self.y-self.iy_mil): 
            cercle = circle_perimeter(self.ix_mil, self.iy_mil,radius)
            data = self.data_array[:,:,1]
            intensite = np.mean(data[cercle[1],cercle[0]])
            intensites.append(intensite)
              
        #Trouver les pics dans les sections
        pics_cercle = [] #Chaque élément sera une liste des pics d'une section
        intensites = np.array(intensites)
        i_mins = find_peaks(-intensites,height=-15,distance=30)
        
        for i in range(0,len(i_mins[0])-1): 
            pics = find_peaks(intensites[i_mins[0][i]:i_mins[0][i+1]],height=20)
            y_pic = self.y[i_mins[0][i]:i_mins[0][i+1]]
            pics_cercle.append(y_pic[pics[0]])   
        n_pics = len(pics_cercle)
        fig,axes = plt.subplots(n_pics,figsize=(10,35),squeeze=True)
        
        for p in range(n_pics):
            ax = axes[p]
            i_debut = i_mins[0][p]
            i_fin = i_mins[0][p+1]
            ax.plot(self.y[i_debut:i_fin],intensites[i_debut:i_fin],label="pic = {}".format(p+1))
            ax.vlines(pics_cercle[p],0,250,linestyle="--",color="g") 
            ax.set_xlabel("y")
            ax.set_ylabel("Intensité")
            ax.legend()
        plt.show()
        
        return intensites,pics_cercle
            
    def energie(self,skip=0):
        plt.figure(1, figsize=(10,4), dpi=400)
        plt.xlabel("Rang du pic d'interférence (discret)")
        plt.ylabel("Rayon des pics secondaires $r^2\ (m^2)$")
        #specify x-axis locations
        x_ticks = [1, 2, 3, 4, 5]
        #add x-axis values to plot
        plt.xticks(ticks=x_ticks)

        y1, popt1, pcov1 = reg_lin(np.arange(1,len(self.pics_array[0+skip])+1,1) ,self.pics_array[0+skip]**2)
        plt.plot(np.arange(1,len(self.pics_array[0+skip])+1,1) ,self.pics_array[0+skip]**2 , ls="none", marker="d", mec="black", mfc="none")
        plt.plot(np.arange(1,len(self.pics_array[0+skip])+1,1) , y1 , ls="--" , color="black", label="1")

        y2, popt2, pcov2 = reg_lin(np.arange(1,len(self.pics_array[1+skip])+1,1) ,self.pics_array[1+skip]**2)
        plt.plot(np.arange(1,len(self.pics_array[1+skip])+1,1) ,self.pics_array[1+skip]**2 , ls="none", marker="x", mec="b", mfc="none")
        plt.plot(np.arange(1,len(self.pics_array[1+skip])+1,1) , y2 , ls="--" , color="b", label="2")

        y3, popt3, pcov3 = reg_lin(np.arange(1,len(self.pics_array[2+skip])+1,1) ,self.pics_array[2+skip]**2)
        plt.plot(np.arange(1,len(self.pics_array[2+skip])+1,1) ,self.pics_array[2+skip]**2 , ls="none", marker="^", mec="g", mfc="none")
        plt.plot(np.arange(1,len(self.pics_array[2+skip])+1,1) , y3 , ls="--" , color="g", label="3")

        y4, popt4, pcov4 = reg_lin(np.arange(1,len(self.pics_array[3+skip])+1,1) ,self.pics_array[3+skip]**2)
        plt.plot(np.arange(1,len(self.pics_array[3+skip])+1,1) ,self.pics_array[3+skip]**2 , ls="none", marker="o", mec="r", mfc="none")
        plt.plot(np.arange(1,len(self.pics_array[3+skip])+1,1) , y4 , ls="--" , color="r", label="4")

        y5, popt5, pcov5 = reg_lin(np.arange(1,len(self.pics_array[4+skip])+1,1) ,self.pics_array[4+skip]**2)
        plt.plot(np.arange(1,len(self.pics_array[4+skip])+1,1) ,self.pics_array[4+skip]**2 , ls="none", marker="v", mec="y", mfc="none")
        plt.plot(np.arange(1,len(self.pics_array[4+skip])+1,1) , y5 , ls="--" , color="y", label="5")

        plt.legend()

        parametre = np.array([[popt1, popt2, popt3, popt4, popt5], [pcov1, pcov2, pcov3, pcov4, pcov5]])

        energie1 = parametre[0,0,1]/parametre[0,0,0]
        energie2 = parametre[0,1,1]/parametre[0,1,0]
        energie3 = parametre[0,2,1]/parametre[0,2,0]
        energie4 = parametre[0,3,1]/parametre[0,3,0]
        energie5 = parametre[0,4,1]/parametre[0,4,0]
        energie_tot = np.array([energie1, energie2, energie3, energie4, energie5])
        print(energie_tot)
      
        
        