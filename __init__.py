from .main import ClickMeteoPlugin

def classFactory(iface):
    return ClickMeteoPlugin(iface)
