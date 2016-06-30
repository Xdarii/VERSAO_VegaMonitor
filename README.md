![Logo](https://github.com/Xdarii/QGIS_Traitement_and_Pheno/blob/master/icon.png "Prétraitement et Param Pheno QGIS")

# Plugin Qgis: Pour le traitement des données MODIS MOD13Q1 et l'extraction de métrique phénologique
##MOD13Q1:
Les données mondiales de MOD13Q1 sont fournies tous les 16 jours à une résolution spatiale de 250 mètres dans une  projection sinusoïdale  avec une fauchée qui permet de couvrir de vaste zone (2350 Km). Tous les pixels d'une image ne sont pas pris à la même date car pour chaque pixel  il compare sa valeur sur les 16 jours et c'est la plus grande valeur qui est retenu.

##Prétraitement
###Découper 

Les données  téléchargées étant dans la majeur partie des cas trop grandes pour notre zone d'études nous avons pris soin de fournir à l'utilisateur la possibilité de découper sa zone en fonction d'un fichier shape (.shp) qui délimite sa zone d'études.
###Interpolation

L'option prétraitement en plus de l'option de découpage dispose d'une fonctionnalité d'interpolation.
Cette option permet de ramener toutes les images du NDVI à un intervalle de 16 jours si cela n'est pas le cas. C’est-à-dire en interpolant on s’assure que tous les pixels d’une image soient pris à la même date et que successivement les images soient à un intervalle de 16 jours.
En plus d’interpoler les images cette option propose de filtrer les images en sorties dans le cas où nous avons affaire à des images bruitées. 

###Lissage
Une option de filtrage est également disponible pour ce qui souhaiterais uniquement lisser les données qu'ils disposent que ce soit du MODIS ou autres satellites.


##Métrique Phénologique 
L’extraction des métrique phénologique fournit entre autre la détermination du start of season (SOS), end of season (EOS), le lenght of season (LOS), les cumules du NDVI avant et après la date de floraison et les anomalies associées pour chaque pixel de l’image pour toute l’année.

*Pour toutes informations supplémentaires veuillez consulter le wiki*


https://github.com/Xdarii/QGIS_Traitement_and_Pheno/wiki/M%C3%A9trique-Ph%C3%A9nologique
https://github.com/Xdarii/QGIS_Traitement_and_Pheno/wiki/Pr%C3%A9traitement
