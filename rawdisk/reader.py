import sys
import hexdump
import scheme

class Reader:
    def __init__(self):
        self.debug = False        

    def load(self, source):
        try:
            self.source = open(source, 'rb')
        except:
            print "Unable to open file: %s" % source
            sys.exit()

        # Detect partitioning scheme
        self.scheme = scheme.common.detect_scheme(self.source)

        if (self.scheme == scheme.common.SCHEME_MBR):
            print 'Partitioning scheme: MBR'
        elif (self.scheme == scheme.common.SCHEME_GPT):
            print 'Partitioning scheme: GPT'
        else:
            print 'Partitioning scheme is not supported.'

        self.source.close()
