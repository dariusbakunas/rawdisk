import sys
import hexdump
import scheme
import rawdisk.filesystems
from rawdisk.filesystems.common import detect_partition_format
from rawdisk.filesystems.ntfs import NtfsVolume


class Reader:
    def __init__(self):
        self.debug = False
        self.partitions = []

    def load(self, filename):
        self.filename = filename

        # Detect partitioning scheme
        self.scheme = scheme.common.detect_scheme(filename)

        if (self.scheme == scheme.common.SCHEME_MBR):
            mbr = scheme.mbr.Mbr()
            mbr.load(filename)

            # Go through table entries and analyse ones that are supported
            for entry in mbr.partition_table.entries:
                pt_format = detect_partition_format(
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
            print 'Partitioning scheme: GPT'
        elif (self.scheme == scheme.common.SCHEME_UNKNOWN):
            print 'Partitioning scheme is not supported.'
        else:
            print 'Error occured.'
            sys.exit()
