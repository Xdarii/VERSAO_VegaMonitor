# -*- coding: utf-8 -*-
"""
Created on Sun May 29 22:42:25 2016

@author: Mamadou Dian BAH
"""

import scipy as sp

def TVDI_function(inNDVI,inLST,pas=0.02,t=1,s1Min=0.3,s2Max=0.8,ss1Min=0.2,ss2Max=0.8):
    """
    Allows to calculates the TVDI.

    this function is a modified version of the IDL script published by Monica Garcia:
    (Garcia,M., Fernández, N., Villagarcía, L., Domingo, F.,  Puigdefábregas,J. & I. Sandholt. 2014. 2014. 
    Accuracy of the Temperature–Vegetation Dryness Index using MODIS under water-limited vs. 
    energy-limited evapotranspiration conditions  Remote Sensing of Environment 149, 100-117.) 

    Input:
        inNDVI: NDVI 
        inLST: land surface temperature
        pas: intervall of the NDVI


        S1min: lower threshold to determine the interval which will be used to determine the design parameters of LSTmax
        S2max: upper threshold to determine the interval which will be used to determine the design parameters of LSTmax
        ss1Min: lower threshold to determine the interval which will be used to determine the calculation of parmaètres LSTmin
        ss2Max: upper threshold to determine the interval which will be used to determine the design parameters of LSTmin

        
        t : t=0 to use Garcia M method  and t=1 to calculate the TVDI without using the threshold .
    Output: 
    
        TVDI
    """
    TVDI=sp.zeros(inLST.shape)
    if inNDVI.shape == inLST.shape :
        
        inNdvi=sp.reshape(inNDVI,(inNDVI.size))  
        inLst=sp.reshape(inLST,(inLST.size))  
        
        mini=sp.nanmin(inNdvi) # valeur minimale
        maxi=sp.nanmax(inNdvi) # valeur maximale
        
        
        arg=sp.argsort(inNdvi) #trie et renvoi les indices des valeurs ordonnées
    
        
        inV=inNdvi[arg] # on récupère les valeurs de NDVI
        inT=inLst[arg] # on récupère les valeurs de temperature
          # pas de decoupade du NDVI en intervalle
        
        
        percentileMax=99.0 
        
        percentileMin=1.0
        
        nObsMin=5 # la longeur minimale que doit avoir un intervalle pour être considéré
        
        ni= int(round((maxi-mini)/pas ) + 1) # Nombre total d'intervalle
        iValMax=0 
        iValMin=ni
        #création des vecteurs de stockage
        vx= sp.zeros((ni),dtype="float")
        vMaxi=sp.zeros((ni),dtype="float")
        vMini=sp.zeros((ni),dtype="float")
        
        vMaxi[0:]=None
        vMini[0:]=None
    
        vNpi=sp.zeros((ni),dtype="float")
        
        
        for k in range (ni):
            
            hi=k*pas + mini # valeur de depart de l'intervalle
            hs=k*pas + hi # valeur de fin de l'intervalle
            
            a=sp.where(inV <= hi)
            ii=a[0].max()
            
            b=sp.where(inV <= hs)
            iis=b[0].max()
            
            vNpi[k]=  iis - ii
            inTp=inT[ii:iis+1] #recuperation des valeurs de temperature contenues dans cet intervalle       
            vx[k]=(hs - hi )/2 +hi #recuperation de valeur de NDVI qui se trouve au milieu intervalle
            if vNpi[k] > nObsMin : #on teste si l'intervalle defini a suffisamment de valeur
    
                inTp=inTp[sp.argsort(inTp)] #on trie les valeurs de temperature contenu dans cet intervalle
                vMaxi[k]=inTp[ int( ( vNpi[k] *percentileMax/100 )) ] #on recupère la valeur de temperature qui correspond au 99em percentile de l'intervalle
                vMini[k]=inTp[ int( ( vNpi[k] *percentileMin/100 ))] #on recupère la valeur de temperature qui correspond au 99em percentile de l'intervalle
                if k >iValMax:
                    iValMax=k
                if k < iValMin:
                    iValMin=k
        
    	# calcul de LSTmax et LSTmin
        if (t==0):
            # Dry Edge     
        	   # on utilise un seuil inferieur pour trouver la fin de l'intervalle qui va servir pour le calcul de la regression linéaire
            # on utilise iValMin et iValMax pour eviter les nan c'est à dire on reste dans les intervalles qui respecte le nObsMin
            try:
                b=sp.where(vx < s1Min) # seuil inferieur à modifier
                ii=sp.nanmax([sp.nanmax(b[0]),iValMin]) 
                
                b=sp.where(vx < s2Max) # seuil superieur à modifier
                iis=sp.nanmin([sp.nanmax(b[0]),iValMax])
            
        
                # Wet Edge        
                c=sp.where(vx < ss1Min) # seuil inferieur à modifier
                ii2=sp.nanmax([sp.nanmax(c[0]),iValMin]) 
                
                c=sp.where(vx < ss2Max) # seuil superieur à modifier
                iis2=sp.nanmin([sp.nanmax(c[0]),iValMax])
            except:
                print "problème avec les valeurs inferieures et superieures utilisées"
        else:
            ii=iValMin
            iis=iValMax
            ii2=iValMin
            iis2=iValMax
            
        #calcul de la regression linéaire
        estimation1=sp.stats.linregress(vx[ii:iis+1],vMaxi[ii:iis+1])
        
        #LSTmax= a * NDVI + b
        lstmax_a=estimation1[0] #recuperation du paramètre de pente
        lstmax_b=estimation1[1] #recuperation du paramètre de l'ordonnée à l'origine
        
        estimation1=sp.stats.linregress(vx[ii2:iis2+1],vMini[ii2:iis2+1])
        #LSTmax= a * NDVI + b
        lstmin=sp.nanmin(vMini[ii2:iis2+1])
        #calcul de TVDI
        TVDI=( inLST - lstmin) / ( lstmax_b + (lstmax_a * inNDVI )- lstmin+0.00000001 )
#        TVDI=( inLST - lstmin) / ( ( lstmax_b + (lstmax_a * inNDVI ))- lstmin +0.00001 )
    else:
        print "les deux tableaux n'ont pas la même taille"
        exit
    
    return TVDI
        


