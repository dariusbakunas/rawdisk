import sys
import hexdump
import scheme
import rawdisk.filesystems
from rawdisk.filesystems.common import detect_partition_format
from rawdisk.filesystems.ntfs import Partition_NTFS


class Reader:
    def __init__(self):
        self.debug = False
        self.partitions = []

    def load(self, filename):
        self.filename = filename

        # Detect partitioning scheme
        self.scheme = scheme.common.detect_scheme(filename)

        if (self.scheme == scheme.common.SCHEME_MBR):
            mbr = scheme.mbr.MBR()
            mbr.load(filename)

            for entry in mbr.partition_table.entries:
                pt_format = detect_partition_format(
                    filename,
                    entry.part_offset,
                    entry.part_type
                )

                if pt_format == rawdisk.filesystems.common.PART_FORMAT_NTFS:
                    partition = Partition_NTFS(filename, entry.part_offset)

        elif (self.scheme == scheme.common.SCHEME_GPT):
            print 'Partitioning scheme: GPT'
        elif (self.scheme == scheme.common.SCHEME_UNKNOWN):
            print 'Partitioning scheme is not supported.'
        else:
            print 'Error occured.'
            sys.exit()
