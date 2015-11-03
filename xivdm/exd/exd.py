import logging
from collections import namedtuple
from struct import Struct

HEADER_STRUCT = Struct(">4sHHI")
STRUCT_INDEX_STRUCT = Struct(">II")
STRUCT_HEADER = Struct(">IH")

STRUCT_INDEX_NT = namedtuple('struct_index', ['id', 'offset'])

DATATYPE_STRUCT = [
    Struct(">I"), # 0
    Struct("?"),
    Struct("b"),
    Struct("B"),
    Struct(">h"),
    Struct(">H"),
    Struct(">i"),
    Struct(">I"),
    Struct("?"),
    Struct(">f"),
    Struct("?"), # 10
    Struct(">Q"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"), # 20
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("?"),
    Struct("b"), # 25
    Struct("b"), # h = size 2 - 26
    Struct("b"), # 27
    Struct("b"),
    Struct("b"),
    Struct("b"), # 30
    Struct("b"),
    Struct("b"),  # 32
]

def extract_data(file_handle, header):
    (_, _, _, index_size) = HEADER_STRUCT.unpack(file_handle.read(HEADER_STRUCT.size))

    file_handle.seek(0x20) # Skip header

    struct_indexes = list()
    for index in range(index_size // 8):
        struct_indexes.append(STRUCT_INDEX_NT._make(STRUCT_INDEX_STRUCT.unpack(file_handle.read(STRUCT_INDEX_STRUCT.size))))

    structs = dict()
    for struct_index in struct_indexes:
        values = list()
        for member in header.members:
            file_handle.seek(struct_index.offset + 0x06 + member.offset)
            #print("member.type = %s", member.type)
            #logging.info('-------------')
            member_struct = DATATYPE_STRUCT[member.type]
            value = member_struct.unpack(file_handle.read(member_struct.size))[0]
            if member.type == 0x00: # if string
                file_handle.seek(struct_index.offset + 0x06 + header.data_offset + value)
                string_size = 0
                char = file_handle.read(0x01)
                while char != b'\0' and char != b'':
                    string_size += 1
                    char = file_handle.read(0x01)
                file_handle.seek(struct_index.offset + 0x06 + header.data_offset + value)
                value = file_handle.read(string_size)

            values.append(value)
        structs[struct_index.id] = values
    return structs
