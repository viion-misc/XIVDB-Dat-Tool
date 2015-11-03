import struct
import logging

from io import BytesIO

class Texture:
    def __init__(self, file_handle):
        file_handle.seek(4)
        self._type = file_handle.read(2)
        file_handle.seek(8)

        unpackWidth = file_handle.read(2)
        unpackHeight = file_handle.read(2)

        if not unpackWidth:
            return

        if not unpackHeight:
            return

        self._width = struct.unpack("<H", unpackWidth)[0]
        self._height = struct.unpack("<H", unpackHeight)[0]

        file_handle.seek(80)
        self._data = file_handle.read()

    def get_as_dds(self):
        output = BytesIO()

        if not hasattr(self, '_height'):
            return

        output.write(b'DDS ') # magic
        output.write(struct.pack("<I", 124)) # size
        output.write(struct.pack("<I", 0))
        output.write(struct.pack("<I", self._height))
        output.write(struct.pack("<I", self._width))
        output.write(struct.pack("<IIIIIIIIIIIIII", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        output.write(struct.pack("<I", 32)) # size

        if self._type == b'\x41\x14':
            output.write(struct.pack("<I", 0x41))
            output.write(struct.pack("<I", 0))
            output.write(struct.pack("<I", 0x10))
            output.write(struct.pack("<I", 0x7c00))
            output.write(struct.pack("<I", 0x03E0))
            output.write(struct.pack("<I", 0x1F))
            output.write(struct.pack("<I", 0x8000))
        elif self._type == b'\x40\x14':
            output.write(struct.pack("<I", 0x41))
            output.write(struct.pack("<I", 0))
            output.write(struct.pack("<I", 0x10))
            output.write(struct.pack("<I", 0x0F00))
            output.write(struct.pack("<I", 0xF0))
            output.write(struct.pack("<I", 0x0F))
            output.write(struct.pack("<I", 0xF000))
        elif self._type == b'\x50\x14':
            output.write(struct.pack("<I", 0x41))
            output.write(struct.pack("<I", 0))
            output.write(struct.pack("<I", 0x20))
            output.write(struct.pack("<I", 0xFF0000))
            output.write(struct.pack("<I", 0xFF00))
            output.write(struct.pack("<I", 0xFF))
            output.write(struct.pack("<I", 0xFF000000))
        elif self._type == b'\x20\x34':
            output.write(struct.pack("<I", 0x04))
            output.write(b'DXT1')
            output.write(struct.pack("<IIIII", 0, 0, 0, 0, 0))
        elif self._type == b'\x31\x34':
            output.write(struct.pack("<I", 0x04))
            output.write(b'DXT5')
            output.write(struct.pack("<IIIII", 0, 0, 0, 0, 0))
        #else:
            #logging.error('Unknown type: %s', self._type)

        output.write(struct.pack("<I", 0x0010))
        output.write(struct.pack("<IIII", 0, 0, 0, 0))

        output.write(self._data)

        output.flush()
        output.seek(0)

        return output
