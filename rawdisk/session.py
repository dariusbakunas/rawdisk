# -*- coding: utf-8 -*-

import rawdisk.scheme
import logging
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.plugins.manager import Manager
from rawdisk.filesystems.unknown_volume import UnknownVolume
from rawdisk.scheme.mbr import SECTOR_SIZE


class Session(object):
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
        self.logger = logging.getLogger(__name__)
        self.__volumes = []
        self.__partition_scheme = None
        self.__filename = None
        self.__plugin_manager = Manager()

    def load_plugins(self):
        """Load filesystem detection plugins"""
        self.__plugin_manager.load_plugins()

    @property
    def volumes(self):
        """Return a list of volumes"""
        return self.__volumes

    @property
    def partition_scheme(self):
        return self.__partition_scheme

    def load(self, filename, bs=512):
        """Starts filesystem analysis. Detects supported filesystems and \
        loads :attr:`partitions` array.

        Args:
            filename - Path to file or device for reading.

        Raises:
            IOError - File/device does not exist or is not readable.
        """
        self.__filename = filename
        self.__volumes = []



        # Detect partitioning scheme
        self.__partition_scheme = rawdisk.scheme.common.detect_scheme(filename)

        if self.__partition_scheme == rawdisk.scheme.common.SCHEME_MBR:
            self.__load_mbr_volumes(filename, bs)
        elif self.__partition_scheme == rawdisk.scheme.common.SCHEME_GPT:
            self.__load_gpt_volumes(filename, bs)
        else:
            self.logger.warning('Partitioning scheme could not be determined.')

    def __load_gpt_volumes(self, filename, bs=512):
        detector = FilesystemDetector()
        gpt = rawdisk.scheme.gpt.Gpt()
        gpt.load(filename)

        for entry in gpt.partition_entries:
            volume = detector.detect_gpt(
                filename,
                entry.first_lba * bs,
                entry.type_guid
            )

            if volume is not None:
                volume.load(filename, entry.first_lba * bs)
                self.__volumes.append(volume)
            else:
                self.logger.warning(
                    'Were not able to detect GPT volume type')

                self.__volumes.append(
                    UnknownVolume(
                        entry.first_lba * bs, entry.type_guid,
                        (entry.last_lba - entry.first_lba) * bs
                    )
                )

    def __load_mbr_volumes(self, filename, bs=512):
        detector = FilesystemDetector()
        mbr = rawdisk.scheme.mbr.Mbr(filename)
        # Go through table entries and analyse ones that are supported
        for entry in mbr.partition_table.entries:
            volume = detector.detect_mbr(
                filename,
                entry.part_offset,
                entry.part_type
            )

            if volume is not None:
                volume.load(filename, entry.part_offset)
                self.__volumes.append(volume)
            else:
                self.logger.warning(
                    'Were not able to detect MBR volume type')
                self.__volumes.append(
                    UnknownVolume(
                        entry.part_offset, entry.part_type,
                        entry.total_sectors * SECTOR_SIZE
                    )
                )
