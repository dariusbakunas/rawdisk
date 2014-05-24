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
r.load('sample_images/ntfs.vhd')
```

* List partitions:

```python
for part in r.partitions:
	print part
```

```console
Type: NTFS, Offset: 0x10000, Size: 1020M, MFT Table Offset: 0x15465000
```

* Hexdump contents of selected system MFT entry and then its attributes

```python
from rawdisk.filesystems.ntfs import *

ntfs_vol = NtfsVolume()
# Use offset from previous output
ntfs_vol.mount("sample_images/ntfs.vhd", 0x10000)
mft_entry = ntfs_vol.mft_table.get_system_entry(MFT_ENTRY_MFT)

mft_entry.hexdump()

for attr in mft_entry.attributes:
	print
	attr.hexdump()

ntfs_partition.unmount()
```

```console
00000000: 10 00 00 00 60 00 00 00  00 00 18 00 00 00 00 00  ....`...........
00000010: 48 00 00 00 18 00 00 00  6C B1 67 D5 90 6C CF 01  H.......l.g..l..
00000020: 6C B1 67 D5 90 6C CF 01  6C B1 67 D5 90 6C CF 01  l.g..l..l.g..l..
00000030: 6C B1 67 D5 90 6C CF 01  06 00 00 00 00 00 00 00  l.g..l..........
00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 01 00 00  ................
00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................

00000000: 30 00 00 00 68 00 00 00  00 00 18 00 00 00 03 00  0...h...........
00000010: 4A 00 00 00 18 00 01 00  05 00 00 00 00 00 05 00  J...............
00000020: 6C B1 67 D5 90 6C CF 01  6C B1 67 D5 90 6C CF 01  l.g..l..l.g..l..
00000030: 6C B1 67 D5 90 6C CF 01  6C B1 67 D5 90 6C CF 01  l.g..l..l.g..l..
00000040: 00 40 00 00 00 00 00 00  00 40 00 00 00 00 00 00  .@.......@......
00000050: 06 00 00 00 00 00 00 00  04 03 24 00 4D 00 46 00  ..........$.M.F.
00000060: 54 00 00 00 00 00 00 00                           T.......

00000000: 80 00 00 00 48 00 00 00  01 00 40 00 00 00 01 00  ....H.....@.....
00000010: 00 00 00 00 00 00 00 00  3F 00 00 00 00 00 00 00  ........?.......
00000020: 40 00 00 00 00 00 00 00  00 00 04 00 00 00 00 00  @...............
00000030: 00 00 04 00 00 00 00 00  00 00 04 00 00 00 00 00  ................
00000040: 31 40 55 54 01 00 30 B7                           1@UT..0.

00000000: B0 00 00 00 50 00 00 00  01 00 40 00 00 00 05 00  ....P.....@.....
00000010: 00 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  ................
00000020: 40 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00  @........ ......
00000030: 08 10 00 00 00 00 00 00  08 10 00 00 00 00 00 00  ................
00000040: 31 01 54 54 01 21 01 DB  F8 00 01 00 00 A0 67 88  1.TT.!........g.

<...>
```

Installation
------------

To install RawDisk, simply run:

	$ python setup.py install

For system-wide installation, you may need to prefix the previous command with ``sudo``:

	$ sudo python setup.py install