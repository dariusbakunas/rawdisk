import sys
import hexdump
import scheme

class Reader:
    def __init__(self):
        self.debug = False

    def analyse(self, source):
        try:
            self.source = open(source, 'rb')
        except:
            print "Unable to open file: %s" % source
            sys.exit()

        self.source.seek(0)
        raw_record = self.source.read(512)

        bootsector = scheme.mbr.MBR()

        if (bootsector.load(raw_record)):
            # This is MBR bootsector (also could be GUID)
            bootsector.hexdump()

        self.source.close()
