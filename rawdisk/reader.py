# -*- coding: utf-8 -*-

import rawdisk.scheme
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.plugins.manager import Manager
from rawdisk.filesystems.unknown_volume import UnknownVolume
from rawdisk.scheme.mbr import SECTOR_SIZE


class Reader(object):
    """Main class used to start filesystem analysis.

    Attributes:
        partitions (list): List of detected filesystems \
        (intialized :class:`Volume <rawdisk.filesystems.volume.Volume>` \
            objects)
        scheme (enum): One of \
        :attr:`SCHEME_MBR <rawdisk.scheme.common.SCHEME_MBR>` \
        or :attr:`SCHEME_GPT <rawdisk.scheme.common.SCHEME_GPT>`.
    """
    def __init__(self):
        self.partitions = []
        self.scheme = None
        self.filename = None
        self.manager = Manager()

        # Load filesystem detection plugins
        self.manager.load_plugins()

    def list_partitions(self):
        """Print a list of detected partitions."""

        for part in self.partitions:
            print(part)

    def load(self, filename, bs=512):
        """Starts filesystem analysis. Detects supported filesystems and \
        loads :attr:`partitions` array.

        Args:
            filename - Path to file or device for reading.

        Raises:
            IOError - File/device does not exist or is not readable.
        """
        self.filename = filename

        # Detect partitioning scheme
        self.scheme = rawdisk.scheme.common.detect_scheme(filename)
        detector = FilesystemDetector()

        if (self.scheme == rawdisk.scheme.common.SCHEME_MBR):
            mbr = rawdisk.scheme.mbr.Mbr(filename)

            # Go through table entries and analyse ones that are supported
            for entry in mbr.partition_table.entries:
                volume = detector.detect_mbr(
                    filename,
                    entry.part_offset,
                    entry.part_type
                )

                if (volume is not None):
                    volume.load(filename, entry.part_offset)
                    self.partitions.append(volume)
                else:
                    self.partitions.append(
                        UnknownVolume(
                            entry.part_offset, entry.part_type,
                            entry.total_sectors * SECTOR_SIZE
                        )
                    )

        elif (self.scheme == rawdisk.scheme.common.SCHEME_GPT):
            gpt = rawdisk.scheme.gpt.Gpt()
            gpt.load(filename)

            for entry in gpt.partition_entries:
                volume = detector.detect_gpt(
                    filename,
                    entry.first_lba * bs,
                    entry.type_guid
                )

                if (volume is not None):
                    volume.load(filename, entry.first_lba * bs)
                    self.partitions.append(volume)
                else:
                    self.partitions.append(
                        UnknownVolume(
                            entry.first_lba * bs, entry.type_guid,
                            (entry.last_lba - entry.first_lba) * bs
                        )
                    )

        elif (self.scheme == rawdisk.scheme.common.SCHEME_UNKNOWN):
            print('Partitioning scheme is not supported.')
        else:
            print('Partitioning scheme could not be determined.')
