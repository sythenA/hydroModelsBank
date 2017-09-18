# -*- coding: utf-8 -*-
"""
/***************************************************************************
 hydroModelsBank
                                 A QGIS plugin
 Entrance App for Models Bank of hydrology Models
                             -------------------
        begin                : 2017-09-18
        copyright            : (C) 2017 by ManySplendid co.
        email                : yengtinglin@manysplendid.com
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
    """Load hydroModelsBank class from file hydroModelsBank.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .hydroBankEntrance import hydroModelsBank
    return hydroModelsBank(iface)
