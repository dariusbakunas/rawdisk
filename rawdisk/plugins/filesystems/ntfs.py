import rawdisk.plugins.categories as categories

class NtfsPlugin(categories.IFilesystemPlugin):
    def register(self):
        print "ntfs was registered"

    def detect_mbr(self, filename, offset, type_id): 
        print "call: detect_mbr from NtfsPlugin"

    def detect_gpt(self, filename, offset, type_guid):
        print "call: detect_gpt from NtfsPlugin"