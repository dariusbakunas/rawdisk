***********
Basic Usage
***********

Loading data file
=================

In order to start filesystem analysis, you need to create :class:`~reader.Reader` instance::

	from rawdisk.reader import Reader

	r = Reader()
	r.load('sample_images/ntfs.vhd')

Last line looks through available filesystem plugins in *rawdisk/plugins/filesystem*. If filesystem is matched, it initializes plugin's volume object. In order to print a list of available partitions (will only show those that were matched), type::
	
	r.list_partitions()

.. code-block:: sh

	Type: NTFS, Offset: 0x10000, Size: 1020M, MFT Table Offset: 0x15465000

Analysing selected partition
============================

r.partitions is a list that contains matched volume objects. For example to get NTFS volume object (:class:`NtfsVolume <plugins.filesystems.ntfs.ntfs_volume.NtfsVolume>`)from the listing above::

	ntfs_vol = r.partitions[0]

To get $MFT system entry (index: 0)::

	mft = ntfs_vol.mft_table.get_system_entry(0)

	mft.hexdump()

Output::

	00000000: 46 49 4C 45 30 00 03 00  EA 22 20 00 00 00 00 00  FILE0...." ....
	00000010: 01 00 01 00 38 00 01 00  A0 01 00 00 00 04 00 00  ....8...........
	00000020: 00 00 00 00 00 00 00 00  06 00 00 00 00 00 00 00  ................
	00000030: 02 00 67 88 00 00 00 00  10 00 00 00 60 00 00 00  ..g.........`...
	00000040: 00 00 18 00 00 00 00 00  48 00 00 00 18 00 00 00  ........H.......
	00000050: 6C B1 67 D5 90 6C CF 01  6C B1 67 D5 90 6C CF 01  l.g..l..l.g..l..
	00000060: 6C B1 67 D5 90 6C CF 01  6C B1 67 D5 90 6C CF 01  l.g..l..l.g..l..
	00000070: 06 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
	00000080: 00 00 00 00 00 01 00 00  00 00 00 00 00 00 00 00  ................

	<...>

To print a list of attributes belonging to this $MFT entry::

	for attr in mft.attributes:
		print attr

Output::

	Type: $STANDARD_INFORMATION Name: N/A Resident Size: 96
	Type: $FILE_NAME Name: N/A Resident Size: 104
	Type: $DATA Name: N/A Non-Resident Size: 72
	Type: $BITMAP Name: N/A Non-Resident Size: 80