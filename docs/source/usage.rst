***********
Basic Usage
***********

Loading data file
=================

In order to start filesystem analysis, you need to create :class:`rawdisk.reader.Reader` instance

.. code-block:: python
   :emphasize-lines: 4

	from rawdisk import Reader

	r = Reader()
	r.load('sample_images/ntfs.vhd')

Last line looks through available filesystem plugins in *rawdisk/plugins/filesystem*. If filesystem is matched, it initializes plugin's volume object. In order to print a list of available partitions (will only show those that were matched), type::
	
	r.list_partitions()

.. code-block:: sh

	Type: NTFS, Offset: 0x10000, Size: 1020M, MFT Table Offset: 0x15465000