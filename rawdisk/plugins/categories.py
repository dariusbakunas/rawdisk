from yapsy.IPlugin import IPlugin

class IFilesystemPlugin(IPlugin):
    """Plugins of this class detect filesystem and 
    returns correct volume object"""
    def register(self): pass
    def detect_mbr(self, filename, offset, type_id): pass
    def detect_gpt(self, filename, offset, type_guid): pass