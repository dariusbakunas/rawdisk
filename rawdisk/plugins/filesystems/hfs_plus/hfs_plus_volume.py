# -*- coding: utf-8 -*-


from rawdisk.filesystems.volume import Volume
from rawdisk.util.rawstruct import RawStruct

VOLUME_HEADER_OFFSET = 1024


class VolumeHeader(RawStruct):
    """Represents HFS+ volume header

    Attributes:
        signature (2 byte string): The volume signature, \
        which must be kHFSPlusSigWord ('H+') for an HFS Plus volume.
        version (ushort): The version of the volume format, \
        which is currently 4 (kHFSPlusVersion) for HFS Plus volumes.
        attributes (uint): HFS+ volume attributes
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.signature = self.get_string(0x00, 2)
        # HFS+ everything is stored in big-endian
        self.version = self.get_ushort_be(0x02)
        self.attributes = self.get_uint_be(0x04)


class HfsPlusVolume(Volume):
    """Structure for HFS+ volume.

    Attributes:
        fd (fd): file descriptor used to read volume information
        vol_header (VolumeHeader): Initialized :class:`VolumeHeader` object

    See Also:
        https://developer.apple.com/legacy/library/technotes/tn/tn1150.html
    """
    def __init__(self):
        self.fd = None
        self.vol_header = None

    def load(self, filename, offset):
        """Loads HFS+ volume information"""
        try:
            self.offset = offset
            self.fd = open(filename, 'rb')
            # 1024 - temporary, need to find out actual volume header size
            self.fd.seek(self.offset + VOLUME_HEADER_OFFSET)
            data = self.fd.read(1024)
            self.vol_header = VolumeHeader(data)

            self.fd.close()
        except IOError as e:
            print(e)

    def __str__(self):
        return "Type: HFS+, Offset: 0x%X" % (
            self.offset
        )
