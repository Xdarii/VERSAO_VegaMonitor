# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:41:03 2016

@author: U115-H016
"""
#j'ai modifié le script qui se trouve dans le site:
#https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#clip-a-geotiff-with-shapefile


from osgeo import  ogr


def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
  the pixel location of a geospatial coordinate
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  rtnX = geoMatrix[2]
  rtnY = geoMatrix[4]
  pixel = int((x - ulX) / xDist)
  line = int((ulY - y) / xDist)
  return (pixel, line)

#

def clipRaster(srcImage,G,P,shapefile_path):
    
    """
    Cette fonction prend en entrée un Raster et un vecteur puis elle
    renvoie un tableau decouper selon l'emprise du vecteur.
    Entree: 
    raster_path: raster en entrée
    shapefile_path: shape par lequel le raster sera découper
    Sortie: clip
    """

    #recupération des information du raster
    clip=0,
    ok=0
    # recupération des infos du shape
    driver = ogr.GetDriverByName('ESRI Shapefile')

    dataSource = driver.Open(shapefile_path, 0) # lecture du shape

    # verification de l'existance du shape file

    if dataSource is None:
        print 'le shape est vide : %s' % (shapefile_path)
    else:
#        print 'Opened %s' % (shapefile_path)
        lyr = dataSource.GetLayer() #chargement des couches qui se trouve dans le shape
        featureCount = lyr.GetFeatureCount() #récupération du nombre de couche
        #le decoupage est réalisé que si nous avons une seule couche ou polygone dans le shape
        
        if featureCount==1:
    
            # Convert the layer extent to image pixel coordinates
            minX, maxX, minY, maxY = lyr.GetExtent()
            ulX, ulY = world2Pixel(G, minX, maxY)
            lrX, lrY = world2Pixel(G, maxX, minY)
            
            # Calculate the pixel size of the new image
#            print  ulX,ulY,lrY,lrX
            L=abs(ulY-lrY)
            C= abs(ulX-lrX)
            [nL,nC,nZ]=srcImage.shape
            if nL<L and nC<C:
#                print "les données sont englobées par le shape"
                message=u"Les images sont déjà à l'interieur du shape. veuillez changer votre shape"
                return clip,G,P,ok,message
            if nL<L:
#                print "erreur les données ne peurvent être decoupé par ce shape"
                message=u"erreur les données ne peurvent être decoupé par ce shape. veuillez changer votre shape"
                return clip,G,P,ok,message
            if nC<C:
#                print "erreur les données ne peurvent être decoupé par ce shape"
                message=u"erreur les données ne peurvent être decoupé par ce shape. veuillez changer votre shape"
                return clip,G,P,ok,message
                
            clip = srcImage[ulY:lrY-1, ulX:lrX-1,:]
            G=list(G)
            G[0]=minX
            G[3]=maxY
            G=tuple(G)
#            print clip.shape
            
        #sinon pas de découpage 
        else:
#            print 'Opened %s has more than one layer' % (shapefile_path)
#            print featureCount
            message="le nombre de couche contenu dans le polygone est supérieur à 1. veuillez utiliser un shape qui ne contient qu'un seul polygone"
            return clip,G,P,ok,message
        ok=1
        message=u"découpage réussi"
        return clip,G,P,ok,message
    
#raster_path=r"D:\Mes Donnees\Dian_stage\Leroux\Dian\MOD11A2\MOD11A2_h17v07_2000_001_LST.tif"
#shapefile_path=r"D:\Mes Donnees\Dian_stage\Leroux\Mamadian\Data\Zones_d'Etudes.shp"
##[srcImage,G,P] = open_data(raster_path)
#clip,g,p,ok,message=clipRaster(raster_path,shapefile_path)
