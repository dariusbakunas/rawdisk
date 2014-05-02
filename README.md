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

Installation
------------

To install RawDisk, simply run:

	$ python setup.py install

For system-wide installation, you may need to prefix the previous command with ``sudo``:

	$ sudo python setup.py install