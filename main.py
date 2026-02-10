# ******************************************************************************
#
# Click Meteo
# ---------------------------------------------------------
# Obtaining data from API based on the point clicked
#
# Copyright (C) 2026 Dariusz Radwan (radwan.dariusz@gmail.com)
#          
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

import os
import inspect
import urllib, json

from PyQt5.QtWidgets import QAction, QLabel
from PyQt5.QtGui import QIcon 

from qgis.gui import QgsMapTool

from .compat import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    getProjectCRSProjString,
)

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class ClickMeteoPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self):
        # Create a Toolbar
        self.clickMeteoToolbar = self.iface.addToolBar('ClickMeteo Toolbar')
        
        # Create an Action with Logo
        icon = os.path.join(os.path.join(cmd_folder, 'logo_temp.png'))
        self.action = QAction(QIcon(icon), 'Show Current Temperature', self.clickMeteoToolbar)
        
        # Create a label
        self.label = QLabel('Current temperature (select and click on the map):', parent=self.clickMeteoToolbar)
            
        # Add all the widgets to the toolbar
        self.clickMeteoToolbar.addWidget(self.label)
        self.clickMeteoToolbar.addAction(self.action)
      
        # Connect the run() method to the action
        self.action.triggered.connect(self.click_action)
      
    def unload(self):
        del self.clickMeteoToolbar

    def click_action(self):
            self.tool = cmTool(self.iface)
            self.canvas.setMapTool(self.tool)


class cmTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def canvasReleaseEvent(self, e):
        # Obtaining coordinates of the point clicked 
        point = self.canvas.getCoordinateTransform().toMapCoordinates(
            e.pos().x(), e.pos().y()
        )
        pt = pointToWGS84(point)

        # Obtaining data from open-meteo.com API
        url = f'http://api.open-meteo.com/v1/forecast?latitude={pt.y():.2f}&longitude={pt.x():.2f}&current=temperature_2m'

        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
        except (urllib.error.URLError) as e:
            self.iface.messageBar().pushWarning('Error', f'Failed to fetch data. Internet connection may be unavailable or API endpoint may be down.')
            return

        # Push message bar with results
        self.iface.messageBar().pushSuccess('Success',f'Temperature for latitude {pt.y():.2f} and longitude {pt.x():.2f} is <b>{data["current"]["temperature_2m"]} {data["current_units"]["temperature_2m"]}</b>')
       
       

# Transform coordinates to WGS84
# Copyright (C) 2008-2010 Barry Rownligson (barry.rowlingson@gmail.com)
def pointToWGS84(point):
    projstring = getProjectCRSProjString()
    if not projstring:
        return point

    t = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    f = QgsCoordinateReferenceSystem()
    f.createFromProj(projstring)

    transformer = QgsCoordinateTransform(f, t)
    pt = transformer.transform(point)
    return pt