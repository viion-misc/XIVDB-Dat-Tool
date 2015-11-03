import logging
import struct

import numpy

class Mesh:
    def __init__(self, file_handle):
        self._vertex_buffer_offset = None
        self._vertex_count = None
        self._vertex_size = None

        self._index_buffer_offset = None
        self._index_count = None

        self._read(file_handle)

    def _read(self, file_handle):
        (self._vertex_count, self._index_count) = struct.unpack("<II", file_handle.read(8))

        file_handle.seek(0x8, 1)

        (self._index_buffer_offset, self._vertex_buffer_offset) = struct.unpack("<II", file_handle.read(8))

        file_handle.seek(0x8, 1)

        (self._vertex_size,) = struct.unpack("<B", file_handle.read(1))

        file_handle.seek(0x3, 1)

    def __repr__(self):
        return "<vertex_buffer_offset: %d - vertex_count: %d - vertex_size: %d - index_buffer_offet: %d - index_count: %d>" % (self._vertex_buffer_offset, self._vertex_count, self._vertex_size, self._index_buffer_offset, self._index_count)


# Bounding boxes = lod + meshes + bones
class Model:
    def __init__(self, path, file_handle):
        self._path = path

        self._vertex_buffer = None
        self._index_buffer = None
        self._vertex_type = None

        self._meshes = []

        self._read(file_handle)

    def get_path(self):
        return self._path

    def _read(self, file_handle):
        logging.info('Reading file: %s' % self._path)

        file_handle.seek(0x40)

        (mesh_nb, material_nb) = struct.unpack("<HH", file_handle.read(4))

        pos = file_handle.tell()
        file_handle.seek(2, 1)
        self._vertex_type = file_handle.read(1)
        file_handle.seek(pos)

        file_handle.seek(0x88 * mesh_nb, 1) # Skipping mesh headers

        file_handle.seek(0x4, 1) # Skipping number of strings

        (string_block_size,) = struct.unpack("<I", file_handle.read(4))

        file_handle.seek(string_block_size, 1) # Skipping string block

        file_handle.seek(0x18, 1) # Skipping part of header
        number_of_struct_to_skip = struct.unpack("<H", file_handle.read(2))[0]
        file_handle.seek(0x20, 1) # Skipping header

        file_handle.seek(0x18 * number_of_struct_to_skip, 1)

        lod_0_mesh_nb = struct.unpack("<H", file_handle.read(2))[0]

        file_handle.seek(0x28, 1) # skipping unimportant stuff

        (vertex_buffer_size, index_buffer_size, vertex_buffer_offset, index_buffer_offset) = struct.unpack("<IIII", file_handle.read(16))

        pos = file_handle.tell()

        file_handle.seek(vertex_buffer_offset)
        #self._vertex_buffer = numpy.frombuffer(file_handle.read(vertex_buffer_size), dtype='float16', count=vertex_buffer_size // 2).astype('float32')
        self._vertex_buffer = file_handle.read(vertex_buffer_size)
        file_handle.seek(index_buffer_offset)
        #self._index_buffer = numpy.frombuffer(file_handle.read(index_buffer_size), dtype='uint8', count=index_buffer_size)
        self._index_buffer = file_handle.read(index_buffer_size)
        file_handle.seek(pos)

        file_handle.seek(0x3C * 2, 1) # skipping two lower lods

        for j in range(lod_0_mesh_nb):
            self._meshes.append(Mesh(file_handle))

        logging.info(self._meshes)
