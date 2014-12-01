from rawdisk.util.filesize import size_str


class UnknownVolume(object):
    def __init__(self, offset, type_id, size):
        self.offset = offset
        self.type_id = type_id
        self.size = size

    def __str__(self):
        return "Type: Unknown (%s), Offset: 0x%X, Size: %s" % (
            self.type_id,
            self.offset,
            size_str(self.size)
        )
