import logging
from collections import namedtuple
from struct import Struct

INFO_BLOCK_RECORD_STRUCT = Struct("<II")
DAT_NB_STRUCT = Struct("<I")
FILE_INFO_STRUCT = Struct("<IIII")

FILE_INFO_NT = namedtuple('file_info', ['dat_nb', 'dir_hash', 'filename_hash', 'dat_offset'])

def extract_hash_table(file_handle):
    print('extract_hash_table', file_handle)
    file_handle.seek(0x400) # skipping header block
    file_handle.seek(0x08, 1) # skipping size/type

    hash_table_block_offset, hash_table_block_size = INFO_BLOCK_RECORD_STRUCT.unpack(file_handle.read(INFO_BLOCK_RECORD_STRUCT.size))
    dat_nb = DAT_NB_STRUCT.unpack(file_handle.read(DAT_NB_STRUCT.size))

    # reading hash table
    file_handle.seek(hash_table_block_offset)

    hash_table = {}
    for index in range(hash_table_block_size // FILE_INFO_STRUCT.size):
        (filename_hash, dir_hash, dat_offset, _) = FILE_INFO_STRUCT.unpack(file_handle.read(FILE_INFO_STRUCT.size))

        dat_nb = (dat_offset & 0x0F) // 0x02
        dat_offset = (dat_offset & 0xFFFFFFF0) * 0x08

        if not dir_hash in hash_table:
            hash_table[dir_hash] = {}

        hash_table[dir_hash][filename_hash] = FILE_INFO_NT._make(
            (dat_nb, dir_hash, filename_hash, dat_offset)
        )

    return hash_table
