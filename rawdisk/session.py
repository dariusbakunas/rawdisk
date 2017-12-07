# -*- coding: utf-8 -*-

import rawdisk.scheme
import logging
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.filesystems.unknown_volume import UnknownVolume
from rawdisk.plugins.plugin_manager import PluginManager
from rawdisk.scheme.mbr import SECTOR_SIZE
from rawdisk.scheme.common import PartitionScheme
from rawdisk.exporting.binary_exporter import BinaryExporter


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
    def __init__(self, filename=None, bs=512, load_plugins=True):
        self.logger = logging.getLogger(__name__)
        self.__volumes = []
        self.__partition_scheme = None
        self.__filename = None
        self.__fs_plugins = []

        if load_plugins:
            self.load_plugins()

        if filename:
            self.load(filename, bs)

    @property
    def filesystem_plugins(self):
        return self.__fs_plugins

    def load_plugins(self):
        """Load filesystem detection plugins"""
        plugin_manager = PluginManager()
        self.__fs_plugins = plugin_manager.load_filesystem_plugins()

    @property
    def volumes(self):
        """Return a list of volumes"""
        return self.__volumes

    @property
    def partition_scheme(self):
        return self.__partition_scheme

    @property
    def filename(self):
        return self.__filename

    def __analyze_disk_image(self, filename, bs=512):
        pass

    def reload(self):
        pass

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

        plugin_objects = [plugin.plugin_object for plugin in self.__fs_plugins]
        fs_detector = FilesystemDetector(fs_plugins=plugin_objects)

        if self.__partition_scheme == PartitionScheme.SCHEME_MBR:
            self.__load_mbr_volumes(filename, fs_detector, bs)
        elif self.__partition_scheme == PartitionScheme.SCHEME_GPT:
            self.__load_gpt_volumes(filename, fs_detector, bs)
        else:
            self.logger.warning('Partitioning scheme could not be determined.')
            # try detecting standalone volume
            volume = fs_detector.detect_standalone(filename, offset=0)
            if volume is not None:
                volume.load(filename, offset=0)
                self.__volumes.append(volume)
            else:
                self.logger.warning(
                    'Were not able to detect standalone volume type')

    def __load_gpt_volumes(self, filename, fs_detector, bs=512):
        gpt = rawdisk.scheme.gpt.Gpt()
        gpt.load(filename)

        for entry in gpt.partition_entries:
            volume = fs_detector.detect_gpt(
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

    def __load_mbr_volumes(self, filename, fs_detector, bs=512):
        mbr = rawdisk.scheme.mbr.Mbr(filename)
        # Go through table entries and analyse ones that are supported
        for entry in mbr.partition_table.partitions:
            volume = fs_detector.detect_mbr(
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
