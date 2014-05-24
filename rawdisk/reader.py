import sys
import hexdump
import scheme
import rawdisk.filesystems
from rawdisk.filesystems.common import *
from rawdisk.filesystems.ntfs import NtfsVolume
from rawdisk.filesystems.hfs_plus import HfsPlusVolume


class Reader:
    def __init__(self):
        self.debug = False
        self.partitions = []

    def list_partitions(self):
        for part in self.partitions:
            print part

    def load(self, filename):
        self.filename = filename

        # Detect partitioning scheme
        self.scheme = scheme.common.detect_scheme(filename)

        if (self.scheme == scheme.common.SCHEME_MBR):
            mbr = scheme.mbr.Mbr()
            mbr.load(filename)

            # Go through table entries and analyse ones that are supported
            for entry in mbr.partition_table.entries:
                pt_format = detect_mbr_partition_format(
                    filename,
                    entry.part_offset,
                    entry.part_type
                )

                if pt_format == rawdisk.filesystems.common.PART_FORMAT_NTFS:
                    partition = NtfsVolume()
                    partition.mount(filename, entry.part_offset)
                    partition.unmount()
                    self.partitions.append(partition)

        elif (self.scheme == scheme.common.SCHEME_GPT):
            gpt = scheme.gpt.Gpt()
            gpt.load(filename)
            
            for entry in gpt.partition_entries:
                pt_format = detect_gpt_partition_format(
                    filename,
                    entry.first_lba * 512,
                    entry.type_guid)

                if pt_format == rawdisk.filesystems.common.PART_FORMAT_HFS_PLUS:
                    partition = HfsPlusVolume()

                    # TODO: Figure out how to calculate block size
                    partition.mount(filename, entry.first_lba * 512)
                    partition.unmount()
                    self.partitions.append(partition)
                elif pt_format == rawdisk.filesystems.common.PART_FORMAT_NTFS:
                    partition = NtfsVolume()
                    partition.mount(filename, entry.first_lba * 512)
                    partition.unmount()
                    self.partitions.append(partition)

        elif (self.scheme == scheme.common.SCHEME_UNKNOWN):
            print 'Partitioning scheme is not supported.'
        else:
            print 'Error occured.'
            sys.exit()
