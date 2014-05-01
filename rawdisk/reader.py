import sys
import hexdump
import scheme


class Reader:
    def __init__(self):
        self.debug = False            

    def load(self, filename):        
        # Detect partitioning scheme
        self.scheme = scheme.common.detect_scheme(filename)

        if (self.scheme == scheme.common.SCHEME_MBR):            
            mbr = scheme.mbr.MBR()
            mbr.load(filename)
        elif (self.scheme == scheme.common.SCHEME_GPT):
            print 'Partitioning scheme: GPT'
        elif (self.scheme == scheme.common.SCHEME_UNKNOWN):
            print 'Partitioning scheme is not supported.'
        else:
            print 'Error occured.'
            sys.exit()
