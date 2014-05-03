RawDisk
=======

A Python library for raw access to filesystems. Started it for educational purposes.

Filesystems Supported
---------------------
* NTFS

Download
--------

	$ git clone https://github.com/dariusbakunas/rawdisk.git

Documentation and usage
-----------------------

```python
from rawdisk import Reader
r = Reader()
r.load("/dev/disk2")
```

* List partitions:

```python
for part in r.partitions:
	print part
```

```console
Type: NTFS, Offset: 0x100000, Size: 14G
```

* Hexdump contents of selected system MFT entry

```python
from rawdisk.filesystems.ntfs import NTFS_Partition
from rawdisk.filesystems.mft import MFT_ENTRY_VOLUME

ntfs_partition = NTFS_Partition()
ntfs_partition.load("/dev/disk2", 0x100000)
mft_entry = ntfs_partition.mft_table.get_metadata_entry(MFT_ENTRY_VOLUME)
mft_entry.hexdump()
```

```console
00000000: 46 49 4C 45 30 00 03 00  88 16 00 02 00 00 00 00  FILE0...........
00000010: 03 00 01 00 38 00 01 00  60 01 00 00 00 04 00 00  ....8...`.......
00000020: 00 00 00 00 00 00 00 00  06 00 00 00 03 00 00 00  ................
00000030: 02 00 00 00 00 00 00 00  10 00 00 00 60 00 00 00  ............`...
00000040: 00 00 18 00 00 00 00 00  48 00 00 00 18 00 00 00  ........H.......
00000050: 64 D0 37 F5 EA 63 CF 01  64 D0 37 F5 EA 63 CF 01  d.7..c..d.7..c..
00000060: 64 D0 37 F5 EA 63 CF 01  64 D0 37 F5 EA 63 CF 01  d.7..c..d.7..c..
00000070: 06 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000080: 00 00 00 00 01 01 00 00  00 00 00 00 00 00 00 00  ................
00000090: 00 00 00 00 00 00 00 00  30 00 00 00 68 00 00 00  ........0...h...
000000A0: 00 00 18 00 00 00 01 00  50 00 00 00 18 00 01 00  ........P.......
000000B0: 05 00 00 00 00 00 05 00  64 D0 37 F5 EA 63 CF 01  ........d.7..c..
000000C0: 64 D0 37 F5 EA 63 CF 01  64 D0 37 F5 EA 63 CF 01  d.7..c..d.7..c..
000000D0: 64 D0 37 F5 EA 63 CF 01  00 00 00 00 00 00 00 00  d.7..c..........
000000E0: 00 00 00 00 00 00 00 00  06 00 00 00 00 00 00 00  ................
000000F0: 07 03 24 00 56 00 6F 00  6C 00 75 00 6D 00 65 00  ..$.V.o.l.u.m.e.

<...>
```

Installation
------------

To install RawDisk, simply run:

	$ python setup.py install

For system-wide installation, you may need to prefix the previous command with ``sudo``:

	$ sudo python setup.py install