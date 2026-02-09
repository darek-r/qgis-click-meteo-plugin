# ******************************************************************************
#
# compat.py
# ---------------------------------------------------------
# This module ensures QGIS version compatibility
# 
#
# Author:   Denis Ilyin, denis.ilyin@nextgis.com
# *****************************************************************************
# Copyright (c) 2015-2021. NextGIS, info@nextgis.com
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
# ******************************************************************************


from qgis import core

if hasattr(core, "QGis"):
    from qgis.core import QGis
else:
    from qgis.core import Qgis as QGis


class QgsCoordinateTransform(core.QgsCoordinateTransform):
    def __init__(self, src_crs, dst_crs):
        super().__init__()

        self.setSourceCrs(src_crs)
        self.setDestinationCrs(dst_crs)

    def setDestinationCrs(self, dst_crs):
        if QGis.QGIS_VERSION_INT >= 30000:
            super().setDestinationCrs(dst_crs)
        else:
            self.setDestCRS(dst_crs)


class QgsCoordinateReferenceSystem(core.QgsCoordinateReferenceSystem):
    @staticmethod
    def fromEpsgId(identifier):
        if QGis.QGIS_VERSION_INT >= 30000:
            return core.QgsCoordinateReferenceSystem.fromEpsgId(identifier)
        return core.QgsCoordinateReferenceSystem(identifier)

    def createFromProj(self, projString):
        if QGis.QGIS_VERSION_INT >= 30000:
            return super().createFromProj(projString)
        return super().createFromProj4(projString)


def getProjectCRSProjString():
    if QGis.QGIS_VERSION_INT >= 30000:
        return core.QgsProject.instance().crs().toProj()
    (proj4string, ok) = core.QgsProject.instance().readEntry(
        "SpatialRefSys", "ProjectCRSProj4String"
    )
    return proj4string
