# -*- coding: utf-8 -*-
"""
/***************************************************************************
 metriquePhenologique
                                 A QGIS plugin
 calcul de metrique phenologique et pretraitement
                             -------------------
        begin                : 2016-04-29
        copyright            : (C) 2016 by Dian
        email                : bah.mamadian@yahoo.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load metriquePhenologique class from file metriquePhenologique.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .metrique_phenologique import metriquePhenologique
    return metriquePhenologique(iface)
