

CRC_32_POLY = 0xEDB88320

CRC_TABLE = None
REV_CRC_TABLE = None

def get_crc_table():
    global CRC_TABLE
    if not CRC_TABLE:
        _precompute_crc_tables()
    return CRC_TABLE

def get_rev_crc_table():
    global REV_CRC_TABLE
    if not REV_CRC_TABLE:
        _precompute_crc_tables()
    return REV_CRC_TABLE

def _precompute_crc_tables():
    global CRC_TABLE
    global REV_CRC_TABLE

    table_size = 256

    CRC_TABLE = [None] * table_size
    REV_CRC_TABLE = [None] * table_size

    for i in range(table_size):
        crc = i
        for j in range(8, 0, -1):
            crc = ((CRC_32_POLY ^ (crc >> 1)) if (crc & 1) else (crc >> 1)) & 0xFFFFFFFF
        CRC_TABLE[i] = crc
        REV_CRC_TABLE[crc >> 24] = i + ((CRC_TABLE[i] & 0x00ffffff) << 8)


def crc_32(data, init_crc = 0):
    crc_table = get_crc_table()
    crc = init_crc

    for i in range(len(data)):
        crc = (crc_table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8)) & 0xFFFFFFFF

    return crc

def rev_crc_32(data, init_crc = 0):
    rev_crc_table = get_rev_crc_table()
    crc = init_crc

    data_size = len(data)

    for i in range(data_size + 4):
        crc = (rev_crc_table[crc >> 24] ^ ((crc << 8) & 0xFFFFFF00) ^ (data[data_size - i - 1] if i < data_size else 0)) & 0xFFFFFFFF

    return crc
