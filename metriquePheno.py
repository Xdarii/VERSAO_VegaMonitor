# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 10:53:01 2016

@author: U115-H016
"""

import scipy as sp

    
    
def metrique_pheno_greenbrown(ndvi=sp.empty, methode="trs",seuil1=-1,seuil2=-1):
    
    """
    
    
    Ce script permet d'identifier les dates de debut de saison,
    de fin de saison à partir du NDVI.
    il est inspiré du script R:https://github.com/rforge/greenbrown/blob/master/pkg/greenbrown/R/PhenoTrs.R
    Entrée:
        ndvi: les données de ndvi
        seuil1: correspond au seuil autour du quel on pense trouver le debut de la vegetation
        seuil2: correspond au seuil autour du quel on pense trouver la sénéscence
        ndvi : correspond à l'evolution DU NDVI pour un pixel sur une année
        methode: correspond à la methode à utiliser pour l'estimation
    Sortie:
        une liste contenant le sos, eos, los, indMin n(indice du min),indMax (indice du max), ndvi min et ndvi max
    """
    
  
    
    ndviMin=ndvi.min() #valeur minimale
    ndviMax=ndvi.max() #valeur maximale
    #ndviMean=ndvi.mean() #valeur moyenne
    ndviEcart=ndviMax-ndviMin+0.00001
    
    indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
    indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
    
    if methode=="white":
    
        ratio=(ndvi-ndviMin)/ndviEcart       
        if seuil1<0 and seuil2<0:
            seuil1=0.5
            seuil2=0.5
    
    if methode=="trs":
    
        ratio=ndvi
        if seuil1<0 and seuil2<0:
            seuil1=0.3
            seuil2=0.6
          
    
    test1=ratio[:indMax] >seuil1     # recherche les valeur de NDVI qui montre la croissance (augmentation de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
    test2=ratio[indMax:] <seuil2  # recherche les valeur de NDVI qui montre la senescence (baisse de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
    
    som1=sp.sum(test1) # teste si le seuil est adapté aux données 
    som2=sp.sum(test2) #teste 
    


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
def metrique_pheno_vito(ndvi=sp.empty,seuil1=0.3,seuil2=0.75):
    """
    Ce script permet d'identifier les dates de debut de saison, de fin de saison à partir du NDVI à partir d'un seuil.
    Entrée:
        ndvi: les données de ndvi
        seuil1: correspond au seuil autour du quel on pense trouver le debut de la vegetation
        seuil2: correspond au seuil autour du quel on pense trouver la sénéscence
        ndvi : correspond à l'evolution DU NDVI pour un pixel sur une année
        methode: correspond à la methode à utiliser pour l'estimation
    Sortie:
        une liste contenant le sos, eos, los, indMin n(indice du min),indMax (indice du max), ndvi min et ndvi max
    """
    ndviMin=ndvi.min() #valeur minimale
    ndviMax=ndvi.max() #valeur maximale
    #ndviMean=ndvi.mean() #valeur moyenne
    
    indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
    indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
    
    
    ndviMin1=ndvi[:indMax].min() #valeur minimale
    indMin1=int(sp.median(sp.where(ndvi[:indMax]==ndviMin1))) #indice du minimum
    
    ndviMin2=ndvi[indMax:].min() #valeur minimale
    indMin2=int(sp.median(sp.where(ndvi[indMax:]==ndviMin2)))+indMax #indice du minimum

    ndvi1=ndvi[indMin1:indMax] #phase de croissance
    ndvi2=ndvi[indMax:indMin2] #phase de senescence
    
    
    ndviEcart1=(ndviMax-ndviMin1)*seuil1 +ndviMin1 #l'ecart entre la valeur min et max
    
    ndviEcart2=(ndviMax-ndviMin2)*seuil2  + ndviMin2     #l'ecart entre la valeur min et max de la valeur maximale   
    test1=ndvi1>=ndviEcart1         # 
    test2=ndvi2<=ndviEcart2        #

    som1=sp.sum(test1)
    som2=sp.sum(test2)
    
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
def metrique_pheno_Tang(ndvi=sp.empty,seuil1=-1,seuil2=-1):

    """
    
    
    Ce script permet d'identifier les dates de debut de saison,
    de fin de saison à partir du NDVI. Elle est aussi appelé methode à seuil variable
    En utilisant l'option par défaut le seuil utilisé correspond à celui conseillé dans :
    Variability and Climate Change Trend in Vegetation Phenology of Recent Decades in the Greater Khingan
    Mountain Area, Northeastern China
     Huan Tang , Zhenwang Li , Zhiliang Zhu , Baorui Chen , Baohui Zhang  and Xiaoping Xin ,
     
    
    seuil1: correspond au seuil autour du quel on pense trouver le debut de la croissance de la végétation
    seuil1: correspond au seuil autour du quel on pense trouver la fin de la croissance de la végétation
    
    ndvi : correspond à l'evolution DU NDVI pour un pixel sur une année
    
    
    """
  
    
    ndviMin=ndvi.min() #valeur minimale
    ndviMax=ndvi.max() #valeur maximale
    #ndviMean=ndvi.mean() #valeur moyenne
    ndviEcart=ndviMax-ndviMin
    
    indMin=int(sp.median(sp.where(ndvi==ndviMin))) #indice du minimum
    indMax=int(sp.median(sp.where(ndvi==ndviMax))) #indice du max
    
    
    ratio=(ndvi-ndviMin)/ndviEcart     
    
    if seuil1<0 and seuil2<0 :
        seuil=ndviEcart/5
        seuil1=seuil
        seuil2=seuil
    
    test1=ratio[:indMax] >seuil1     # recherche les valeur de NDVI qui montre la croissance (augmentation de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
    test2=ratio[indMax:] <seuil2  # recherche les valeur de NDVI qui montre la senescence (baisse de NDVI) et verifie que cette valeur se trouve dans l'intervalle definit
    
    som1=sp.sum(test1) # teste si le seuil est adapté aux données 
    som2=sp.sum(test2) #teste 
    


    if (som1>0):
        
        Tsos=sp.where( test1==1)[0][0]  
        sos=int(sp.median(sp.where( ratio[:indMax]==ratio[Tsos])))  + 1
        

    if (som2>0):

        Teos=sp.where( test2==1)[0][0] + indMax  #     
        eos=int(sp.median(sp.where( ratio[indMax:]==ratio[Teos]))) + indMax + 1 # 

    if(som1==0):
        
        sos=-1
        
    if(som2==0):
        
        eos=-1  
        
    if(som1>0 and som2>0):
        
        los=eos-sos
        
    else:
        los=-1



    out=[]
    out=[sos,eos,los,indMin+1,indMax+1,ndviMin,ndviMax]


    return out
    
#%%

def metrique_pheno_param(inNdvi=sp.empty,inSos=0,inEos=0,inIndMax=0):
    
    """
    Ce script a pour objectif de calculer differentes metriques phenologique 
    à partir du NDVI
    
    Entree:
    inNDVI: le NDVI
    inSos:  la seizaine correspondant au debut de saison
    inEos:  la seizaine correspondant à la fin de saison
    inIndMax: indice de la valeur maximale du NDVI (floraison)
    
    Sortie:
    outListe: une liste contenant l'ensemble des métriques phénologiques calculées
    
    """
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
    
    return outListe
