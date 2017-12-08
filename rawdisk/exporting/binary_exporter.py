# coding=utf-8

class BinaryExporter(object):
    def export(self, input_filename, output_filename, start_offset, size):
        CHUNK_SIZE = 1024*1024
        remaining = size

        with open(input_filename, 'rb') as input, open(output_filename, 'wb+') as output:
            input.seek(start_offset)

            while remaining:
                chunk_size = CHUNK_SIZE if CHUNK_SIZE < remaining else remaining
                data = input.read(chunk_size)
                output.write(data)
                remaining -= chunk_size
