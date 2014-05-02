RawDisk
=======

A Python library for raw access to filesystems. Started it for educational purposes.

Filesystems Supported
---------------------
	* NTFS

Download
--------

	$ git clone git:://github.com/dariusbakunas/rawdisk.git

Documentation and usage
-----------------------

	```python
	from rawdisk import Reader
	r = Reader()
	r.load("/dev/disk2")
	```

Installation
------------

To install RawDisk, simply run::

	$ python setup.py install

For system-wide installation, you may need to prefix the previous command with ``sudo``::

	$ sudo python setup.py install