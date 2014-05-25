class IFilesystemPlugin(object):
    """Plugins of this class detect filesystem and 
    returns correct volume object"""

    def detect_mbr(filename, offset, type_id): pass
    def detect_gpt(filename, offset, type_guid): pass