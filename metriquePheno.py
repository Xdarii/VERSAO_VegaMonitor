# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 10:53:01 2016

@author: Mamadou Dian BAH
"""

import scipy as sp

    
    
def metrique_pheno_greenbrown(ndvi=sp.empty, methode="trs",seuil1=-1,seuil2=-1):
    
    """
    
    This script uses an absolue threshold to identifie the dates of beginning ,end , length, of season and other metrics
     Parameters:
     ----------
         ndvi: ndvi of data
         threshold1: corresponds to the threshold around which we think to find the beginning of the vegetation
         threshold2: corresponds to the threshold around which we think to find senescence
         ndvi: is the Evolution OF NDVI for a pixel over a year
         method: is the method used to estimate
     Returns:
     ------
         a list containing the sos, eos, los, indMin n (index min), indMax (index max) ndvi min and max ndvi    """
    
  
    try:
        ndviMin=ndvi.min() #valeur minimale
        ndviMax=ndvi.max() #valeur maximale
        #ndviMean=ndvi.mean() #valeur moyenne
        
        indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
        indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
        
        
        if methode=="trs":
        
            ratio=ndvi
            if seuil1<0 and seuil2<0:
                seuil1=0.3
                seuil2=0.6
              
        
        test1=ratio[:indMax] >seuil1     # recherche les valeur de NDVI qui montre la croissance (augmentation de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
        test2=ratio[indMax:] <seuil2  # recherche les valeur de NDVI qui montre la senescence (baisse de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
        
        som1=sp.sum(test1) # teste si le seuil est adapté aux données 
        som2=sp.sum(test2) #teste 
    
    except:
        som1=0
        som2=0

    if (som1>0):
        
        Tsos=sp.where( test1==1)[0][0]  
        sos=int(sp.median(sp.where( ratio[:indMax]==ratio[Tsos])))  + 1
        

    if (som2>0):

        Teos=sp.where( test2==1)[0][0] + indMax      
        eos=int(sp.median(sp.where( ratio[indMax:]==ratio[Teos]))) + indMax + 1 

    if(som1==0):
        
        sos=-1
        
    if(som2==0):
        
        eos=-1  
        
    if(som1>0 and som2>0):
        
        los=eos-sos
        
    else:
        los=-1



    out=[sos,eos,los,indMin+1,indMax+1,ndviMin,ndviMax]


    return out


#%%
def metrique_pheno_vito(ndvi=sp.empty,seuil1=0.25,seuil2=0.75):
    """
    This script uses a relative threshold to identifie the dates of beginning of season, end of season .    
     Parameters:
     ----------
         ndvi: ndvi of data
         threshold1: corresponds to the threshold around which we think to find the beginning of the vegetation
         threshold2: corresponds to the threshold around which we think to find senescence
         ndvi: is the Evolution OF NDVI for a pixel over a year
         method: is the method used to estimate
     Returns:
     ------
         a list containing the sos, eos, los, indMin n (index min), indMax (index max), ndvi min and max ndvi    
    """
    ndviMin=ndvi.min() #valeur minimale
    ndviMax=ndvi.max() #valeur maximale
    
    indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
    indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
    
    try:
        ndviMin1=ndvi[:indMax].min() #valeur minimale
        indMin1=int(sp.median(sp.where(ndvi[:indMax]==ndviMin1))) #indice du minimum
    
        
        ndviMin2=ndvi[indMax:].min() #valeur minimale
        indMin2=int(sp.median(sp.where(ndvi[indMax:]==ndviMin2)))+indMax #indice du minimum
    
        ndvi1=ndvi[indMin1:indMax] #phase de croissance
        ndvi2=ndvi[indMax+1:indMin2] #phase de senescence
        
        
        ndviEcart1=(ndviMax-ndviMin1)*seuil1 +ndviMin1 #l'ecart entre la valeur min et max
        
        ndviEcart2=(ndviMax-ndviMin2)*seuil2  + ndviMin2     #l'ecart entre la valeur min et max de la valeur maximale   
        test1=ndvi1>=ndviEcart1         # 
        test2=ndvi2<=ndviEcart2        #
    
        som1=sp.sum(test1)
        som2=sp.sum(test2)
    except:
        som1=0
        som2=0
    
    if (som1>0):
        Tsos=sp.where( test1==1)[0][0]  
        sos=int(sp.median(sp.where( ndvi1==ndvi1[Tsos]))) + indMin1 +1 # 
        

    if (som2>0):

        Teos=sp.where( test2==1)[0][0]   #     
        eos=int(sp.median(sp.where( ndvi2==ndvi2[Teos]))) + indMax +1 # 

    if(som1==0):
        sos=-1
    if(som2==0):
        eos=-1        
    if(som1>0 and som2>0):
        
        los=eos-sos
        
    else:
        los=-1
    
    
    out=[sos,eos,los,indMin+1,indMax+1,ndviMin,ndviMax] # +1 parceque l'indice commence à 0
    
    return out


#%%
def metrique_pheno_derivative(ndvi=sp.empty):
    """
    This method use the second derivative of the NDVI to identifie the dates of beginning of season, end of season and more.
     Parameters:
     ----------
        
        ndvi : correspond à l'evolution DU NDVI pour un pixel sur une année
    
    """
    
    try:
        ndviMin=ndvi.min() #valeur minimale
        ndviMax=ndvi.max() #valeur maximale
        #ndviMean=ndvi.mean() #valeur moyenne
        
        indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
        indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
        d1=sp.convolve(ndvi, [1, -1],'same') #first derivative approximation
        d2=sp.convolve(ndvi, [1, -2, 1],'same') #second derivative approximation
        
        k1=d1[:-1]*d1[1:] #to find inflection point
        k2=d2[:-1]*d2[1:] #to find inflection point
        
        ind0d1=(sp.where(k1[:indMax]<0))[0][-1]
        ind0d2=(sp.where(k2[:indMax]<0))[0][-1]

        sos=ind0d2
        sos=sp.nanmax([ind0d1,ind0d2])
        
        ind0d22=(sp.where(k2[indMax+1:]<0))[0][0]

        
        eos=ind0d22+indMax
        
        los=eos-sos
        out=[sos,eos+1,los,indMin+1,indMax+1,ndviMin,ndviMax] # +1 parceque l'indice commence à 0
    except:
        out=[-1,-1,-1,-1,-1,-1,-1] 
    
    return out




    
#%%

def metrique_pheno_param(inNdvi=sp.empty,inSos=0,inEos=0,inIndMax=0):
    
    """
    This script aims to calculate different metrics phenological from NDVI   
    
     Parameters:
     ----------
     inNDVI: NDVI
     Insos: seizaine the corresponding early in season
     inEos: the seizaine corresponding to the end of season
     inIndMax: index of the maximum NDVI value (flowering)
    
     Returns:
     ------
     outListe: a list containing all the phenological metric calculated    
    """
    try:
        
        if (inSos<inEos and inSos>0 ):
            
            areabef=[]   #suface sous la courbe avant la valeur max du NDVI
            areaaft=[]   #surface sous la courbe après la valeur max du NDVI 
            pente1=[]    #pente du sos à la valeur max (vitesse de croissance)
            pente2=[]    #pente du max au eos (vitesse de croissance)
            tsos_tmax=[] #duree entre le debut de la saison et le max de vegetation
            area=[]      #surface du debut de la saison  à la fin
            tmax_teos=[] #duree entre la floraison et la fin de la saison
            
            ms=inSos-1      # -1 parceque indice commence à 0
            me=inEos-1      # -1 parceque indice commence à 0
            mMaX=inIndMax-1 #
            ndviMax=inNdvi[mMaX]
            
            areabef=sp.sum(inNdvi[ms:mMaX])
            areaaft=sp.sum(inNdvi[mMaX:inEos]) 
            area=sp.sum(inNdvi[ms:inEos])
            tsos_tmax=mMaX-ms        
            tmax_teos=me-mMaX
    
            if mMaX>ms and mMaX<me :
                
                pente1=(ndviMax-inNdvi[ms])/tsos_tmax
                pente2=(ndviMax-inNdvi[me])/tmax_teos
            else:
                pente1=0
                pente2=0
                
            
            outListe=[area,areabef,areaaft,inIndMax,tsos_tmax,tmax_teos,pente1,pente2]
        
        else:
            outListe=[-1,-1,-1,-1,-1,-1,-1,-1]
    except:
        outListe=[-1,-1,-1,-1,-1,-1,-1,-1]
    
    return outListe
