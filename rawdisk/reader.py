import sys
import hexdump
import scheme
import rawdisk.filesystems
from rawdisk.filesystems.common import *
from rawdisk.filesystems.hfs_plus import HfsPlusVolume
from rawdisk.filesystems.detector import FilesystemDetectorSingleton

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
        detector = FilesystemDetectorSingleton.get()

        if (self.scheme == scheme.common.SCHEME_MBR):
            print "Scheme: MBR"
            mbr = scheme.mbr.Mbr()
            mbr.load(filename)

            # Go through table entries and analyse ones that are supported
            for entry in mbr.partition_table.entries:
                volume = detector.detect_mbr(
                    filename, 
                    entry.part_offset, 
                    entry.part_type
                )

                if (volume!=None):
                    volume.load(filename, entry.part_offset)
                    self.partitions.append(volume)

        elif (self.scheme == scheme.common.SCHEME_GPT):
            print "Scheme: GPT"
            gpt = scheme.gpt.Gpt()
            gpt.load(filename)
            
            for entry in gpt.partition_entries:
                volume = detector.detect_gpt(
                    filename,
                    entry.first_lba * 512,
                    entry.type_guid
                )

                if (volume != None):
                    volume.load(filename, entry.first_lba * 512)
                    self.partitions.append(volume)

        elif (self.scheme == scheme.common.SCHEME_UNKNOWN):
            print 'Partitioning scheme is not supported.'
        else:
            print 'Error occured.'
            sys.exit()
