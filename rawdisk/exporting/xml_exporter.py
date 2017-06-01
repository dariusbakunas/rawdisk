import xml.etree.ElementTree as xml
from rawdisk.scheme.mbr import Mbr
from rawdisk.scheme.gpt import Gpt


class XmlExporter(object):
    @staticmethod
    def export(session, filename=None):
        # partitioning_scheme = XmlExporter.get_partitioning_scheme_xml()
        #
        # with open(output_filename, "wb") as f:
        #     tree.write(f, encoding='utf-8', xml_declaration=True)
        pass

    @staticmethod
    def get_partitioning_scheme_xml(scheme):
        root = xml.Element('partitioning-scheme')

        if isinstance(scheme, Mbr):
            xml.SubElement(root, 'mbr', {
                'offset': '{:#04x}'.format(scheme.offset)
            })
        elif isinstance(scheme, Gpt):
            xml.SubElement(root, 'gpt', {
                'offset': '{:#04x}'.format(scheme.offset)
            })

        return root
