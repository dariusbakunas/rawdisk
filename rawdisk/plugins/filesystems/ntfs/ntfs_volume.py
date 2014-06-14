# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Darius Bakunas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from rawdisk.util.filesize import size_str
from mft import MftTable, ENTRY_VOLUME
from mft_attribute import MFT_ATTR_VOLUME_NAME, MFT_ATTR_VOLUME_INFO
from bootsector import BootSector
from rawdisk.filesystems.volume import Volume

NTFS_BOOTSECTOR_SIZE = 512

# entries to preload
NUM_SYSTEM_ENTRIES = 12


class NtfsVolume(Volume):
    """Represents NTFS volume.

    Attributes:
        offset (uint): offset to the partition from the start of the disk \
        in bytes
        fd (fd): file descriptor that is used to load volume information
        bootsector (BootSector): initialized \
        :class:`~.bootsector.BootSector` object.
        mft_table (MftTable): initialized :class:`~.mft.MftTable` object

    See More:
        http://en.wikipedia.org/wiki/NTFS
    """
    def __init__(self):
        self.offset = 0
        self.bootsector = None
        self.mft_table = None
        self.vol_name = None
        self.mft_zone_size = None
        self.major_ver = None
        self.minor_ver = None

    def load(self, filename, offset):
        """Loads NTFS volume information

        Args:
            filename (str): Path to file/device to read the volume \
            information from.
            offset (uint): Valid NTFS partition offset from the beginning \
            of the file/device.

        Raises:
            IOError: If source file/device does not exist or is not readable
        """
        self.offset = offset
        self.filename = filename

        self.bootsector = BootSector(
            filename=filename,
            length=NTFS_BOOTSECTOR_SIZE,
            offset=self.offset)

        self.mft_table = MftTable(
            mft_entry_size=self.bootsector.bpb.mft_record_size,
            filename=self.filename,
            offset=self.mft_table_offset
        )

        self.mft_table.preload_entries(NUM_SYSTEM_ENTRIES)

        self._load_volume_information()

    def _load_volume_information(self):
        # Get $Volume file.
        vol_entry = self.mft_table.get_entry(ENTRY_VOLUME)
        vol_attr = vol_entry.lookup_attribute(MFT_ATTR_VOLUME_NAME)

        if (vol_attr is not None):
            self.vol_name = vol_attr.vol_name

        vol_info_attr = vol_entry.lookup_attribute(MFT_ATTR_VOLUME_INFO)

        if (vol_info_attr is not None):
            self.major_ver = vol_info_attr.major_ver
            self.minor_ver = vol_info_attr.minor_ver

        # Determine the size of the MFT zone.
        num_clusters = self.bootsector.bpb.total_clusters
        self.mft_zone_size = self.bootsector.bpb.bytes_per_cluster * \
            self._get_mft_zone_size(num_clusters)

    def _get_mft_zone_size(self, num_clusters, mft_zone_multiplier=1):
        """Returns mft zone size in clusters.
        From ntfs_progs.1.22."""

        sizes = {
            4: num_clusters >> 1,           # 50%
            3: (num_clusters * 3) >> 3,     # 37,5%
            2: num_clusters >> 2,           # 25%
        }

        return sizes.get(mft_zone_multiplier, num_clusters >> 3)

    def __str__(self):
        return "Type: NTFS, Offset: 0x%X, Size: %s, MFT Table Offset: 0x%X" % (
            self.offset,
            size_str(self.size),
            self.mft_table_offset
        )

    def dump_volume(self):
        print "Volume Information"
        print "\tVolume Name: %s" % self.vol_name
        print "\tVolume Version: %d.%d" % (self.major_ver, self.minor_ver)
        print "\tVolume Size: %s" % size_str(self.bootsector.bpb.volume_size)
        print "\tVolume Offset: 0x%x" % self.offset
        print "\tTotal Sectors: %u" % self.bootsector.bpb.total_sectors
        print "\tTotal Clusters: %u" % self.bootsector.bpb.total_clusters
        # print "\tFree Clusters:"
        # print "\tFree Space:"
        print "\tMFT Offset: 0x%x (from beginning of volume)" % \
            self.bootsector.bpb.mft_offset
        print "\tMFT Mirror Offset: 0x%x" % \
            self.bootsector.bpb.mft_mirror_offset
        print "\tMFT Record Size: %s" % \
            size_str(self.bootsector.bpb.mft_record_size)
        print "\tMFT Size: %s (%s of drive)" % (
            size_str(self.mft_zone_size), "{0:.0f}%".format(
                float(self.mft_zone_size) /
                self.bootsector.bpb.volume_size * 100
                )
            )

    @property
    def size(self):
        """
        Returns:
            int: Total size of NTFS volume in bytes
        """
        return self.bootsector.bpb.volume_size

    @property
    def mft_table_offset(self):
        """
        Returns:
            int: MFT Table offset from the beginning of the disk in bytes
        """
        return self.offset + self.bootsector.bpb.mft_offset

    @property
    def mft_mirror_offset(self):
        """
        Returns:
            int: MFT Mirror Table offset from the beginning of the disk in bytes
        """
        return self.offset + self.bootsector.bpb.mft_mirror_offset
