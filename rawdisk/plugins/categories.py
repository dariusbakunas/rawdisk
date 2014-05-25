from yapsy.IPlugin import IPlugin

class IFilesystemPlugin(IPlugin):
    """Plugins of this class detect filesystem and 
    returns correct volume object"""

    def register(self): pass
    def detect(self, filename, offset): pass
    def get_volume_object(self): pass