***********
Basic Usage
***********

Loading data file
=================

In order to start filesystem analysis, you need to create :class:`~rawdisk.reader.Reader` instance::

    from rawdisk.reader import Reader

    r = Reader()
    r.load('sample_images/ntfs_mbr.vhd')

Last line looks through available filesystem plugins in *rawdisk/plugins/filesystem*. If filesystem is matched, it initializes plugin's volume object. In order to print a list of available partitions (will only show those that were matched), type::

    r.list_partitions()

.. code-block:: sh

    Type: NTFS, Offset: 0x10000, Size: 7.00MB, MFT Table Offset: 0x265000

Show selected volume information
================================

To print selected volume information::

    ntfs_vol = r.partitions[0]
    ntfs_vol.dump_volume()

Output::

    Volume Information
        Volume Name: New Volume
        Volume Version: 3.1
        Volume Size: 1.00GB
        Volume Offset: 0x10000
        Total Sectors: 2091007
        Total Clusters: 261375
        MFT Offset: 0x15455000 (from beginning of volume)
        MFT Mirror Offset: 0x2000
        MFT Record Size: 1.00KB
        MFT Size: 127.62MB (12% of drive)

Analysing selected partition
============================

r.partitions is a list that contains matched volume objects. For example to get NTFS volume object (:class:`NtfsVolume <rawdisk.plugins.filesystems.ntfs.ntfs_volume.NtfsVolume>`)from the listing above::

    ntfs_vol = r.partitions[0]

To get $MFT entry (index: 0)::

    mft = ntfs_vol.mft_table.get_entry(0)

    mft.hexdump()

Output::

    00000000: 46 49 4C 45 30 00 03 00  82 4D 10 00 00 00 00 00  FILE0....M......
    00000010: 01 00 01 00 38 00 01 00  A0 01 00 00 00 04 00 00  ....8...........
    00000020: 00 00 00 00 00 00 00 00  07 00 00 00 00 00 00 00  ................
    00000030: 02 00 FF 00 00 00 00 00  10 00 00 00 60 00 00 00  ............`...
    00000040: 00 00 18 00 00 00 00 00  48 00 00 00 18 00 00 00  ........H.......
    00000050: F8 58 8A 44 11 01 D0 01  F8 58 8A 44 11 01 D0 01  .X.D.....X.D....
    00000060: F8 58 8A 44 11 01 D0 01  F8 58 8A 44 11 01 D0 01  .X.D.....X.D....
    00000070: 06 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
    00000080: 00 00 00 00 00 01 00 00  00 00 00 00 00 00 00 00  ................

    <...>

To print a list of attributes belonging to this $MFT entry::

    for attr in mft.attributes:
        print attr

Output::

    Type: $STANDARD_INFORMATION Name: N/A Resident Size: 96
    Type: $FILE_NAME Name: N/A Resident Size: 104
    Type: $DATA Name: N/A Non-Resident Size: 80
    Type: $BITMAP Name: N/A Non-Resident Size: 72
